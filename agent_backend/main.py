import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents.builder_agent_1 import BuilderAgent1
from agents.builder_agent_2 import BuilderAgent2
from agents.builder_agent_3 import BuilderAgent3
from agents.judge_agent import JudgeAgent
from agents.orchestrator_agent import OrchestratorAgent
from models.agent_output import AgentOutput, OrchestratorOutput
from query_analyzer import QueryAnalyzer

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
        query_analyzer = QueryAnalyzer(api_key)
        judge_agent = JudgeAgent(api_key)
        _orchestrator = OrchestratorAgent(builders, query_analyzer, judge_agent)
    return _orchestrator


class QueryRequest(BaseModel):
    query: str


@app.post("/orchestrate", response_model=OrchestratorOutput)
def orchestrate(request: QueryRequest) -> OrchestratorOutput:
    """Feed a query to the orchestrator agent and return outputs + judgments for NestJS."""
    orchestrator = get_orchestrator()
    return orchestrator.run(request.query)
