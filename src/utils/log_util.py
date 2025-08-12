
import logging
import json
import sys
import threading
from datetime import datetime

class LogUtil:
    def __init__(self, use_structured_logs: bool):
        self.use_structured_logs = use_structured_logs
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(handler)

    def _log(self, level: str, message: str):
        if self.use_structured_logs:
            log_entry = {
                "level": level,
                "message": message,
                "timestamp": datetime.utcnow().isoformat(),
                "thread": threading.get_ident(),
            }
            print(json.dumps(log_entry))
        else:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            thread_id = threading.get_ident()
            print(f"{timestamp} [{level}] [thread {thread_id}] {message}")

    def info(self, message: str):
        self._log("INFO", message)

    def warn(self, message: str):
        self._log("WARN", message)

    def error(self, message: str):
        self._log("ERROR", message)

