/**
 * Mirrors FastAPI Pydantic models.
 * Keeps NestJS types in sync with the agent backend.
 */

/** Request body for POST /orchestrate (QueryRequest) */
export interface QueryRequest {
  query: string;
}

/** Response from POST /orchestrate (QueryResponse) */
export interface QueryResponse {
  results: Record<string, string>;
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
