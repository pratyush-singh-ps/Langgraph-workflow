"""
Databricks Client

Client for interacting with Databricks APIs using credentials from AWS Secrets Manager.
"""

import aiohttp
import asyncio
from typing import Dict, Any, Optional
import logging
from .models import ClientNCSDetailsRequest, APIResponse
from .aws_secrets import secrets_manager
from .config import ExternalAPIConfig, Environment

logger = logging.getLogger(__name__)

class DatabricksClient:
    """Databricks client for API interactions with AWS Secrets Manager integration."""
    
    def __init__(self):
        """Initialize the Databricks client."""
        self.session = None
        self.timeout = 30
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self.session
    
    def _get_ncs_endpoint(self, env: Environment, client_id: str) -> str:
        """
        Get NCS endpoint URL based on environment and client_id.
        
        Args:
            env: Target environment
            client_id: Client ID
            
        Returns:
            NCS endpoint URL
        """
        return ExternalAPIConfig.get_databricks_ncs_url("client_setup_status", env, client_id=client_id)
    
    def _get_databricks_credentials(self, env: Environment) -> Optional[Dict[str, Any]]:
        """
        Get Databricks credentials from AWS Secrets Manager.
        
        Args:
            env: Target environment
            
        Returns:
            Databricks credentials or None if failed
        """
        secret_name = f"databricks/{env.value}/sp_ccp"
        return secrets_manager.get_secret(secret_name)
    
    async def get_client_ncs_details(self, request: ClientNCSDetailsRequest) -> APIResponse:
        """
        Get client NCS details from Databricks.
        
        Args:
            request: ClientNCSDetailsRequest with client_id and env
            
        Returns:
            APIResponse with NCS details data
        """
        try:
            # Get NCS endpoint based on environment and client_id
            ncs_endpoint = self._get_ncs_endpoint(request.env, request.client_id)
            
            # Get Databricks credentials
            credentials = self._get_databricks_credentials(request.env)
            
            if not credentials:
                return APIResponse(
                    success=False,
                    error=f"Failed to fetch Databricks credentials for environment: {request.env.value}",
                    status_code=500
                )
            
            # Validate required fields
            if 'db_host' not in credentials or 'token' not in credentials:
                return APIResponse(
                    success=False,
                    error="Missing required Databricks credentials (db_host or token)",
                    status_code=500
                )
            
            # Make request to NCS endpoint
            session = await self._get_session()
            
            headers = {
                "Authorization": f"Bearer {credentials['token']}",
                "accept": "*/*"
            }
            
            async with session.get(ncs_endpoint, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return APIResponse(
                        success=True,
                        data=data,
                        status_code=200
                    )
                else:
                    error_text = await response.text()
                    return APIResponse(
                        success=False,
                        error=f"NCS API request failed: {error_text}",
                        status_code=response.status
                    )
                    
        except Exception as e:
            logger.error(f"Error getting client NCS details: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                status_code=500
            )
    
    async def get_job_run_details(self, env: Environment, run_id: str) -> APIResponse:
        """
        Get job run details from Databricks API.
        
        Args:
            env: Target environment
            run_id: Job run ID
            
        Returns:
            APIResponse with job run details data
        """
        try:
            logger.info(f"Getting job run details for environment: {env.value}, run_id: {run_id}")
            
            # Get Databricks credentials
            credentials = self._get_databricks_credentials(env)
            logger.info(f"Fetched credentials: {credentials}")
            
            if not credentials:
                return APIResponse(
                    success=False,
                    error=f"Failed to fetch Databricks credentials for environment: {env.value}",
                    status_code=500
                )
            
            # Validate required fields
            if 'db_host' not in credentials or 'token' not in credentials:
                return APIResponse(
                    success=False,
                    error="Missing required Databricks credentials (db_host or token)",
                    status_code=500
                )
            
            # Construct the URL using host from credentials and run_id parameter
            host = credentials['db_host']
            token = credentials['token']
            
            logger.info(f"Original host: {host}")
            logger.info(f"Token: {token[:10]}..." if len(token) > 10 else f"Token: {token}")
            
            # Ensure host has https:// protocol
            if not host.startswith('http'):
                host = f"https://{host}"
            
            # Ensure host ends with / if not already present
            if not host.endswith('/'):
                host = host + '/'
            
            url = f"{host}api/2.0/jobs/runs/get?run_id={run_id}"
            
            logger.info(f"Final URL: {url}")
            
            # Validate URL format
            if not url.startswith('http'):
                return APIResponse(
                    success=False,
                    error=f"Invalid URL format: {url}",
                    status_code=500
                )
            
            # Make request to Databricks API
            session = await self._get_session()
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            logger.info(f"Request headers: {headers}")
            
            try:
                logger.info(f"Starting request to: {url}")
                async with session.get(url, headers=headers, ssl=False) as response:
                    logger.info(f"Response status: {response.status}")
                    
                    if response.status == 200:
                        data = await response.json()
                        return APIResponse(
                            success=True,
                            data=data,
                            status_code=200
                        )
                    else:
                        error_text = await response.text()
                        logger.error(f"Databricks API request failed with status {response.status}: {error_text}")
                        return APIResponse(
                            success=False,
                            error=f"Databricks API request failed with status {response.status}: {error_text}",
                            status_code=response.status
                        )
            except aiohttp.ClientConnectorError as e:
                logger.error(f"Connection error during Databricks API request: {e}")
                return APIResponse(
                    success=False,
                    error=f"Connection error: Unable to connect to Databricks API. Please check the host URL and network connectivity.",
                    status_code=500
                )
            except aiohttp.ClientError as e:
                logger.error(f"Client error during Databricks API request: {e}")
                return APIResponse(
                    success=False,
                    error=f"Client error during Databricks API request: {str(e)}",
                    status_code=500
                )
            except Exception as e:
                logger.error(f"Unexpected error during Databricks API request: {e}")
                return APIResponse(
                    success=False,
                    error=f"Unexpected error during Databricks API request: {str(e)}",
                    status_code=500
                )
                    
        except Exception as e:
            logger.error(f"Error getting job run details: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                status_code=500
            )
    
    async def close(self):
        """Close the client session."""
        if self.session and not self.session.closed:
            await self.session.close() 