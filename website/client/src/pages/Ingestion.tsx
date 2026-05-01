import { useState } from "react";
import { motion } from "framer-motion";
import { trpc } from "@/lib/trpc";
import SpecLayout from "@/components/SpecLayout";
import { useAuth } from "@/_core/hooks/useAuth";
import { getLoginUrl } from "@/const";
import {
  Rss, Plus, Check, X, Archive, RefreshCw, ExternalLink,
  AlertCircle, Clock, Database, Filter, Loader2
} from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

const stagger = {
  visible: { transition: { staggerChildren: 0.05 } },
};

type StatusFilter = "all" | "unverified" | "verified" | "rejected" | "archived";
type CategoryFilter = "all" | "regulation" | "standard" | "academic" | "organization" | "sovereign_infra" | "news" | "industry";

export default function Ingestion() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("unverified");
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>("all");
  const [showAddFeed, setShowAddFeed] = useState(false);
  const [newFeed, setNewFeed] = useState({ name: "", url: "", category: "news" as string, feedType: "rss" as string });

  // tRPC queries
  const feedsQuery = trpc.feeds.list.useQuery(undefined, { enabled: isAuthenticated });
  const refsQuery = trpc.references.list.useQuery(
    {
      status: statusFilter === "all" ? undefined : statusFilter,
      category: categoryFilter === "all" ? undefined : categoryFilter,
      limit: 50,
      offset: 0,
    },
    { enabled: isAuthenticated }
  );
  const statsQuery = trpc.references.stats.useQuery(undefined, { enabled: isAuthenticated });
  const logsQuery = trpc.ingestion.logs.useQuery(undefined, { enabled: isAuthenticated });

  // Mutations
  const createFeedMutation = trpc.feeds.create.useMutation({
    onSuccess: () => {
      feedsQuery.refetch();
      setShowAddFeed(false);
      setNewFeed({ name: "", url: "", category: "news", feedType: "rss" });
    },
  });

  const reviewMutation = trpc.references.review.useMutation({
    onSuccess: () => {
      refsQuery.refetch();
      statsQuery.refetch();
    },
  });

  const deleteFeedMutation = trpc.feeds.delete.useMutation({
    onSuccess: () => feedsQuery.refetch(),
  });

  if (authLoading) {
    return (
      <SpecLayout>
        <div className="flex items-center justify-center min-h-[60vh]">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </SpecLayout>
    );
  }

  if (!isAuthenticated) {
    return (
      <SpecLayout>
        <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
          <AlertCircle className="w-12 h-12 text-muted-foreground" />
          <h2 className="text-xl font-display font-bold">Authentication Required</h2>
          <p className="text-muted-foreground text-center max-w-md">
            Sign in to access the autonomous reference ingestion dashboard and manage feeds.
          </p>
          <a
            href={getLoginUrl()}
            className="inline-flex items-center gap-2 px-6 py-3 rounded bg-primary text-primary-foreground font-medium hover:opacity-90 transition-opacity"
          >
            Sign In
          </a>
        </div>
      </SpecLayout>
    );
  }

  const stats = statsQuery.data ?? { total: 0, unverified: 0, verified: 0, rejected: 0 };

  return (
    <SpecLayout>
      

      <div className="container max-w-7xl pt-24 pb-16">
        <motion.div initial="hidden" animate="visible" variants={stagger}>
          {/* Header */}
          <motion.div variants={fadeUp} className="mb-8">
            <h1 className="text-4xl font-display font-bold mb-2">
              <span className="text-gradient-teal">Reference Ingestion</span>
            </h1>
            <p className="text-muted-foreground text-lg">
              Autonomous monitoring of regulatory feeds, academic sources, and news — with Council-approved verification workflow.
            </p>
          </motion.div>

          {/* Stats Bar */}
          <motion.div variants={fadeUp} className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
            <div className="p-4 rounded border border-border/50 bg-card/50 text-center">
              <div className="text-2xl font-display font-bold text-primary">{stats.total}</div>
              <div className="text-xs text-muted-foreground">Total References</div>
            </div>
            <div className="p-4 rounded border border-amber-500/30 bg-amber-500/5 text-center">
              <div className="text-2xl font-display font-bold text-amber-400">{stats.unverified}</div>
              <div className="text-xs text-muted-foreground">Pending Review</div>
            </div>
            <div className="p-4 rounded border border-emerald-500/30 bg-emerald-500/5 text-center">
              <div className="text-2xl font-display font-bold text-emerald-400">{stats.verified}</div>
              <div className="text-xs text-muted-foreground">Verified</div>
            </div>
            <div className="p-4 rounded border border-red-500/30 bg-red-500/5 text-center">
              <div className="text-2xl font-display font-bold text-red-400">{stats.rejected}</div>
              <div className="text-xs text-muted-foreground">Rejected</div>
            </div>
          </motion.div>

          {/* Two Column Layout */}
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Left: Feeds Panel */}
            <motion.div variants={fadeUp} className="lg:col-span-1">
              <div className="rounded border border-border/50 bg-card/30 p-4">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-display font-semibold flex items-center gap-2">
                    <Rss className="w-4 h-4 text-primary" />
                    Monitored Feeds
                  </h2>
                  <button
                    onClick={() => setShowAddFeed(!showAddFeed)}
                    className="p-1.5 rounded hover:bg-primary/10 text-primary transition-colors"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>

                {/* Add Feed Form */}
                {showAddFeed && (
                  <div className="mb-4 p-3 rounded border border-primary/30 bg-primary/5 space-y-2">
                    <input
                      type="text"
                      placeholder="Feed name"
                      value={newFeed.name}
                      onChange={(e) => setNewFeed({ ...newFeed, name: e.target.value })}
                      className="w-full px-3 py-1.5 rounded bg-background border border-border text-sm"
                    />
                    <input
                      type="url"
                      placeholder="Feed URL"
                      value={newFeed.url}
                      onChange={(e) => setNewFeed({ ...newFeed, url: e.target.value })}
                      className="w-full px-3 py-1.5 rounded bg-background border border-border text-sm"
                    />
                    <div className="flex gap-2">
                      <select
                        value={newFeed.category}
                        onChange={(e) => setNewFeed({ ...newFeed, category: e.target.value })}
                        className="flex-1 px-3 py-1.5 rounded bg-background border border-border text-sm"
                      >
                        <option value="regulation">Regulation</option>
                        <option value="standard">Standard</option>
                        <option value="academic">Academic</option>
                        <option value="news">News</option>
                        <option value="industry">Industry</option>
                        <option value="sovereign_infra">Sovereign Infra</option>
                      </select>
                      <select
                        value={newFeed.feedType}
                        onChange={(e) => setNewFeed({ ...newFeed, feedType: e.target.value })}
                        className="flex-1 px-3 py-1.5 rounded bg-background border border-border text-sm"
                      >
                        <option value="rss">RSS</option>
                        <option value="api">API</option>
                        <option value="scrape">Scrape</option>
                        <option value="manual">Manual</option>
                      </select>
                    </div>
                    <button
                      onClick={() => createFeedMutation.mutate({
                        name: newFeed.name,
                        url: newFeed.url,
                        category: newFeed.category as any,
                        feedType: newFeed.feedType as any,
                      })}
                      disabled={!newFeed.name || !newFeed.url || createFeedMutation.isPending}
                      className="w-full px-3 py-1.5 rounded bg-primary text-primary-foreground text-sm font-medium disabled:opacity-50"
                    >
                      {createFeedMutation.isPending ? "Adding..." : "Add Feed"}
                    </button>
                  </div>
                )}

                {/* Feed List */}
                <div className="space-y-2 max-h-[400px] overflow-y-auto">
                  {feedsQuery.isLoading ? (
                    <div className="flex items-center justify-center py-8">
                      <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />
                    </div>
                  ) : feedsQuery.data && feedsQuery.data.length > 0 ? (
                    feedsQuery.data.map((feed) => (
                      <div
                        key={feed.id}
                        className="flex items-center justify-between p-2 rounded border border-border/30 bg-background/50 text-sm"
                      >
                        <div className="flex-1 min-w-0">
                          <div className="font-medium truncate">{feed.name}</div>
                          <div className="text-xs text-muted-foreground flex items-center gap-2">
                            <span className={`inline-block w-1.5 h-1.5 rounded-full ${feed.enabled ? "bg-emerald-400" : "bg-red-400"}`} />
                            {feed.category} • {feed.feedType}
                          </div>
                        </div>
                        <button
                          onClick={() => deleteFeedMutation.mutate({ id: feed.id })}
                          className="p-1 rounded hover:bg-red-500/10 text-red-400 transition-colors"
                        >
                          <X className="w-3 h-3" />
                        </button>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-muted-foreground text-sm">
                      <Database className="w-8 h-8 mx-auto mb-2 opacity-50" />
                      No feeds configured yet. Add one above.
                    </div>
                  )}
                </div>

                {/* Ingestion Logs */}
                <div className="mt-6 pt-4 border-t border-border/30">
                  <h3 className="font-display font-semibold text-sm mb-3 flex items-center gap-2">
                    <Clock className="w-3.5 h-3.5 text-muted-foreground" />
                    Recent Ingestion Runs
                  </h3>
                  <div className="space-y-1.5 max-h-[200px] overflow-y-auto">
                    {logsQuery.data && logsQuery.data.length > 0 ? (
                      logsQuery.data.slice(0, 10).map((log) => (
                        <div key={log.id} className="flex items-center justify-between text-xs p-1.5 rounded bg-background/30">
                          <span className={`font-mono ${
                            log.status === "success" ? "text-emerald-400" :
                            log.status === "failed" ? "text-red-400" :
                            "text-amber-400"
                          }`}>
                            {log.status}
                          </span>
                          <span className="text-muted-foreground">
                            +{log.itemsIngested} / {log.itemsFound}
                          </span>
                          <span className="text-muted-foreground">
                            {log.startedAt ? new Date(log.startedAt).toLocaleDateString() : "—"}
                          </span>
                        </div>
                      ))
                    ) : (
                      <p className="text-xs text-muted-foreground text-center py-2">No ingestion runs yet</p>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Right: Reference Queue */}
            <motion.div variants={fadeUp} className="lg:col-span-2">
              <div className="rounded border border-border/50 bg-card/30 p-4">
                {/* Filters */}
                <div className="flex flex-wrap items-center gap-3 mb-4">
                  <div className="flex items-center gap-1">
                    <Filter className="w-3.5 h-3.5 text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">Status:</span>
                  </div>
                  {(["all", "unverified", "verified", "rejected", "archived"] as StatusFilter[]).map((s) => (
                    <button
                      key={s}
                      onClick={() => setStatusFilter(s)}
                      className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
                        statusFilter === s
                          ? "bg-primary/20 text-primary border border-primary/30"
                          : "bg-background/50 text-muted-foreground border border-border/30 hover:border-primary/20"
                      }`}
                    >
                      {s === "all" ? "All" : s.charAt(0).toUpperCase() + s.slice(1)}
                    </button>
                  ))}
                  <div className="ml-auto flex items-center gap-1">
                    <span className="text-xs text-muted-foreground">Category:</span>
                    <select
                      value={categoryFilter}
                      onChange={(e) => setCategoryFilter(e.target.value as CategoryFilter)}
                      className="px-2 py-1 rounded bg-background border border-border text-xs"
                    >
                      <option value="all">All</option>
                      <option value="regulation">Regulation</option>
                      <option value="standard">Standard</option>
                      <option value="academic">Academic</option>
                      <option value="news">News</option>
                      <option value="industry">Industry</option>
                      <option value="sovereign_infra">Sovereign Infra</option>
                    </select>
                  </div>
                </div>

                {/* Reference List */}
                <div className="space-y-2 max-h-[600px] overflow-y-auto">
                  {refsQuery.isLoading ? (
                    <div className="flex items-center justify-center py-12">
                      <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
                    </div>
                  ) : refsQuery.data && refsQuery.data.items.length > 0 ? (
                    refsQuery.data.items.map((ref) => (
                      <div
                        key={ref.id}
                        className="p-3 rounded border border-border/30 bg-background/50 hover:border-primary/20 transition-colors"
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                              <h3 className="font-medium text-sm truncate">{ref.title}</h3>
                              {ref.relevanceScore && (
                                <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                                  ref.relevanceScore >= 80 ? "bg-emerald-500/10 text-emerald-400" :
                                  ref.relevanceScore >= 50 ? "bg-amber-500/10 text-amber-400" :
                                  "bg-muted text-muted-foreground"
                                }`}>
                                  {ref.relevanceScore}%
                                </span>
                              )}
                            </div>
                            {ref.summary && (
                              <p className="text-xs text-muted-foreground line-clamp-2 mb-1.5">{ref.summary}</p>
                            )}
                            <div className="flex flex-wrap items-center gap-2 text-[10px]">
                              {ref.source && (
                                <span className="px-1.5 py-0.5 rounded bg-muted/50 text-muted-foreground">{ref.source}</span>
                              )}
                              <span className="px-1.5 py-0.5 rounded bg-primary/10 text-primary">{ref.category}</span>
                              {ref.vipElements && (ref.vipElements as string[]).map((vip) => (
                                <span key={vip} className="px-1.5 py-0.5 rounded bg-accent/10 text-accent">{vip}</span>
                              ))}
                              {ref.dialectOverlay && (
                                <span className="px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-400">{ref.dialectOverlay}</span>
                              )}
                            </div>
                          </div>

                          {/* Actions */}
                          <div className="flex items-center gap-1 shrink-0">
                            <a
                              href={ref.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="p-1.5 rounded hover:bg-primary/10 text-muted-foreground hover:text-primary transition-colors"
                            >
                              <ExternalLink className="w-3.5 h-3.5" />
                            </a>
                            {ref.status === "unverified" && (
                              <>
                                <button
                                  onClick={() => reviewMutation.mutate({ id: ref.id, status: "verified" })}
                                  className="p-1.5 rounded hover:bg-emerald-500/10 text-muted-foreground hover:text-emerald-400 transition-colors"
                                  title="Verify"
                                >
                                  <Check className="w-3.5 h-3.5" />
                                </button>
                                <button
                                  onClick={() => reviewMutation.mutate({ id: ref.id, status: "rejected" })}
                                  className="p-1.5 rounded hover:bg-red-500/10 text-muted-foreground hover:text-red-400 transition-colors"
                                  title="Reject"
                                >
                                  <X className="w-3.5 h-3.5" />
                                </button>
                                <button
                                  onClick={() => reviewMutation.mutate({ id: ref.id, status: "archived" })}
                                  className="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
                                  title="Archive"
                                >
                                  <Archive className="w-3.5 h-3.5" />
                                </button>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-12 text-muted-foreground">
                      <RefreshCw className="w-10 h-10 mx-auto mb-3 opacity-30" />
                      <p className="text-sm font-medium mb-1">No references found</p>
                      <p className="text-xs">
                        {statusFilter === "unverified"
                          ? "No pending references to review. The ingestion pipeline will populate this queue automatically."
                          : "Try adjusting your filters."}
                      </p>
                    </div>
                  )}
                </div>

                {/* Pagination info */}
                {refsQuery.data && refsQuery.data.total > 0 && (
                  <div className="mt-4 pt-3 border-t border-border/30 text-xs text-muted-foreground text-center">
                    Showing {Math.min(50, refsQuery.data.items.length)} of {refsQuery.data.total} references
                  </div>
                )}
              </div>
            </motion.div>
          </div>

          {/* How It Works */}
          <motion.div variants={fadeUp} className="mt-12">
            <h2 className="text-2xl font-display font-bold mb-4">How Autonomous Ingestion Works</h2>
            <div className="substrate-line mb-6" />
            <div className="grid sm:grid-cols-3 gap-4">
              <div className="p-4 rounded border border-border/50 bg-card/30">
                <div className="text-primary font-mono text-xs mb-2">01 — DISCOVERY</div>
                <h3 className="font-display font-semibold text-sm mb-2">Scheduled Agent Monitors</h3>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  A Manus scheduled task runs periodically, researching regulatory feeds, academic databases,
                  and news sources relevant to the ontology's VIP Elements and dialect overlays.
                </p>
              </div>
              <div className="p-4 rounded border border-border/50 bg-card/30">
                <div className="text-primary font-mono text-xs mb-2">02 — CLASSIFICATION</div>
                <h3 className="font-display font-semibold text-sm mb-2">LLM-Powered Triage</h3>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Each discovered reference is analyzed for relevance, mapped to VIP Elements and House/Sphere
                  addresses, scored 0-100, and tagged with dialect overlays. All entries start as "unverified."
                </p>
              </div>
              <div className="p-4 rounded border border-border/50 bg-card/30">
                <div className="text-primary font-mono text-xs mb-2">03 — VERIFICATION</div>
                <h3 className="font-display font-semibold text-sm mb-2">Council Approval Queue</h3>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Unverified references appear in this dashboard for human review. Verified entries are
                  promoted to the canonical Knowledge Base. Rejected entries are archived with notes.
                </p>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </SpecLayout>
  );
}
