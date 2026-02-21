"use client";

import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles } from "lucide-react";
import { BriefStep } from "@/components/brief-step";
import { ShowroomStep } from "@/components/showroom-step";
import { WinnerStep } from "@/components/winner-step";
import { createJob, getSubmissions, selectWinner } from "@/lib/api";
import type { Job, Submission } from "@/lib/types";

const POLL_INTERVAL_MS = 3000;

type Step = "brief" | "showroom" | "winner";

export default function Home() {
  const [step, setStep] = useState<Step>("brief");
  const [prompt, setPrompt] = useState("");
  const [job, setJob] = useState<Job | null>(null);
  const [submissions, setSubmissions] = useState<Submission[] | null>(null);
  const [winner, setWinner] = useState<Submission | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSubmissions = useCallback(async () => {
    if (!job?.id) return;
    try {
      const data = await getSubmissions(job.id);
      setSubmissions(data);
    } catch (e) {
      console.error("fetchSubmissions", e);
    }
  }, [job?.id]);

  // Poll for submissions when in showroom
  useEffect(() => {
    if (step !== "showroom" || !job?.id) return;
    fetchSubmissions();
    const id = setInterval(fetchSubmissions, POLL_INTERVAL_MS);
    return () => clearInterval(id);
  }, [step, job?.id, fetchSubmissions]);

  const handleSubmitBrief = async (briefPrompt: string) => {
    setError(null);
    setIsSubmitting(true);
    try {
      const newJob = await createJob({ prompt: briefPrompt });
      setJob(newJob);
      setPrompt(briefPrompt);
      setStep("showroom");
      setSubmissions(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create job");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSelectWinner = async (submissionId: string) => {
    if (!job?.id) return;
    setError(null);
    try {
      await selectWinner({ job_id: job.id, submission_id: submissionId });
      const sub = submissions?.find((s) => s.id === submissionId);
      if (sub) setWinner(sub);
      setStep("winner");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to select winner");
    }
  };

  const handleStartOver = () => {
    setStep("brief");
    setJob(null);
    setSubmissions(null);
    setWinner(null);
    setPrompt("");
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted/30">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <div className="flex size-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Sparkles className="size-5" />
            </div>
            <span className="font-semibold text-lg">Task Forge</span>
          </div>
          <nav className="flex items-center gap-4 text-sm text-muted-foreground">
            <span className="hidden sm:inline">Multi-Agent Creative Studio</span>
          </nav>
        </div>
      </header>

      {/* Main content */}
      <main className="container mx-auto px-4 py-12">
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 rounded-lg border border-destructive/50 bg-destructive/10 px-4 py-3 text-sm text-destructive"
          >
            {error}
          </motion.div>
        )}

        <AnimatePresence mode="wait">
          {step === "brief" && (
            <BriefStep key="brief" onSubmit={handleSubmitBrief} isSubmitting={isSubmitting} />
          )}
          {step === "showroom" && (
            <ShowroomStep
              key="showroom"
              prompt={prompt}
              submissions={submissions}
              isLoading={submissions === null}
              onSelectWinner={handleSelectWinner}
            />
          )}
          {step === "winner" && winner && (
            <WinnerStep
              key="winner"
              prompt={prompt}
              winner={winner}
              onStartOver={handleStartOver}
            />
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
