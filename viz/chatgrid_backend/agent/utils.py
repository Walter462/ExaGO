import os
import psycopg
from typing import Literal, Dict, Any, TypedDict, Annotated, Sequence, Optional
from agent.logger import default_server_logging
import logging

# Activate logging messages at certain level
logger = default_server_logging('db_utils', level=logging.DEBUG)

# Helper function for database connection (reusable by other tools)
def _get_db_connection(
    database_name: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None
):
    """Helper function to establish PostgreSQL connection.
    Returns tuple of (connection, database_name)
    """
    host = host or os.getenv("POSTGRES_HOST", "localhost")
    port = port or os.getenv("POSTGRES_PORT", "5432")
    db = database_name or os.getenv("POSTGRES_DB")
    user = user or os.getenv("POSTGRES_USER")
    password = password or os.getenv("POSTGRES_PASSWORD", "")
    
    if not all([host, port, db, user]):
        logger.error("Missing required database parameters: host=%s, port=%s, db=%s, user=%s", 
                    host, port, db, user)
        raise ValueError("Database connection parameters not configured. Please set them in .env file or provide them directly.")
    
    logger.debug("Attempting database connection: host=%s, port=%s, db=%s, user=%s", 
                host, port, db, user)
    
    try:
        conn = psycopg.connect(
            host=host,
            port=port,
            dbname=db,
            user=user,
            password=password
        )
        logger.debug("Successfully connected to database '%s' at %s:%s", db, host, port)
        return conn, db
    except Exception as e:
        logger.error("Failed to connect to database '%s' at %s:%s - %s", 
                    db, host, port, str(e))
        raise
