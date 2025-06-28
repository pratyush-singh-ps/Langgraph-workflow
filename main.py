from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from codebase_intelligence.orchestration.codebase_agent import CodebaseAgent
from external_apis.routes import router as external_router

app = FastAPI(title="Codebase Intelligence API", description="API for codebase analysis using LangGraph workflows")

# Initialize codebase agent
codebase_agent = CodebaseAgent()

# Include external API routes
app.include_router(external_router)

class CodebaseQueryRequest(BaseModel):
    query: str
    codebase: str = "both"  # "ccp-vap", "ccp-execute", or "both"

@app.post("/codebase-query")
async def query_codebase(request: CodebaseQueryRequest):
    """
    Query the codebase using LangGraph workflows.
    
    Args:
        request: Contains query and codebase preference
        
    Returns:
        AI-generated response based on codebase analysis
    """
    try:
        response = codebase_agent.query_codebase(request.query, request.codebase)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "Codebase Intelligence API is running!",
        "endpoints": {
            "POST /codebase-query": "Query codebase using LangGraph workflows",
            "GET /external/getGraphEntity": "Get graph entities from CCP VAP",
            "GET /external/getLinkStatus/{project_id}": "Get link status from CCP VAP",
            "GET /external/getExecutionDetails/{execution_id}": "Get execution details from CCP Execute",
            "GET /external/getClientNCSDetails": "Get client NCS details from Databricks",
            "POST /external/executeDBQuery": "Execute database query",
            "POST /external/getJobRunDetails": "Get job run details from any endpoint"
        }
    } 