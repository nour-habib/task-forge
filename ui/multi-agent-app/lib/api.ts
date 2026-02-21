/**
 * Centralized API module for multi-agent task application.
 * - Mock mode (default): uses local stubs.
 * - Real mode (NEXT_PUBLIC_USE_MOCK=false): calls NestJS POST /build via /api/build proxy.
 */

import type { Job, Submission, CreateJobRequest, SelectWinnerRequest } from "./types";

/** Agent backend response item (AgentOutput) */
interface AgentOutputItem {
  image: string;
  agent_name: string;
  persona?: string;
  created_at?: string;
  prompt_or_job?: string | null;
  style_notes?: string | null;
}

/** Client: use /api/build (same-origin, avoids CORS). Server proxies to NestJS. */
const BUILD_URL = typeof window !== "undefined" ? "/api/build" : `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3001"}/build`;
const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK !== "false";

// ---------------------------------------------------------------------------
// Mock data for development
// ---------------------------------------------------------------------------

const MOCK_AGENTS = [
  { id: "agent-1", name: "Agent Alpha" },
  { id: "agent-2", name: "Agent Beta" },
  { id: "agent-3", name: "Agent Gamma" },
];

const MOCK_ASSETS = [
  "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=400&h=300&fit=crop",
  "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=300&fit=crop",
  "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop",
];

function createMockJob(prompt: string): Job {
  return {
    id: `job-${Date.now()}`,
    status: "open",
    requirements_json: { prompt },
    created_at: new Date().toISOString(),
  };
}

function createMockSubmissions(jobId: string): Submission[] {
  return MOCK_AGENTS.map((agent, i) => ({
    id: `sub-${jobId}-${agent.id}`,
    job_id: jobId,
    agent_id: agent.id,
    agent_name: agent.name,
    asset_url: MOCK_ASSETS[i],
    status: "pending" as const,
    created_at: new Date().toISOString(),
  }));
}

// ---------------------------------------------------------------------------
// Build cache (real backend: POST /build returns results synchronously)
// ---------------------------------------------------------------------------

const buildCache = new Map<string, Submission[]>();

// ---------------------------------------------------------------------------
// API functions
// ---------------------------------------------------------------------------

/**
 * Create a new job (brief).
 * Mock: returns synthetic job. Real: POST /build, caches agent results.
 */
export async function createJob(req: CreateJobRequest): Promise<Job> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 800));
    return createMockJob(req.prompt);
  }

  const res = await fetch(BUILD_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: req.prompt }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`createJob failed: ${res.status} ${res.statusText}${text ? ` - ${text}` : ""}`);
  }

  const data = (await res.json()) as { items?: AgentOutputItem[] };
  const items = Array.isArray(data?.items) ? data.items : [];
  const jobId = `build-${Date.now()}`;

  const submissions: Submission[] = items.map((item, i) => ({
    id: `sub-${jobId}-${item.agent_name}-${i}`,
    job_id: jobId,
    agent_id: item.agent_name,
    agent_name: item.agent_name.replace(/([A-Z])/g, " $1").trim(),
    asset_url: item.image,
    proposal_text: item.style_notes ?? undefined,
    status: "pending" as const,
    created_at: item.created_at ?? new Date().toISOString(),
  }));

  buildCache.set(jobId, submissions);

  return {
    id: jobId,
    status: "in_progress",
    requirements_json: { prompt: req.prompt },
    created_at: new Date().toISOString(),
  };
}

/**
 * Get job status and details.
 */
export async function getJob(jobId: string): Promise<Job> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 400));
    return {
      id: jobId,
      status: "in_progress",
      requirements_json: { prompt: "Minimalist logo for a coffee shop" },
      created_at: new Date().toISOString(),
    };
  }
  const cached = buildCache.get(jobId);
  if (!cached) throw new Error(`Job ${jobId} not found`);
  return {
    id: jobId,
    status: "in_progress",
    requirements_json: { prompt: "" },
    created_at: new Date().toISOString(),
  };
}

/**
 * Get submissions for a job.
 * Mock: synthetic. Real: cached from createJob.
 */
export async function getSubmissions(jobId: string): Promise<Submission[]> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 500));
    return createMockSubmissions(jobId);
  }
  return buildCache.get(jobId) ?? [];
}

/**
 * Select winner. No backend endpoint yet; returns success.
 */
export async function selectWinner(req: SelectWinnerRequest): Promise<{ success: boolean }> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 600));
    return { success: true };
  }
  return { success: true };
}
