from typing import List, Protocol

from models.agent_output import AgentOutput, OrchestratorOutput


class BuilderAgent(Protocol):
    """Protocol for builder agents that accept queries and return AgentOutput."""

    def run(self, query: str) -> AgentOutput: ...


class OrchestratorAgent:
    """
    Orchestrator agent for coordinating multi-agent workflows.
    Feeds queries to builder agents and returns OrchestratorOutput with the 3 AgentOutput items.
    """

    def __init__(self, builder_agents: List[BuilderAgent]):
        if len(builder_agents) != 3:
            raise ValueError("OrchestratorAgent requires exactly 3 builder agents (1, 2, 3)")
        self.builder_agents = builder_agents

    def run(self, query: str) -> OrchestratorOutput:
        """
        Feed the query to all builder agents and return OrchestratorOutput
        containing the 3 AgentOutput items from builder agents 1, 2, 3.
        """
        outputs = [agent.run(query) for agent in self.builder_agents]
        return OrchestratorOutput(items=outputs)
