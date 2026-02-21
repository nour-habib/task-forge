"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { FileText, Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

interface BriefStepProps {
  onSubmit: (prompt: string) => void;
  isSubmitting?: boolean;
}

export function BriefStep({ onSubmit, isSubmitting = false }: BriefStepProps) {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) onSubmit(prompt.trim());
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="w-full max-w-2xl mx-auto"
    >
      <Card className="border-0 shadow-lg">
        <CardHeader className="space-y-1.5">
          <div className="flex items-center gap-2">
            <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10">
              <FileText className="size-5 text-primary" />
            </div>
            <div>
              <CardTitle className="text-xl">The Brief</CardTitle>
              <CardDescription>
                Describe what you need. Our agents will compete to deliver the best result.
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Textarea
              placeholder="e.g., Minimalist logo for a coffee shop — or: Build a simple landing page (generates code)"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="min-h-[140px] resize-none text-base"
              disabled={isSubmitting}
            />
            <Button
              type="submit"
              size="lg"
              disabled={!prompt.trim() || isSubmitting}
              className="w-full sm:w-auto"
            >
              {isSubmitting ? (
                <>
                  <span className="size-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                  Submitting...
                </>
              ) : (
                <>
                  <Send className="size-4" />
                  Launch Competition
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </motion.div>
  );
}
