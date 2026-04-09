import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Ensures the app find
sys.path.append(str(Path(__file__).parent.parent))

from src.agent import DeepResearchWorkflow

app = FastAPI(title="Deep Research Agent API")
workflow = DeepResearchWorkflow(timeout=600) 

class TopicRequest(BaseModel):
    topic: str

# Add a Health Check
@app.get("/")
async def health_check():
    return {"status": "online", "model": "gpt-4o"}

@app.post("/research")
async def conduct_research(request: TopicRequest):
    try:
        # This invokes the LlamaIndex workflow
        result = await workflow.run(query=request.topic)
        return {"status": "success", "data": result}
    except Exception as e:
        # Prevents the 500 Internal Server Error from being generic
        print(f"Error during research: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Render provides the PORT via environment variable
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)