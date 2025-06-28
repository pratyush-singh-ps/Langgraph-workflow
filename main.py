from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from codebase_intelligence.orchestration.codebase_agent import CodebaseAgent

app = FastAPI(title="Codebase Intelligence API", description="API for codebase analysis using LangGraph workflows")

# Initialize codebase agent
codebase_agent = CodebaseAgent()

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
            "POST /codebase-query": "Query codebase using LangGraph workflows"
        }
    } 