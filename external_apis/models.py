"""
Pydantic Models for External APIs

Request and response models for external API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from .config import Environment

# CCP VAP Models
class GraphEntityRequest(BaseModel):
    """Request model for getting graph entities."""
    branch_name: str = Field(..., description="Branch name")
    ccp_entity_name: str = Field(..., description="CCP entity name")
    project_name: str = Field(..., description="Project name")

class LinkStatusRequest(BaseModel):
    """Request model for getting link status."""
    project_id: str = Field(..., description="Project ID")

# CCP Execute Models
class ExecutionDetailsRequest(BaseModel):
    """Request model for getting execution details."""
    execution_id: str = Field(..., description="Execution ID")

# Database Models
class DatabaseQueryRequest(BaseModel):
    """Request model for database queries."""
    query: str = Field(..., description="SQL SELECT query to execute")
    env: Environment = Field(..., description="Target environment")

# Databricks Models
class ClientNCSDetailsRequest(BaseModel):
    """Request model for getting client NCS details."""
    client_id: str = Field(..., description="Client ID")
    env: Environment = Field(..., description="Target environment")

class JobRunDetailsRequest(BaseModel):
    """Request model for getting job run details."""
    env: Environment = Field(..., description="Target environment")
    run_id: str = Field(..., description="Job run ID")

# Response Models
class APIResponse(BaseModel):
    """Generic API response model."""
    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Response data")
    error: Optional[str] = Field(default=None, description="Error message if any")
    status_code: int = Field(..., description="HTTP status code")

class DatabaseQueryResponse(BaseModel):
    """Database query response model."""
    success: bool = Field(..., description="Whether the query was successful")
    data: Optional[List[Dict[str, Any]]] = Field(default=None, description="Query results")
    error: Optional[str] = Field(default=None, description="Error message if any")
    row_count: Optional[int] = Field(default=None, description="Number of rows returned")
    execution_time: Optional[float] = Field(default=None, description="Query execution time in seconds") 