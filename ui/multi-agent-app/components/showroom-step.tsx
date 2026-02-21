"use client";

import { motion } from "framer-motion";
import { LayoutGrid, Loader2, Download, Code } from "lucide-react";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import type { Submission } from "@/lib/types";
import { downloadImage, downloadCode } from "@/lib/download";

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
  const agentName = submission.agent_name ?? submission.agent_id;
  const hasCode = !!submission.code;
  const hasImage = !!submission.asset_url && !hasCode;

  return (
    <motion.div
      whileHover={{ y: -4 }}
      className="group rounded-xl border bg-card overflow-hidden shadow-sm transition-shadow hover:shadow-md"
    >
      <div className="relative aspect-[4/3] bg-muted overflow-hidden">
        {hasCode ? (
          <div className="absolute inset-0 overflow-hidden">
            <iframe
              srcDoc={submission.code}
              title={`Preview by ${agentName}`}
              sandbox="allow-scripts"
              className="absolute top-0 left-0 w-[400%] h-[400%] border-0 origin-top-left scale-[0.25]"
            />
          </div>
        ) : submission.asset_url ? (
          submission.asset_url.startsWith("data:") ? (
            <img
              src={submission.asset_url}
              alt={`Proposal by ${agentName}`}
              className="size-full object-cover transition-transform group-hover:scale-[1.02]"
            />
          ) : (
            <Image
              src={submission.asset_url}
              alt={`Proposal by ${agentName}`}
              fill
              className="object-cover transition-transform group-hover:scale-[1.02]"
              sizes="(max-width: 768px) 100vw, 33vw"
            />
          )
        ) : submission.proposal_text ? (
          <div className="absolute inset-0 overflow-y-auto p-4 text-sm text-foreground">
            <p className="whitespace-pre-wrap">{submission.proposal_text}</p>
          </div>
        ) : (
          <div className="flex size-full items-center justify-center text-muted-foreground">
            No preview
          </div>
        )}
        <div className="absolute top-3 left-3 right-3 flex items-start justify-between gap-2">
          <Badge variant="secondary" className="bg-background/90 backdrop-blur-sm shrink-0">
            {agentName}
          </Badge>
          {submission.score != null && (
            <Badge variant="outline" className="bg-background/90 backdrop-blur-sm shrink-0">
              {(submission.score * 20).toFixed(0)}/100
            </Badge>
          )}
        </div>
      </div>
      <div className="p-4 space-y-3">
        <p className="text-sm text-muted-foreground line-clamp-2">
          {submission.persona ?? agentName} • {hasCode ? "Code" : "Proposal"}
        </p>
        <div className="flex gap-2 flex-wrap">
          {hasCode && (
            <Button
              variant="outline"
              size="sm"
              className="gap-1.5 shrink-0"
              onClick={() => downloadCode(submission.code!, agentName)}
            >
              <Code className="size-4" />
              Download HTML
            </Button>
          )}
          {hasImage && (
            <Button
              variant="outline"
              size="sm"
              className="gap-1.5 shrink-0"
              onClick={() => downloadImage(submission.asset_url!, agentName)}
            >
              <Download className="size-4" />
              Download
            </Button>
          )}
          <Button onClick={onSelect} className="flex-1 min-w-0" size="sm">
            Select as Winner
          </Button>
        </div>
      </div>
    </motion.div>
  );
}
