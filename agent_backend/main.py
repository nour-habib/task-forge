import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents.builder_agent_1 import BuilderAgent1
from agents.builder_agent_2 import BuilderAgent2
from agents.builder_agent_3 import BuilderAgent3
from agents.orchestrator_agent import OrchestratorAgent

app = FastAPI()

# Initialize orchestrator with builder agents (lazy init on first request)
_orchestrator: OrchestratorAgent | None = None


def get_orchestrator() -> OrchestratorAgent:
    global _orchestrator
    if _orchestrator is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENAI_API_KEY environment variable is not set",
            )
        builders = [
            BuilderAgent1(api_key),
            BuilderAgent2(api_key),
            BuilderAgent3(api_key),
        ]
        _orchestrator = OrchestratorAgent(builders)
    return _orchestrator


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    results: dict[str, str]


@app.post("/orchestrate", response_model=QueryResponse)
def orchestrate(request: QueryRequest) -> QueryResponse:
    """Feed a query to the orchestrator agent and return responses from all builder agents."""
    orchestrator = get_orchestrator()
    results = orchestrator.run(request.query)
    return QueryResponse(results=results)
