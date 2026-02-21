/**
 * Shared types for the multi-agent task application.
 * Aligns with backend schema: Jobs, Submissions, Feedback.
 */

export type JobStatus = "open" | "in_progress" | "completed" | "cancelled";
export type SubmissionStatus = "pending" | "won" | "lost" | "rejected";

export interface Job {
  id: string;
  user_id?: string;
  status: JobStatus;
  budget?: number;
  requirements_json: {
    prompt: string;
    [key: string]: unknown;
  };
  created_at?: string;
}

export interface Submission {
  id: string;
  job_id: string;
  agent_id: string;
  agent_name?: string;
  asset_url?: string;
  status: SubmissionStatus;
  created_at?: string;
}

export interface CreateJobRequest {
  prompt: string;
  budget?: number;
  requirements?: Record<string, unknown>;
}

export interface SelectWinnerRequest {
  job_id: string;
  submission_id: string;
}
