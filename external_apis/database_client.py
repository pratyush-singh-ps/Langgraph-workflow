"""
Database Client for External APIs

Handles database connections and queries using AWS Secrets Manager for credentials.
"""

import asyncio
import re
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from .config import ExternalAPIConfig, Environment
from .aws_secrets import AWSSecretsManager

logger = logging.getLogger(__name__)

class DatabaseClient:
    """Database client for executing queries with automatic secret management."""
    
    def __init__(self):
        """Initialize database client."""
        self.secrets_manager = AWSSecretsManager()
    
    def _validate_select_query(self, query: str) -> bool:
        """
        Validate that the query is a SELECT statement only.
        
        Args:
            query: SQL query string
            
        Returns:
            bool: True if valid SELECT query, False otherwise
        """
        # Remove comments and normalize whitespace
        query_clean = re.sub(r'--.*$', '', query, flags=re.MULTILINE)  # Remove single line comments
        query_clean = re.sub(r'/\*.*?\*/', '', query_clean, flags=re.DOTALL)  # Remove multi-line comments
        query_clean = re.sub(r'\s+', ' ', query_clean).strip().upper()
        
        # print(f"Cleaned query: {query_clean}")

        # Check if it starts with SELECT
        if not query_clean.startswith('SELECT'):
            return False
        
        # # Check for forbidden keywords that could modify data
        # forbidden_keywords = [
        #     'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 
        #     'TRUNCATE', 'GRANT', 'REVOKE', 'EXECUTE', 'CALL'
        # ]
        
        # for keyword in forbidden_keywords:
        #     if keyword in query_clean:
        #         return False
        
        print(f"Cleaned query: {query_clean}")

        return True
    
    def _get_database_credentials(self, environment: Environment) -> Dict[str, Any]:
        """
        Get database credentials for the specified environment.
        
        Args:
            environment: Target environment
            
        Returns:
            Dict containing database credentials
        """
        secret_name = ExternalAPIConfig.get_database_secret(environment)
        try:
            credentials = self.secrets_manager.get_secret(secret_name)
            if credentials is None:
                raise ValueError(f"No credentials found for secret: {secret_name}")
            return credentials
        except Exception as e:
            logger.error(f"Failed to get database credentials for {environment.value}: {e}")
            raise
    
    def execute_query(self, query: str, environment: Environment) -> Dict[str, Any]:
        """
        Execute a SELECT query on the database.
        
        Args:
            query: SQL SELECT query to execute
            environment: Target environment
            
        Returns:
            Dict containing query results and metadata
        """
        import time
        start_time = time.time()
        
        try:
            # Validate query
            if not self._validate_select_query(query):
                return {
                    "success": False,
                    "error": "Only SELECT statements are allowed. Query contains forbidden keywords or is not a SELECT statement.",
                    "data": None,
                    "row_count": 0,
                    "execution_time": time.time() - start_time
                }
            
            # Get credentials
            credentials = self._get_database_credentials(environment)
            database_name = ExternalAPIConfig.get_database_name(environment)
            
            # Add database name to credentials
            credentials['database'] = database_name
            
            # Execute query based on database type
            if credentials.get('engine') == 'mysql':
                return self._execute_mysql_query(query, credentials, start_time)
            else:
                # Default to PostgreSQL
                return self._execute_postgres_query(query, credentials, start_time)
                
        except Exception as e:
            logger.error(f"Database query execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": None,
                "row_count": 0,
                "execution_time": time.time() - start_time
            }
    
    def _execute_postgres_query(self, query: str, credentials: Dict[str, Any], start_time: float) -> Dict[str, Any]:
        """Execute PostgreSQL query."""
        import time
        
        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                host=credentials.get('host'),
                port=credentials.get('port', 5432),
                database=credentials.get('database'),
                user=credentials.get('username'),
                password=credentials.get('password')
            )
            
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                
                # Convert results to list of dictionaries
                data = [dict(row) for row in results]
                
                return {
                    "success": True,
                    "data": data,
                    "row_count": len(data),
                    "execution_time": time.time() - start_time,
                    "error": None
                }
                
        except Exception as e:
            logger.error(f"PostgreSQL query execution failed: {e}")
            return {
                "success": False,
                "error": f"PostgreSQL error: {str(e)}",
                "data": None,
                "row_count": 0,
                "execution_time": time.time() - start_time
            }
        finally:
            if 'conn' in locals():
                conn.close()
    
    def _execute_mysql_query(self, query: str, credentials: Dict[str, Any], start_time: float) -> Dict[str, Any]:
        """Execute MySQL query."""
        import time
        
        try:
            # Import MySQL connector here to avoid import errors if not installed
            import mysql.connector
            from mysql.connector import Error as MySQLError
            
            # Connect to MySQL
            conn = mysql.connector.connect(
                host=credentials.get('host'),
                port=credentials.get('port', 3306),
                database=credentials.get('database'),
                user=credentials.get('username'),
                password=credentials.get('password')
            )
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Convert results to list of dictionaries
            data = [dict(row) for row in results]
            
            return {
                "success": True,
                "data": data,
                "row_count": len(data),
                "execution_time": time.time() - start_time,
                "error": None
            }
            
        except ImportError:
            return {
                "success": False,
                "error": "MySQL connector not installed. Please install mysql-connector-python to use MySQL functionality.",
                "data": None,
                "row_count": 0,
                "execution_time": time.time() - start_time
            }
        except Exception as e:
            logger.error(f"MySQL query execution failed: {e}")
            return {
                "success": False,
                "error": f"MySQL error: {str(e)}",
                "data": None,
                "row_count": 0,
                "execution_time": time.time() - start_time
            }
        finally:
            if 'conn' in locals():
                conn.close() 