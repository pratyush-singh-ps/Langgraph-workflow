"""
CCP Execute API Client

Client for interacting with CCP Execute APIs including execution details.
"""

import httpx
import asyncio
from typing import Dict, Any, Optional
from .config import ExternalAPIConfig, Environment
from .models import ExecutionDetailsRequest, APIResponse

class CCPExecuteClient:
    """
    Client for CCP Execute API operations.
    
    Handles:
    - Execution details retrieval
    """
    
    def __init__(self):
        """Initialize the CCP Execute client."""
        self.timeout = ExternalAPIConfig.REQUEST_TIMEOUT
        self.headers = ExternalAPIConfig.DEFAULT_HEADERS.copy()
    
    async def _make_request(self, method: str, url: str, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        """
        Make HTTP request with error handling and retries.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Full URL to request
            params: Query parameters
            
        Returns:
            APIResponse with result or error
        """
        for attempt in range(ExternalAPIConfig.MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.request(
                        method=method,
                        url=url,
                        params=params,
                        headers=self.headers
                    )
                    
                    if response.status_code == 200:
                        return APIResponse(
                            success=True,
                            data=response.json(),
                            status_code=response.status_code
                        )
                    else:
                        return APIResponse(
                            success=False,
                            error=f"HTTP {response.status_code}: {response.text}",
                            status_code=response.status_code
                        )
                        
            except httpx.TimeoutException:
                if attempt == ExternalAPIConfig.MAX_RETRIES - 1:
                    return APIResponse(
                        success=False,
                        error="Request timeout",
                        status_code=408
                    )
                await asyncio.sleep(ExternalAPIConfig.RETRY_DELAY)
                
            except Exception as e:
                return APIResponse(
                    success=False,
                    error=f"Request failed: {str(e)}",
                    status_code=500
                )
        
        return APIResponse(
            success=False,
            error="Max retries exceeded",
            status_code=500
        )
    
    async def get_execution_details(self, request: ExecutionDetailsRequest, environment: Environment = Environment.PROD) -> APIResponse:
        """
        Get execution details from CCP Execute.
        
        Args:
            request: ExecutionDetailsRequest with execution_id
            environment: Target environment (default: PROD)
            
        Returns:
            APIResponse with execution details data
        """
        url = ExternalAPIConfig.get_ccp_execute_url("execution_details", environment).format(
            execution_id=request.execution_id
        )
        
        return await self._make_request("GET", url) 