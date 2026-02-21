"use client";

import { motion } from "framer-motion";
import { Trophy, CheckCircle, Download, Code } from "lucide-react";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Submission } from "@/lib/types";
import { downloadImage, downloadCode } from "@/lib/download";

interface WinnerStepProps {
  prompt: string;
  winner: Submission;
  onStartOver: () => void;
}

export function WinnerStep({ prompt, winner, onStartOver }: WinnerStepProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
      className="w-full max-w-2xl mx-auto"
    >
      <Card className="border-0 shadow-lg overflow-hidden">
        <CardHeader className="space-y-1.5 border-b bg-muted/30">
          <div className="flex items-center gap-2">
            <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10">
              <Trophy className="size-5 text-primary" />
            </div>
            <div>
              <CardTitle className="text-xl">Winner Selected</CardTitle>
              <CardDescription>
                The winning agent has the contract. Final high-res delivery is in progress.
              </CardDescription>
            </div>
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            <span className="font-medium text-foreground">Brief:</span> {prompt}
          </p>
        </CardHeader>
        <CardContent className="p-6 space-y-6">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="rounded-xl border overflow-hidden bg-card"
          >
            <div className="relative aspect-video bg-muted min-h-[200px]">
              {winner.code ? (
                <div className="absolute inset-0 overflow-hidden">
                  <iframe
                    srcDoc={winner.code}
                    title={`Winner by ${winner.agent_name ?? winner.agent_id}`}
                    sandbox="allow-scripts"
                    className="absolute top-0 left-0 w-[400%] h-[400%] border-0 origin-top-left scale-[0.25]"
                  />
                </div>
              ) : winner.asset_url ? (
                <>
                  {winner.asset_url.startsWith("data:") ? (
                    <img
                      src={winner.asset_url}
                      alt={`Winner: ${winner.agent_name ?? winner.agent_id}`}
                      className="size-full object-cover"
                    />
                  ) : (
                    <Image
                      src={winner.asset_url}
                      alt={`Winner: ${winner.agent_name ?? winner.agent_id}`}
                      fill
                      className="object-cover"
                      sizes="(max-width: 768px) 100vw, 672px"
                    />
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent pointer-events-none" />
                </>
              ) : winner.proposal_text ? (
                <div className="absolute inset-0 overflow-y-auto p-4 text-sm text-foreground">
                  <p className="whitespace-pre-wrap">{winner.proposal_text}</p>
                </div>
              ) : (
                <div className="flex size-full items-center justify-center text-muted-foreground">
                  No preview
                </div>
              )}
              <div className="absolute bottom-4 left-4 right-4 flex items-center gap-2 flex-wrap">
                <CheckCircle className="size-5 text-green-500 shrink-0" />
                <span className="font-semibold text-foreground">
                  {winner.persona ?? winner.agent_name ?? winner.agent_id}
                </span>
                {winner.score != null && (
                  <Badge variant="secondary" className="shrink-0">
                    {(winner.score * 20).toFixed(0)}/100
                  </Badge>
                )}
                <span className="text-muted-foreground text-sm">— Contract awarded</span>
              </div>
            </div>
          </motion.div>

          <div className="flex gap-2 flex-wrap">
            {winner.code && (
              <Button
                variant="outline"
                className="gap-2"
                onClick={() =>
                  downloadCode(winner.code!, winner.agent_name ?? winner.agent_id)
                }
              >
                <Code className="size-4" />
                Download HTML
              </Button>
            )}
            {winner.asset_url && !winner.code && (
              <Button
                variant="outline"
                className="gap-2"
                onClick={() =>
                  downloadImage(
                    winner.asset_url!,
                    winner.agent_name ?? winner.agent_id
                  )
                }
              >
                <Download className="size-4" />
                Download image
              </Button>
            )}
            <Button variant="outline" className="flex-1 min-w-0" onClick={onStartOver}>
              Start New Brief
            </Button>
          </div>

          <p className="text-sm text-muted-foreground text-center">
            Refinement and high-res delivery will appear here once the agent completes the work.
          </p>
        </CardContent>
      </Card>
    </motion.div>
  );
}
