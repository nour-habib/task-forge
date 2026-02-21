from typing import List, Protocol


class BuilderAgent(Protocol):
    """Protocol for builder agents that accept queries."""

    def run(self, query: str) -> str: ...

class OrchestratorAgent:
    """
    Orchestrator agent for coordinating multi-agent workflows.
    Feeds queries to builder agents and collects their responses.
    """

    def __init__(self, builder_agents: List[BuilderAgent]):
        self.builder_agents = builder_agents

    def run(self, query: str) -> dict[str, str]:
        """
        Feed the query to all builder agents and return their responses.
        Returns a dict mapping agent name to response (agents must have a .name attribute).
        """
        results = {}
        for agent in self.builder_agents:
            response = agent.run(query)
            name = getattr(agent, "name", f"agent_{id(agent)}")
            results[name] = response
        return results
