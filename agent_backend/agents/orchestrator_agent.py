from typing import List, Protocol

from models.agent_output import AgentOutput, OrchestratorOutput
from query_analyzer import QueryAnalyzer, StructuredQuery


class BuilderAgent(Protocol):
    """Protocol for builder agents that accept StructuredQuery and return AgentOutput."""

    def run(self, structured_query: StructuredQuery) -> AgentOutput: ...


class OrchestratorAgent:
    """
    Orchestrator agent for coordinating multi-agent workflows.
    Parses the query with QueryAnalyzer, then feeds the parsed query to builder agents.
    """

    def __init__(self, builder_agents: List[BuilderAgent], query_analyzer: QueryAnalyzer):
        if len(builder_agents) != 3:
            raise ValueError("OrchestratorAgent requires exactly 3 builder agents (1, 2, 3)")
        self.builder_agents = builder_agents
        self.query_analyzer = query_analyzer

    def run(self, query: str) -> OrchestratorOutput:
        """
        Parse the query with QueryAnalyzer, then feed the parsed query to all builder agents.
        Returns OrchestratorOutput containing the 3 AgentOutput items.
        """
        parsed = self.query_analyzer.analyze(query)
        outputs = [agent.run(parsed) for agent in self.builder_agents]
        return OrchestratorOutput(items=outputs)
