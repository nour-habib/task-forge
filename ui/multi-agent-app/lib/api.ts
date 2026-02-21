/**
 * Centralized API module for multi-agent task application.
 * Uses mock stubs until Nimesh's Next.js service/controller endpoints are merged.
 * Replace fetch base URL and paths when real endpoints are available.
 */

import type { Job, Submission, CreateJobRequest, SelectWinnerRequest } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3001";
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
// API functions
// ---------------------------------------------------------------------------

/**
 * Create a new job (brief).
 * POST /api/jobs or equivalent
 */
export async function createJob(req: CreateJobRequest): Promise<Job> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 800));
    return createMockJob(req.prompt);
  }
  const res = await fetch(`${API_BASE}/api/jobs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error(`createJob failed: ${res.statusText}`);
  return res.json();
}

/**
 * Get job status and details.
 * GET /api/jobs/:id
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
  const res = await fetch(`${API_BASE}/api/jobs/${jobId}`);
  if (!res.ok) throw new Error(`getJob failed: ${res.statusText}`);
  return res.json();
}

/**
 * Get submissions for a job.
 * GET /api/jobs/:id/submissions
 */
export async function getSubmissions(jobId: string): Promise<Submission[]> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 500));
    return createMockSubmissions(jobId);
  }
  const res = await fetch(`${API_BASE}/api/jobs/${jobId}/submissions`);
  if (!res.ok) throw new Error(`getSubmissions failed: ${res.statusText}`);
  return res.json();
}

/**
 * Select winner and trigger refinement.
 * POST /api/jobs/:id/winner
 */
export async function selectWinner(req: SelectWinnerRequest): Promise<{ success: boolean }> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 600));
    return { success: true };
  }
  const res = await fetch(`${API_BASE}/api/jobs/${req.job_id}/winner`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ submission_id: req.submission_id }),
  });
  if (!res.ok) throw new Error(`selectWinner failed: ${res.statusText}`);
  return res.json();
}
