"""
External API Routes

FastAPI routes for external API endpoints including CCP VAP, CCP Execute, Databricks, and database operations.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
import logging
from .models import (
    GraphEntityRequest, LinkStatusRequest, ExecutionDetailsRequest,
    DatabaseQueryRequest, JobRunDetailsRequest, ClientNCSDetailsRequest,
    APIResponse, DatabaseQueryResponse
)
from .ccp_vap_client import CCPVAPClient
from .ccp_execute_client import CCPExecuteClient
from .databricks_client import DatabricksClient
from .database_client import DatabaseClient
from .generic_client import GenericClient
from .config import Environment

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/external", tags=["External APIs"])

# Initialize clients
ccp_vap_client = CCPVAPClient()
ccp_execute_client = CCPExecuteClient()
databricks_client = DatabricksClient()
database_client = DatabaseClient()
generic_client = GenericClient()

@router.post("/getGraphEntity", response_model=APIResponse)
async def get_graph_entity(request: GraphEntityRequest, env: Environment = Query(Environment.PROD, description="Target environment")) -> APIResponse:
    """Get graph entity from CCP VAP."""
    try:
        response = await ccp_vap_client.get_graph_entities(request, env)
        return response
    except Exception as e:
        logger.error(f"Error getting graph entity: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/getLinkStatus", response_model=APIResponse)
async def get_link_status(request: LinkStatusRequest, env: Environment = Query(Environment.PROD, description="Target environment")) -> APIResponse:
    """Get link status from CCP VAP."""
    try:
        response = await ccp_vap_client.get_link_status(request, env)
        return response
    except Exception as e:
        logger.error(f"Error getting link status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/getExecutionDetails", response_model=APIResponse)
async def get_execution_details(request: ExecutionDetailsRequest, env: Environment = Query(Environment.PROD, description="Target environment")) -> APIResponse:
    """Get execution details from CCP Execute."""
    try:
        response = await ccp_execute_client.get_execution_details(request, env)
        return response
    except Exception as e:
        logger.error(f"Error getting execution details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/getClientNCSDetails", response_model=APIResponse)
async def get_client_ncs_details(request: ClientNCSDetailsRequest) -> APIResponse:
    """Get client NCS details from Databricks."""
    try:
        response = await databricks_client.get_client_ncs_details(request)
        return response
    except Exception as e:
        logger.error(f"Error getting client NCS details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/executeDBQuery", response_model=DatabaseQueryResponse)
async def execute_db_query(request: DatabaseQueryRequest) -> DatabaseQueryResponse:
    """Execute a SELECT query on the database."""
    try:
        result = database_client.execute_query(request.query, request.env)
        
        return DatabaseQueryResponse(
            success=result["success"],
            data=result.get("data"),
            error=result.get("error"),
            row_count=result.get("row_count"),
            execution_time=result.get("execution_time")
        )
    except Exception as e:
        logger.error(f"Error executing database query: {e}")
        return DatabaseQueryResponse(
            success=False,
            error=str(e),
            data=None,
            row_count=0,
            execution_time=0.0
        )

@router.post("/getJobRunDetails", response_model=APIResponse)
async def get_job_run_details(request: JobRunDetailsRequest) -> APIResponse:
    """Get job run details from Databricks."""
    try:
        response = await databricks_client.get_job_run_details(request.env, request.run_id)
        return response
    except Exception as e:
        logger.error(f"Error getting job run details: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 