"use client";

import { motion } from "framer-motion";
import { LayoutGrid, Loader2 } from "lucide-react";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import type { Submission } from "@/lib/types";

interface ShowroomStepProps {
  prompt: string;
  submissions: Submission[] | null;
  isLoading: boolean;
  onSelectWinner: (submissionId: string) => void;
}

export function ShowroomStep({
  prompt,
  submissions,
  isLoading,
  onSelectWinner,
}: ShowroomStepProps) {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.08 },
    },
  };

  const item = {
    hidden: { opacity: 0, y: 16 },
    show: { opacity: 1, y: 0 },
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="w-full max-w-6xl mx-auto"
    >
      <Card className="border-0 shadow-lg overflow-hidden">
        <CardHeader className="space-y-1.5 border-b bg-muted/30">
          <div className="flex items-center gap-2">
            <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10">
              <LayoutGrid className="size-5 text-primary" />
            </div>
            <div>
              <CardTitle className="text-xl">The Showroom</CardTitle>
              <CardDescription>
                Review proposals side-by-side. Pick your favorite to proceed to refinement.
              </CardDescription>
            </div>
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            <span className="font-medium text-foreground">Brief:</span> {prompt}
          </p>
        </CardHeader>
        <CardContent className="p-6">
          {isLoading && submissions === null ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="aspect-[4/3] rounded-lg" />
              ))}
            </div>
          ) : submissions && submissions.length > 0 ? (
            <motion.div
              variants={container}
              initial="hidden"
              animate="show"
              className="grid grid-cols-1 md:grid-cols-3 gap-6"
            >
              {submissions.map((sub) => (
                <motion.div key={sub.id} variants={item}>
                  <ProposalCard submission={sub} onSelect={() => onSelectWinner(sub.id)} />
                </motion.div>
              ))}
            </motion.div>
          ) : (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <Loader2 className="size-12 animate-spin text-muted-foreground mb-4" />
              <p className="text-muted-foreground">Agents are generating proposals...</p>
              <p className="text-sm text-muted-foreground mt-1">
                This usually takes 30–60 seconds. We&apos;ll refresh automatically.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}

function ProposalCard({
  submission,
  onSelect,
}: {
  submission: Submission;
  onSelect: () => void;
}) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
      className="group rounded-xl border bg-card overflow-hidden shadow-sm transition-shadow hover:shadow-md"
    >
      <div className="relative aspect-[4/3] bg-muted overflow-hidden">
        {submission.asset_url ? (
          <Image
            src={submission.asset_url}
            alt={`Proposal by ${submission.agent_name ?? submission.agent_id}`}
            fill
            className="object-cover transition-transform group-hover:scale-[1.02]"
            sizes="(max-width: 768px) 100vw, 33vw"
          />
        ) : (
          <div className="flex size-full items-center justify-center text-muted-foreground">
            No preview
          </div>
        )}
        <Badge
          variant="secondary"
          className="absolute top-3 left-3 bg-background/90 backdrop-blur-sm"
        >
          {submission.agent_name ?? submission.agent_id}
        </Badge>
      </div>
      <div className="p-4 space-y-3">
        <p className="text-sm text-muted-foreground line-clamp-2">
          {submission.agent_name ?? submission.agent_id} • Proposal
        </p>
        <Button onClick={onSelect} className="w-full" size="sm">
          Select as Winner
        </Button>
      </div>
    </motion.div>
  );
}
