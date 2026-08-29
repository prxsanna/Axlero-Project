"""
MetricMind PostgreSQL Database Engine and Connection Handler.

PostgreSQL is the single authoritative source of truth for all business data.
"""

import os
from typing import List, Dict, Any, Tuple, Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "metricmind")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

_engine: Optional[Engine] = None

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600
        )
    return _engine

engine = get_engine()

def check_connection() -> Dict[str, Any]:
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "connected",
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME,
            "user": DB_USER
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME,
            "user": DB_USER,
            "hint": "Please verify PostgreSQL service is running and credentials in .env are correct."
        }

def execute_raw_sql(sql_query: str, params: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
    eng = get_engine()
    try:
        with eng.connect() as conn:
            if params:
                result = conn.execute(text(sql_query), params)
            else:
                result = conn.execute(text(sql_query))
            
            if result.returns_rows:
                columns = list(result.keys())
                raw_rows = result.fetchall()
                dict_rows = [dict(zip(columns, row)) for row in raw_rows]
                return dict_rows, columns
            else:
                conn.commit()
                return [], []
    except SQLAlchemyError as err:
        raise RuntimeError(f"PostgreSQL Database Error: {str(err)}") from err

if __name__ == "__main__":
    status = check_connection()
    if status["status"] == "connected":
        print(f"PostgreSQL connected successfully to '{status['database']}' at {status['host']}:{status['port']}.")
    else:
        print(f"PostgreSQL connection failed: {status['error']}")
        print(f"Hint: {status['hint']}")