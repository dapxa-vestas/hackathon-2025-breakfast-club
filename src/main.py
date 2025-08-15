import os
import signal
import threading

from utils.log_util import LogUtil
from utils.db_util import DbUtil
from utils.metrics_util import MetricsUtil

otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
connection_string = os.getenv("CONNECTION_STRING")
structured_logs_enabled = os.getenv("STRUCTURED_LOGS_ENABLED", "false").lower() == "true"

metrics_enabled = bool(otel_endpoint)
database_enabled = bool(connection_string)

logger = LogUtil(use_structured_logs=structured_logs_enabled)

if database_enabled:
    db = DbUtil(logger, connection_string)

if metrics_enabled:
    metrics = MetricsUtil(otel_endpoint)

stop_event = threading.Event()
def signal_handler(signum, frame):
    logger.info("Shutting down gracefully...")
    stop_event.set()

def init_metrics():
    if not metrics_enabled:
        logger.warn("No OTEL_EXPORTER_OTLP_ENDPOINT set. Metrics disabled.")
    else:
        logger.info("OTEL_EXPORTER_OTLP_ENDPOINT is set. Metrics enabled.")
        metrics.init()

def init_database():
    if not database_enabled:
        logger.warn("No CONNECTION_STRING set. Database disabled.")
    else:
        logger.info("CONNECTION_STRING set. Starting database setup.")
        db.init()

def main():
    logger.info("Starting...")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    init_metrics()
    init_database()

    while not stop_event.is_set():
        logger.info("Starting worker loop")
        if metrics_enabled:
            logger.info("Writing metrics..")
            metrics.write_counter("loops", 1)
        else:
            logger.warn("Skipping metrics, because they are not configured.")

        if database_enabled:
            logger.info("Interacting with database..")
            try:
                db.write_row()
                row_count = db.get_row_count()
                if metrics_enabled:
                    metrics.write_counter("rows_created", 1)
                logger.info(f"There are {row_count} rows in the database")
            except Exception as e:
                logger.error(f"Failed to interact with database: {e}")
        else:
            logger.warn("Skipping database interaction, because it is not configured.")

        logger.info("Worker loop finished, will run again in 15 seconds")
        stop_event.wait(timeout=15)

    if metrics_enabled:
        metrics.clean_up_metrics()

if __name__ == "__main__":
    main()
