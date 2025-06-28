"""
Generic HTTP Client

Generic client for making HTTP requests to external APIs.
"""

import aiohttp
import asyncio
from typing import Dict, Any, Optional
import logging
from .models import JobRunDetailsRequest, APIResponse, Environment
from .aws_secrets import secrets_manager

logger = logging.getLogger(__name__)

class GenericClient:
    """Generic HTTP client for external API interactions."""
    
    def __init__(self):
        """Initialize the generic client."""
        self.session = None
        self.timeout = 30
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self.session
    
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
    
    async def get_job_run_details(self, request: JobRunDetailsRequest) -> APIResponse:
        """
        Get job run details from any endpoint with Databricks authentication.
        
        Args:
            request: JobRunDetailsRequest with environment and endpoint URL
            
        Returns:
            APIResponse with job run details data
        """
        try:
            # Get Databricks credentials for authentication
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
            
            # Make request to the specified endpoint with Databricks authentication
            session = await self._get_session()
            
            headers = {
                "Authorization": f"Bearer {credentials['token']}",
                "Content-Type": "application/json"
            }
            
            async with session.get(request.endpoint, headers=headers) as response:
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
                        error=f"Job run details request failed: {error_text}",
                        status_code=response.status
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