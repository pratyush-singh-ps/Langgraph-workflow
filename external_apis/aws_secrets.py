"""
AWS Secrets Manager Utility

Utility functions for fetching secrets from AWS Secrets Manager.
"""

import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AWSSecretsManager:
    """AWS Secrets Manager client for fetching secrets."""
    
    def __init__(self, region_name: str = "us-west-2"):
        """
        Initialize AWS Secrets Manager client.
        
        Args:
            region_name: AWS region name
        """
        try:
            self.client = boto3.client('secretsmanager', region_name=region_name)
            logger.info("AWS Secrets Manager client initialized successfully")
        except NoCredentialsError:
            logger.warning("AWS credentials not found. Using mock client for development.")
            self.client = None
        except Exception as e:
            logger.warning(f"Failed to initialize AWS Secrets Manager client: {e}. Using mock client.")
            self.client = None
    
    def get_secret(self, secret_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a secret from AWS Secrets Manager.
        
        Args:
            secret_name: Name of the secret to fetch
            
        Returns:
            Dictionary containing the secret values or None if failed
        """
        if not self.client:
            logger.info(f"Using mock secret for: {secret_name}")
            return self._get_mock_secret(secret_name)
        
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            
            if 'SecretString' in response:
                secret = json.loads(response['SecretString'])
                logger.info(f"Successfully fetched secret from AWS: {secret_name}")
                return secret
            else:
                logger.warning(f"Secret '{secret_name}' not found in AWS, using mock")
                return self._get_mock_secret(secret_name)
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                logger.warning(f"Secret '{secret_name}' not found in AWS, using mock")
                return self._get_mock_secret(secret_name)
            else:
                logger.error(f"AWS Secrets Manager error for '{secret_name}': {error_code}")
                logger.info(f"Falling back to mock secret for: {secret_name}")
                return self._get_mock_secret(secret_name)
        except Exception as e:
            logger.error(f"Unexpected error fetching secret '{secret_name}' from AWS: {e}")
            logger.info(f"Falling back to mock secret for: {secret_name}")
            return self._get_mock_secret(secret_name)
    
    def _get_mock_secret(self, secret_name: str) -> Optional[Dict[str, Any]]:
        """
        Return mock secrets for development/testing.
        
        Args:
            secret_name: Name of the secret
            
        Returns:
            Mock secret data
        """
        mock_secrets = {
            "database/qa/credentials": {
                "username": "qa_user",
                "password": "qa_password",
                "engine": "postgresql",
                "host": "qa-db.example.com",
                "port": 5432,
                "dbInstanceIdentifier": "qa-db-instance"
            },
            "database/beta/credentials": {
                "username": "beta_user",
                "password": "beta_password",
                "engine": "postgresql",
                "host": "beta-db.example.com",
                "port": 5432,
                "dbInstanceIdentifier": "beta-db-instance"
            },
            "database/prod/credentials": {
                "username": "prod_user",
                "password": "prod_password",
                "engine": "postgresql",
                "host": "prod-db.example.com",
                "port": 5432,
                "dbInstanceIdentifier": "prod-db-instance"
            },
            "databricks/qa/sp_ccp": {
                "db_host": "https://dbc-b3e2823d-6d7a.cloud.databricks.com",
                "token": "qa_databricks_token"
            },
            "databricks/beta/sp_ccp": {
                "db_host": "https://dbc-bdecc1d6-b083.cloud.databricks.com",
                "token": "beta_databricks_token"
            },
            "databricks/prod/sp_ccp": {
                "db_host": "https://dbc-prod-workspace.cloud.databricks.com",
                "token": "prod_databricks_token"
            }
        }
        
        logger.info(f"Mock secret requested: {secret_name}")
        secret = mock_secrets.get(secret_name, None)
        if secret:
            logger.info(f"Returning mock secret for {secret_name}: {secret}")
        else:
            logger.warning(f"No mock secret found for: {secret_name}")
        
        return secret

# Global instance
secrets_manager = AWSSecretsManager() 