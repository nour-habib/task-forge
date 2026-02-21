from typing import List, Protocol

from agents.judge_agent import JudgeAgent
from models.agent_output import AgentOutput, OrchestratorOutput
from query_analyzer import QueryAnalyzer, StructuredQuery


class BuilderAgent(Protocol):
    """Protocol for builder agents that accept StructuredQuery and return AgentOutput."""

    def run(self, structured_query: StructuredQuery) -> AgentOutput: ...


class OrchestratorAgent:
    """
    Orchestrator agent for coordinating multi-agent workflows.
    Parses the query with QueryAnalyzer, feeds the parsed query to builder agents,
    then uses JudgeAgent to judge the outputs.
    """

    def __init__(
        self,
        builder_agents: List[BuilderAgent],
        query_analyzer: QueryAnalyzer,
        judge_agent: JudgeAgent,
    ):
        if len(builder_agents) != 3:
            raise ValueError("OrchestratorAgent requires exactly 3 builder agents (1, 2, 3)")
        self.builder_agents = builder_agents
        self.query_analyzer = query_analyzer
        self.judge_agent = judge_agent

    def run(self, query: str) -> OrchestratorOutput:
        """
        Parse the query, feed to builder agents, then judge the outputs.
        Returns OrchestratorOutput with the 3 AgentOutput items and their judgments.
        """
        parsed = self.query_analyzer.analyze(query)
        outputs = [agent.run(parsed) for agent in self.builder_agents]
        prompt_or_job = parsed.to_agent_prompt()
        judge_output = self.judge_agent.judge(outputs, prompt_or_job)
        # Attach judge's score to each AgentOutput
        outputs_with_score = [
            output.model_copy(update={"score": j.overall_score})
            for output, j in zip(outputs, judge_output.judgments)
        ]
        return OrchestratorOutput(items=outputs_with_score, judgments=judge_output.judgments)
