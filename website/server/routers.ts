import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, protectedProcedure, adminProcedure, router } from "./_core/trpc";
import { z } from "zod";
import {
  listFeeds, createFeed, updateFeed, deleteFeed,
  listReferences, createReference, createReferences, updateReferenceStatus, getReferenceStats, checkDuplicateReference,
  listIngestionLogs, createIngestionLog, updateIngestionLog,
} from "./db";

export const appRouter = router({
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return { success: true } as const;
    }),
  }),

  // ==================== FEEDS ====================
  feeds: router({
    list: protectedProcedure.query(async () => {
      return listFeeds();
    }),

    create: protectedProcedure
      .input(z.object({
        name: z.string().min(1),
        url: z.string().url(),
        feedType: z.enum(["rss", "api", "scrape", "manual"]).default("rss"),
        category: z.enum(["regulation", "standard", "academic", "organization", "sovereign_infra", "news", "industry"]).default("news"),
        vipElements: z.array(z.string()).optional(),
        dialectOverlay: z.string().optional(),
        checkIntervalMinutes: z.number().min(60).default(360),
      }))
      .mutation(async ({ input }) => {
        const id = await createFeed(input);
        return { id };
      }),

    update: protectedProcedure
      .input(z.object({
        id: z.number(),
        name: z.string().optional(),
        url: z.string().url().optional(),
        enabled: z.boolean().optional(),
        checkIntervalMinutes: z.number().min(60).optional(),
        category: z.enum(["regulation", "standard", "academic", "organization", "sovereign_infra", "news", "industry"]).optional(),
        vipElements: z.array(z.string()).optional(),
        dialectOverlay: z.string().optional(),
      }))
      .mutation(async ({ input }) => {
        const { id, ...data } = input;
        await updateFeed(id, data);
        return { success: true };
      }),

    delete: protectedProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input }) => {
        await deleteFeed(input.id);
        return { success: true };
      }),
  }),

  // ==================== REFERENCES ====================
  references: router({
    list: protectedProcedure
      .input(z.object({
        status: z.string().optional(),
        category: z.string().optional(),
        limit: z.number().min(1).max(100).default(50),
        offset: z.number().min(0).default(0),
      }).optional())
      .query(async ({ input }) => {
        return listReferences(input);
      }),

    stats: protectedProcedure.query(async () => {
      return getReferenceStats();
    }),

    review: protectedProcedure
      .input(z.object({
        id: z.number(),
        status: z.enum(["verified", "rejected", "archived"]),
        reviewNotes: z.string().optional(),
      }))
      .mutation(async ({ input, ctx }) => {
        if (!ctx.user) throw new Error("Not authenticated");
        await updateReferenceStatus(input.id, input.status, ctx.user.id, input.reviewNotes);
        return { success: true };
      }),
  }),

  // ==================== INGESTION LOGS ====================
  ingestion: router({
    logs: protectedProcedure.query(async () => {
      return listIngestionLogs(50);
    }),
  }),

  // ==================== EDITORIAL PASSES ====================
  editorial: router({
    /** Submit an editorial pass from an LLM council member (e.g., Gemini S2) */
    submit: protectedProcedure
      .input(z.object({
        modelId: z.string().min(1), // e.g., "gemini-s2", "claude-s2", "deepseek-r1"
        passType: z.enum(["grammar", "factual", "structural", "constitutional", "ontological"]),
        targetType: z.enum(["doctrine", "sphere", "invariant", "module", "vip_element", "general"]),
        targetId: z.string().optional(), // e.g., "DOC-097a", "S-042", "INV-7c"
        findings: z.array(z.object({
          severity: z.enum(["critical", "major", "minor", "suggestion"]),
          location: z.string(), // where in the target the finding applies
          original: z.string().optional(), // original text if applicable
          suggested: z.string().optional(), // suggested replacement
          rationale: z.string(), // why this change is needed
          invariantsAffected: z.array(z.string()).optional(), // e.g., ["INV-1", "INV-7c"]
        })),
        summary: z.string(), // brief summary of the pass
        confidence: z.number().min(0).max(100), // model confidence in findings
        metadata: z.object({
          modelVersion: z.string().optional(),
          tokensUsed: z.number().optional(),
          timestamp: z.string().optional(),
          dialectContext: z.string().optional(),
        }).optional(),
      }))
      .mutation(async ({ input, ctx }) => {
        if (!ctx.user) throw new Error("Not authenticated");

        // Validate provenance: log who submitted and when
        const passRecord = {
          ...input,
          submittedBy: ctx.user.id,
          submittedAt: new Date().toISOString(),
          status: "pending_review" as const,
          provenanceHash: generateProvenanceHash(input),
        };

        // For now, store as a reference with editorial metadata
        // In production, this would go to a dedicated editorial_passes table
        const refId = await createReference({
          title: `[Editorial Pass] ${input.modelId} — ${input.passType} — ${input.targetId ?? 'general'}`,
          url: `internal://editorial/${input.modelId}/${Date.now()}`,
          summary: input.summary,
          source: input.modelId,
          category: "academic" as any,
          status: "unverified",
          relevanceScore: input.confidence,
          vipElements: input.findings.flatMap(f => f.invariantsAffected ?? []),
          metadata: passRecord as any,
        });

        return {
          success: true,
          passId: refId,
          provenanceHash: passRecord.provenanceHash,
          message: `Editorial pass from ${input.modelId} recorded. ${input.findings.length} findings pending review.`,
        };
      }),

    /** List editorial passes (filtered by model or type) */
    list: protectedProcedure
      .input(z.object({
        modelId: z.string().optional(),
        passType: z.string().optional(),
        limit: z.number().min(1).max(100).default(20),
      }).optional())
      .query(async ({ input }) => {
        // Filter references that are editorial passes
        const result = await listReferences({
          category: "academic",
          limit: input?.limit ?? 20,
          offset: 0,
        });
        // Filter to only editorial passes
        const editorialPasses = result.items.filter(r =>
          r.url.startsWith("internal://editorial/")
        );
        return { items: editorialPasses, total: editorialPasses.length };
      }),
  }),
});

/** Generate a provenance hash for an editorial pass (INV-17 compliance) */
function generateProvenanceHash(input: any): string {
  const content = JSON.stringify({
    modelId: input.modelId,
    passType: input.passType,
    targetId: input.targetId,
    findingsCount: input.findings.length,
    timestamp: Date.now(),
  });
  // Simple hash for now — in production use SHA-256
  let hash = 0;
  for (let i = 0; i < content.length; i++) {
    const char = content.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0;
  }
  return `prov_${Math.abs(hash).toString(36)}_${Date.now().toString(36)}`;
}

export type AppRouter = typeof appRouter;
