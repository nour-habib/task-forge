/**
 * Mirrors FastAPI Pydantic models.
 * Keeps NestJS types in sync with the agent backend.
 */

/** Request body for POST /orchestrate (QueryRequest) */
export interface QueryRequest {
  query: string;
}

/** Response from POST /orchestrate (OrchestratorOutput) */
export interface QueryResponse {
  items: AgentOutputItem[];
  judgments: AgentJudgment[];
}

/** Single agent output (AgentOutput) */
export interface AgentOutputItem {
  image: string;
  agent_name: string;
  persona: string;
  created_at?: string;
  prompt_or_job?: string | null;
  style_notes?: string | null;
  score?: number | null;
  extra?: Record<string, unknown>;
}

/** Judge's rating for one agent (AgentJudgment) */
export interface AgentJudgment {
  agent_name: string;
  persona: string;
  criteria_ratings: Array<{ criterion: string; score: number; rationale: string }>;
  overall_score: number;
  summary: string;
}

/** Metadata for agent-generated output (AgentOutputMetadata) */
export interface AgentOutputMetadata {
  agent_name: string;
  persona: string;
  created_at: string;
  prompt_or_job?: string | null;
  style_notes?: string | null;
  extra?: Record<string, unknown>;
}

/** Agent return type: image + metadata (AgentImageOutput) */
export interface AgentImageOutput {
  image: string;
  metadata: AgentOutputMetadata;
}
