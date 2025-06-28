"""
Configuration for External APIs

Centralized configuration for all external API endpoints, credentials, and settings.
"""

import os
from typing import Dict, Any
from enum import Enum

class Environment(Enum):
    """Environment enumeration."""
    QA = "qa"
    BETA = "beta"
    PROD = "prod"

class ExternalAPIConfig:
    """Configuration class for external APIs."""
    
    # CCP VAP API Configuration - Environment-specific URLs
    CCP_VAP_URLS = {
        Environment.QA: "http://ccp-vap-qa.commerceiq.ai",
        Environment.BETA: "http://ccp-vap-beta.commerceiq.ai",
        Environment.PROD: "http://ccp-vap.commerceiq.ai"
    }
    
    CCP_VAP_ENDPOINTS = {
        "entities": "/ccp/project/entities",
        "status": "/ccp/project/status"
    }
    
    # CCP Execute API Configuration - Environment-specific URLs
    CCP_EXECUTE_URLS = {
        Environment.QA: "http://ccp-execute-qa.commerceiq.ai",
        Environment.BETA: "http://ccp-execute-beta.commerceiq.ai",
        Environment.PROD: "http://ccp-execute.commerceiq.ai"
    }
    
    CCP_EXECUTE_ENDPOINTS = {
        "execution_details": "/ccp/execute/{execution_id}/details"
    }
    
    # Databricks NCS API Configuration - Environment-specific URLs
    DATABRICKS_NCS_URLS = {
        Environment.QA: "http://databricks-ncs.qa-dbx.commerceiq.ai",
        Environment.BETA: "http://databricks-ncs.beta-dbx.commerceiq.ai",
        Environment.PROD: "http://databricks-ncs.prod-dbx.commerceiq.ai"
    }
    
    DATABRICKS_ENDPOINTS = {
        "service_principal_status": "/servicePrincipal/v1/status/sp_ccp",
        "client_details": "/client/details",
        "client_setup_status": "/clientSetup/v1/status/{client_id}"
    }
    
    # Database Configuration - CCP Database Secrets
    DATABASE_SECRETS = {
        Environment.QA: "rds/beta/ccp-beta-psql",
        Environment.BETA: "rds/beta/ccp-beta-psql", 
        Environment.PROD: "rds/prod/ccp-prod-psql"
    }
    
    DATABASE_NAMES = {
        Environment.QA: "ccp_qa",
        Environment.BETA: "ccp_beta",
        Environment.PROD: "ccp_prod"
    }
    
    # Request Configuration
    REQUEST_TIMEOUT = 30  # seconds
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    
    # Headers
    DEFAULT_HEADERS = {
        "accept": "*/*",
        "Content-Type": "application/json"
    }
    
    @classmethod
    def get_ccp_vap_url(cls, endpoint: str, environment: Environment = Environment.PROD) -> str:
        """Get full CCP VAP URL for given endpoint and environment."""
        base_url = cls.CCP_VAP_URLS.get(environment, cls.CCP_VAP_URLS[Environment.PROD])
        return f"{base_url}{cls.CCP_VAP_ENDPOINTS.get(endpoint, endpoint)}"
    
    @classmethod
    def get_ccp_execute_url(cls, endpoint: str, environment: Environment = Environment.PROD) -> str:
        """Get full CCP Execute URL for given endpoint and environment."""
        base_url = cls.CCP_EXECUTE_URLS.get(environment, cls.CCP_EXECUTE_URLS[Environment.PROD])
        return f"{base_url}{cls.CCP_EXECUTE_ENDPOINTS.get(endpoint, endpoint)}"
    
    @classmethod
    def get_databricks_ncs_url(cls, endpoint: str, environment: Environment = Environment.PROD, **kwargs) -> str:
        """Get full Databricks NCS URL for given endpoint and environment."""
        base_url = cls.DATABRICKS_NCS_URLS.get(environment, cls.DATABRICKS_NCS_URLS[Environment.PROD])
        endpoint_template = cls.DATABRICKS_ENDPOINTS.get(endpoint, endpoint)
        return f"{base_url}{endpoint_template.format(**kwargs)}"
    
    @classmethod
    def get_database_secret(cls, environment: Environment) -> str:
        """Get database secret for given environment."""
        return cls.DATABASE_SECRETS.get(environment, "")
    
    @classmethod
    def get_database_name(cls, environment: Environment) -> str:
        """Get database name for given environment."""
        return cls.DATABASE_NAMES.get(environment, "") 