// Global Search — Cmd+K command palette for searching across all content types
import { useState, useEffect, useCallback, useRef } from "react";
import { useLocation } from "wouter";
import { Search, X, Layers, Zap, Shield, BookOpen, Users, Globe, Database, BarChart3 } from "lucide-react";
import {
  houses,
  vipElements,
  invariants,
  doctrines,
  councilSeats,
  routingModules,
  marketPlayers,
} from "@/lib/data";

interface SearchResult {
  id: string;
  title: string;
  subtitle: string;
  category: "house" | "sphere" | "vip" | "invariant" | "doctrine" | "council" | "module" | "dialect" | "market";
  href: string;
}

const categoryMeta: Record<string, { icon: typeof Search; color: string; label: string }> = {
  house: { icon: Layers, color: "text-primary", label: "House" },
  sphere: { icon: Layers, color: "text-cyan-400", label: "Sphere" },
  vip: { icon: Zap, color: "text-amber-400", label: "VIP Element" },
  invariant: { icon: Shield, color: "text-red-400", label: "Invariant" },
  doctrine: { icon: BookOpen, color: "text-blue-400", label: "Doctrine" },
  council: { icon: Users, color: "text-purple-400", label: "Council" },
  module: { icon: Database, color: "text-emerald-400", label: "Module" },
  dialect: { icon: Globe, color: "text-teal-400", label: "Dialect" },
  market: { icon: BarChart3, color: "text-yellow-400", label: "Market" },
};

function buildSearchIndex(): SearchResult[] {
  const results: SearchResult[] = [];

  // Houses
  houses.forEach((h) => {
    results.push({
      id: `house-${h.id}`,
      title: `${h.id}: ${h.name}`,
      subtitle: h.spheres.join(", "),
      category: "house",
      href: "/lattice",
    });
    // Spheres
    h.spheres.forEach((s, idx) => {
      results.push({
        id: `sphere-${h.id}-S${idx + 1}`,
        title: `${h.id}-S${idx + 1}: ${s}`,
        subtitle: `House: ${h.name}`,
        category: "sphere",
        href: "/lattice",
      });
    });
  });

  // VIP Elements
  vipElements.forEach((v) => {
    results.push({
      id: `vip-${v.id}`,
      title: `${v.id}: ${v.name}`,
      subtitle: v.subtitle,
      category: "vip",
      href: "/elements",
    });
  });

  // Invariants
  invariants.forEach((inv) => {
    results.push({
      id: `inv-${inv.id}`,
      title: `${inv.id}: ${inv.name}`,
      subtitle: `${inv.category} — ${inv.description}`,
      category: "invariant",
      href: "/governance",
    });
  });

  // Doctrines
  doctrines.forEach((d) => {
    results.push({
      id: `doc-${d.id}`,
      title: `${d.id}: ${d.name}`,
      subtitle: `Status: ${d.status}`,
      category: "doctrine",
      href: "/governance",
    });
  });

  // Council Seats
  councilSeats.forEach((s) => {
    results.push({
      id: `council-${s.id}`,
      title: `${s.id}: ${s.name}`,
      subtitle: `${s.role} — ${s.status}`,
      category: "council",
      href: "/governance",
    });
  });

  // Routing Modules
  routingModules.forEach((m) => {
    results.push({
      id: `module-${m.id}`,
      title: `${m.id}: ${m.name}`,
      subtitle: `${m.layer} — ${m.description}`,
      category: "module",
      href: "/routing",
    });
  });

  // Market Players
  marketPlayers.forEach((p: { name: string; approach: string; weakness: string }) => {
    results.push({
      id: `market-${p.name}`,
      title: p.name,
      subtitle: p.approach,
      category: "market",
      href: "/market",
    });
  });

  return results;
}

export default function GlobalSearch() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const [, setLocation] = useLocation();
  const indexRef = useRef<SearchResult[]>([]);

  // Build index on mount
  useEffect(() => {
    indexRef.current = buildSearchIndex();
  }, []);

  // Keyboard shortcut: Cmd+K / Ctrl+K
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setOpen((prev) => !prev);
      }
      if (e.key === "Escape") {
        setOpen(false);
      }
    }
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Focus input when opened
  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery("");
      setResults([]);
      setSelectedIndex(0);
    }
  }, [open]);

  // Search logic
  const handleSearch = useCallback((q: string) => {
    setQuery(q);
    if (q.length < 2) {
      setResults([]);
      setSelectedIndex(0);
      return;
    }
    const lower = q.toLowerCase();
    const filtered = indexRef.current.filter(
      (r) =>
        r.title.toLowerCase().includes(lower) ||
        r.subtitle.toLowerCase().includes(lower)
    );
    setResults(filtered.slice(0, 20));
    setSelectedIndex(0);
  }, []);

  // Navigate to result
  const navigateTo = useCallback(
    (result: SearchResult) => {
      setOpen(false);
      setLocation(result.href);
    },
    [setLocation]
  );

  // Keyboard navigation
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.min(prev + 1, results.length - 1));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.max(prev - 1, 0));
      } else if (e.key === "Enter" && results[selectedIndex]) {
        e.preventDefault();
        navigateTo(results[selectedIndex]);
      }
    },
    [results, selectedIndex, navigateTo]
  );

  return (
    <>
      {/* Trigger button */}
      <button
        onClick={() => setOpen(true)}
        className="flex items-center gap-2 px-3 py-1.5 rounded border border-border/50 bg-secondary/50 text-muted-foreground hover:text-foreground hover:border-primary/30 transition-colors text-sm"
      >
        <Search className="w-3.5 h-3.5" />
        <span className="hidden sm:inline">Search</span>
        <kbd className="hidden sm:inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded bg-background/80 border border-border/50 text-[10px] font-mono text-muted-foreground ml-2">
          ⌘K
        </kbd>
      </button>

      {/* Modal overlay */}
      {open && (
        <div className="fixed inset-0 z-[100] flex items-start justify-center pt-[15vh]">
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-background/80 backdrop-blur-sm"
            onClick={() => setOpen(false)}
          />

          {/* Search panel */}
          <div className="relative w-full max-w-2xl mx-4 bg-card border border-border rounded-xl shadow-2xl overflow-hidden animate-in fade-in slide-in-from-top-4 duration-200">
            {/* Input */}
            <div className="flex items-center gap-3 px-4 py-3 border-b border-border/50">
              <Search className="w-5 h-5 text-muted-foreground shrink-0" />
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => handleSearch(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Search houses, spheres, VIPs, invariants, doctrines, modules..."
                className="flex-1 bg-transparent text-foreground placeholder:text-muted-foreground outline-none text-sm"
              />
              <button
                onClick={() => setOpen(false)}
                className="p-1 rounded text-muted-foreground hover:text-foreground"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Results */}
            <div className="max-h-[50vh] overflow-y-auto">
              {query.length < 2 && (
                <div className="p-6 text-center text-muted-foreground text-sm">
                  <p className="mb-2">Type at least 2 characters to search across:</p>
                  <div className="flex flex-wrap justify-center gap-2 text-xs">
                    {Object.entries(categoryMeta).map(([key, meta]) => (
                      <span key={key} className={`px-2 py-1 rounded bg-secondary/50 ${meta.color}`}>
                        {meta.label}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {query.length >= 2 && results.length === 0 && (
                <div className="p-6 text-center text-muted-foreground text-sm">
                  No results found for &ldquo;{query}&rdquo;
                </div>
              )}

              {results.length > 0 && (
                <div className="py-2">
                  {results.map((result, i) => {
                    const meta = categoryMeta[result.category];
                    const Icon = meta.icon;
                    return (
                      <button
                        key={result.id}
                        onClick={() => navigateTo(result)}
                        className={`w-full flex items-start gap-3 px-4 py-3 text-left transition-colors ${
                          i === selectedIndex
                            ? "bg-primary/10 border-l-2 border-primary"
                            : "hover:bg-secondary/50 border-l-2 border-transparent"
                        }`}
                      >
                        <Icon className={`w-4 h-4 mt-0.5 shrink-0 ${meta.color}`} />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-medium text-foreground truncate">
                              {result.title}
                            </span>
                            <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded bg-secondary ${meta.color}`}>
                              {meta.label}
                            </span>
                          </div>
                          <p className="text-xs text-muted-foreground truncate mt-0.5">
                            {result.subtitle}
                          </p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between px-4 py-2 border-t border-border/50 text-[10px] text-muted-foreground">
              <div className="flex items-center gap-3">
                <span className="flex items-center gap-1">
                  <kbd className="px-1 py-0.5 rounded bg-secondary border border-border/50 font-mono">↑↓</kbd>
                  Navigate
                </span>
                <span className="flex items-center gap-1">
                  <kbd className="px-1 py-0.5 rounded bg-secondary border border-border/50 font-mono">↵</kbd>
                  Select
                </span>
                <span className="flex items-center gap-1">
                  <kbd className="px-1 py-0.5 rounded bg-secondary border border-border/50 font-mono">Esc</kbd>
                  Close
                </span>
              </div>
              <span>{results.length > 0 ? `${results.length} results` : `${indexRef.current.length} indexed`}</span>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
