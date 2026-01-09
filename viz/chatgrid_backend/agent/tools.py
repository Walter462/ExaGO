"""
Hardcoded tools called by LLM in a tool-specified context.
"""

import os
import time
import logging
import psycopg
from langchain.tools import tool
from typing import Literal, Dict, Any, TypedDict, Annotated, Sequence, Optional
from agent.utils import _get_db_connection
from agent.logger import default_server_logging

# Activate logging messages at certain level
logger = default_server_logging('tools', level=logging.INFO)


@tool
def test_database_connection(
    database_name: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None
) -> str:
    """Test database connection with specified or default parameters.
    Use this to verify database connectivity or try different connection parameters
    if the default .env configuration is not working.
    
    Args:
        database_name: Database name (defaults to POSTGRES_DB from .env)
        host: Database host (defaults to POSTGRES_HOST from .env, or 'localhost')
        port: Database port (defaults to POSTGRES_PORT from .env, or '5432')
        user: Database user (defaults to POSTGRES_USER from .env)
        password: Database password (defaults to POSTGRES_PASSWORD from .env)
        
    Returns:
        A message indicating connection success or failure with details
    """
    logger.info(f"Tool invoked: test_database_connection(database={database_name or 'default'}, host={host or 'default'}, user={user or 'default'})")
    
    try:
        start_time = time.time()
        conn, db = _get_db_connection(database_name, host, port, user, password)
        
        # Test the connection by running a simple query
        cursor = conn.cursor()
        logger.debug(f"Executing version query on database '{db}'")
        cursor.execute("SELECT version();")
        row = cursor.fetchone()
        version = row[0] if row is not None else "unknown"
        
        elapsed = time.time() - start_time
        logger.info(f"Successfully tested connection to '{db}' in {elapsed:.2f}s")
        
        cursor.close()
        conn.close()
        
        return f"✓ Successfully connected to database '{db}'.\nPostgreSQL version: {version}"
        
    except ValueError as e:
        logger.error(f"Configuration error in test_database_connection: {str(e)}")
        return f"✗ Configuration error: {str(e)}"
    except psycopg.Error as e:
        logger.error(f"Database connection failed in test_database_connection: {str(e)}")
        return f"✗ Database connection failed: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in test_database_connection: {str(e)}", exc_info=True)
        return f"✗ Unexpected error: {str(e)}"


@tool
def list_databases(
    host: Optional[str] = None,
    port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None
) -> str:
    """List all databases available on the PostgreSQL server.
    This connects to the 'postgres' maintenance database to query available databases.
    Use this to discover what databases exist on the server.
    
    Args:
        host: Database host (defaults to POSTGRES_HOST from .env, or 'localhost')
        port: Database port (defaults to POSTGRES_PORT from .env, or '5432')
        user: Database user (defaults to POSTGRES_USER from .env)
        password: Database password (defaults to POSTGRES_PASSWORD from .env)
        
    Returns:
        A formatted list of all databases on the server
    """
    logger.info(f"Tool invoked: list_databases(host={host or 'default'}, user={user or 'default'})")
    
    try:
        start_time = time.time()
        # Connect to 'postgres' database to list all databases
        conn, _ = _get_db_connection(
            database_name="postgres",
            host=host,
            port=port,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Query to list all non-template databases
        query = """
        SELECT 
            datname,
            pg_size_pretty(pg_database_size(datname)) as size,
            pg_encoding_to_char(encoding) as encoding,
            datcollate as collation
        FROM 
            pg_database
        WHERE 
            datistemplate = false
        ORDER BY 
            datname;
        """
        
        logger.debug("Executing database listing query")
        cursor.execute(query)
        results = cursor.fetchall()
        
        elapsed = time.time() - start_time
        logger.info(f"Retrieved {len(results)} databases in {elapsed:.2f}s")
        
        if not results:
            cursor.close()
            conn.close()
            return "No databases found on server."
        
        # Format output
        output = [f"Databases on server: {host or os.getenv('POSTGRES_HOST', 'localhost')}\n{'='*60}\n"]
        for datname, size, encoding, collation in results:
            output.append(f"  • {datname:<20} Size: {size:<10} Encoding: {encoding}")
        
        output.append(f"\nTotal: {len(results)} database(s)")
        
        cursor.close()
        conn.close()
        
        return "\n".join(output)
        
    except ValueError as e:
        logger.error(f"Configuration error in list_databases: {str(e)}")
        return f"Error: {str(e)}"
    except psycopg.Error as e:
        logger.error(f"Database error in list_databases: {str(e)}")
        return f"Database error: {str(e)}\nNote: Make sure your user has permission to connect to the 'postgres' database."
    except Exception as e:
        logger.error(f"Unexpected error in list_databases: {str(e)}", exc_info=True)
        return f"Error listing databases: {str(e)}"


@tool
def get_database_tables(
    database_name: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None
) -> str:
    """Get a simple list of all user tables in the PostgreSQL database.
    Use this first to see what tables exist before getting detailed schema.
    This is more efficient than getting the full schema when you just want table names.
    
    Args:
        database_name: Database name (defaults to POSTGRES_DB from .env)
        host: Database host (defaults to POSTGRES_HOST from .env)
        port: Database port (defaults to POSTGRES_PORT from .env)
        user: Database user (defaults to POSTGRES_USER from .env)
        password: Database password (defaults to POSTGRES_PASSWORD from .env)
        
    Returns:
        A formatted list of tables in the database
    """
    logger.info(f"Tool invoked: get_database_tables(database={database_name or 'default'})")
    
    try:
        start_time = time.time()
        conn, db = _get_db_connection(database_name, host, port, user, password)
        cursor = conn.cursor()
        
        # Simple query to list tables
        query = """
        SELECT 
            table_schema,
            table_name,
            table_type
        FROM 
            information_schema.tables
        WHERE 
            table_schema NOT IN ('information_schema', 'pg_catalog')
            AND table_type = 'BASE TABLE'
        ORDER BY 
            table_schema, table_name;
        """
        
        logger.debug(f"Executing table listing query on database '{db}'")
        cursor.execute(query)
        results = cursor.fetchall()
        
        elapsed = time.time() - start_time
        logger.info(f"Retrieved {len(results)} tables from '{db}' in {elapsed:.2f}s")
        
        if not results:
            cursor.close()
            conn.close()
            return f"No tables found in database '{db}'."
        
        # Format output
        output = [f"Tables in database: {db}\n{'='*60}\n"]
        for schema, table, table_type in results:
            output.append(f"  • {schema}.{table}")
        
        output.append(f"\nTotal: {len(results)} table(s)")
        
        cursor.close()
        conn.close()
        
        return "\n".join(output)
        
    except ValueError as e:
        logger.error(f"Configuration error in get_database_tables: {str(e)}")
        return f"Error: {str(e)}"
    except psycopg.Error as e:
        logger.error(f"Database error in get_database_tables: {str(e)}")
        return f"Database error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in get_database_tables: {str(e)}", exc_info=True)
        return f"Error retrieving tables: {str(e)}"


@tool
def get_postgres_schema(
    database_name: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None
) -> str:
    """Get detailed database schema from PostgreSQL with all columns, types, and constraints.
    This returns comprehensive information but can be lengthy for databases with many tables.
    Consider using get_database_tables first to see what tables exist.
    
    Args:
        database_name: Database name (defaults to POSTGRES_DB from .env)
        host: Database host (defaults to POSTGRES_HOST from .env)
        port: Database port (defaults to POSTGRES_PORT from .env)
        user: Database user (defaults to POSTGRES_USER from .env)
        password: Database password (defaults to POSTGRES_PASSWORD from .env)
        
    Returns:
        A formatted string containing the complete database schema
    """
    logger.info(f"Tool invoked: get_postgres_schema(database={database_name or 'default'})")
    
    try:
        start_time = time.time()
        conn, db = _get_db_connection(database_name, host, port, user, password)
        cursor = conn.cursor()
        
        # Query to get all tables and their columns with detailed information
        query = """
        SELECT 
            t.table_schema,
            t.table_name,
            c.column_name,
            c.data_type,
            c.character_maximum_length,
            c.is_nullable,
            c.column_default,
            tc.constraint_type,
            kcu.constraint_name
        FROM 
            information_schema.tables t
        LEFT JOIN 
            information_schema.columns c ON t.table_name = c.table_name 
            AND t.table_schema = c.table_schema
        LEFT JOIN 
            information_schema.key_column_usage kcu ON c.column_name = kcu.column_name 
            AND c.table_name = kcu.table_name 
            AND c.table_schema = kcu.table_schema
        LEFT JOIN 
            information_schema.table_constraints tc ON kcu.constraint_name = tc.constraint_name
            AND kcu.table_schema = tc.table_schema
        WHERE 
            t.table_schema NOT IN ('information_schema', 'pg_catalog')
            AND t.table_type = 'BASE TABLE'
        ORDER BY 
            t.table_schema, t.table_name, c.ordinal_position;
        """
        
        logger.debug(f"Executing detailed schema query on database '{db}'")
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Count unique tables for logging
        unique_tables = len(set((row[0], row[1]) for row in results))
        elapsed = time.time() - start_time
        logger.info(f"Retrieved schema for {unique_tables} tables with {len(results)} columns from '{db}' in {elapsed:.2f}s")
        
        if not results:
            cursor.close()
            conn.close()
            return f"No tables found in database '{db}'."
        
        # Format the schema information
        schema_output = [f"Database Schema for: {db}\n{'='*60}\n"]
        current_table = None
        
        for row in results:
            schema, table, column, data_type, max_length, nullable, default, constraint_type, constraint_name = row
            
            # New table section
            if current_table != f"{schema}.{table}":
                current_table = f"{schema}.{table}"
                schema_output.append(f"\nTable: {current_table}\n{'-'*60}")
            
            # Format column information
            col_info = f"  - {column}: {data_type}"
            if max_length:
                col_info += f"({max_length})"
            if nullable == "NO":
                col_info += " NOT NULL"
            if default:
                col_info += f" DEFAULT {default}"
            if constraint_type:
                col_info += f" [{constraint_type}]"
            
            schema_output.append(col_info)
        
        cursor.close()
        conn.close()
        
        return "\n".join(schema_output)
        
    except ValueError as e:
        logger.error(f"Configuration error in get_postgres_schema: {str(e)}")
        return f"Error: {str(e)}"
    except psycopg.Error as e:
        logger.error(f"Database error in get_postgres_schema: {str(e)}")
        return f"Database error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in get_postgres_schema: {str(e)}", exc_info=True)
        return f"Error retrieving schema: {str(e)}"
