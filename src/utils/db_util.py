
import psycopg2
from datetime import datetime

class DbUtil:
    def __init__(self, logger, connection_string: str):
        self.logger = logger
        self.connection_string = connection_string
        self.conn = None

    def init(self):
        try:
            self.conn = psycopg2.connect(self.connection_string)
            self.logger.info(f"Connected to database: {self.conn.get_dsn_parameters()['dbname']}")
            with self.conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS public.hackathon (timestamp TEXT);");
            self.conn.commit()
        except psycopg2.Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise

    def write_row(self):
        if not self.conn:
            raise RuntimeError("DB connection not initialized")
        
        timestamp = datetime.now().isoformat()
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO public.hackathon (timestamp) VALUES (%s)", (timestamp,))
        self.conn.commit()

    def get_row_count(self) -> int:
        if not self.conn:
            raise RuntimeError("DB connection not initialized")

        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM public.hackathon")
            return cur.fetchone()[0]
