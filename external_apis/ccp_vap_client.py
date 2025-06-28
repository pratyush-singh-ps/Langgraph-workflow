"""
CCP VAP API Client

Client for interacting with CCP VAP APIs including graph entities and link status.
"""

import httpx
import asyncio
from typing import Dict, Any, Optional
from .config import ExternalAPIConfig, Environment
from .models import GraphEntityRequest, LinkStatusRequest, APIResponse

class CCPVAPClient:
    """
    Client for CCP VAP API operations.
    
    Handles:
    - Graph entity retrieval
    - Link status checking
    """
    
    def __init__(self):
        """Initialize the CCP VAP client."""
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
    
    async def get_graph_entities(self, request: GraphEntityRequest, environment: Environment = Environment.PROD) -> APIResponse:
        """
        Get graph entities from CCP VAP.
        
        Args:
            request: GraphEntityRequest with branch_name, ccp_entity_name, project_name
            environment: Target environment (default: PROD)
            
        Returns:
            APIResponse with graph entities data
        """
        url = ExternalAPIConfig.get_ccp_vap_url("entities", environment)
        params = {
            "branchName": request.branch_name,
            "ccpEntityName": request.ccp_entity_name,
            "projectName": request.project_name
        }
        
        return await self._make_request("GET", url, params)
    
    async def get_link_status(self, request: LinkStatusRequest, environment: Environment = Environment.PROD) -> APIResponse:
        """
        Get link status from CCP VAP.
        
        Args:
            request: LinkStatusRequest with project_id
            environment: Target environment (default: PROD)
            
        Returns:
            APIResponse with link status data
        """
        url = f"{ExternalAPIConfig.get_ccp_vap_url('status', environment)}/{request.project_id}"
        
        return await self._make_request("GET", url) 