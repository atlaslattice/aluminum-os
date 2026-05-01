import { Link, useLocation } from "wouter";
import { useState } from "react";
import { ChevronDown, ChevronRight, Menu, X, Github, ExternalLink } from "lucide-react";
import { GITHUB_URL } from "@/lib/data";
import GlobalSearch from "./GlobalSearch";

interface NavGroup {
  label: string;
  items: { href: string; label: string }[];
}

const sidebarGroups: NavGroup[] = [
  {
    label: "Overview",
    items: [
      { href: "/", label: "Home" },
      { href: "/canon", label: "Canon (Keystone)" },
      { href: "/layers", label: "9-Layer Architecture" },
      { href: "/glossary", label: "Glossary" },
    ],
  },
  {
    label: "Ontology",
    items: [
      { href: "/lattice", label: "12×12 Lattice" },
      { href: "/elements", label: "VIP Elements (E145–E156)" },
      { href: "/mirror", label: "As Above, So Below" },
    ],
  },
  {
    label: "Routing & Compute",
    items: [
      { href: "/routing", label: "Routing Pack" },
      { href: "/sovereignty", label: "Sovereignty" },
      { href: "/dialects", label: "Dialects" },
      { href: "/compute-zones", label: "Compute Zones" },
      { href: "/simulation", label: "Simulation & Activation" },
    ],
  },
  {
    label: "Governance",
    items: [
      { href: "/governance", label: "Constitution & Council" },
      { href: "/invariants", label: "43 Invariants" },
      { href: "/doctrines", label: "Doctrines Registry" },
      { href: "/anti-monoculture", label: "Anti-Monoculture" },
      { href: "/provenance", label: "Provenance" },
      { href: "/verifier", label: "Open-Weight Verifier" },
    ],
  },
  {
    label: "Strategy & Operations",
    items: [
      { href: "/strategy", label: "Battle Strategy" },
      { href: "/market", label: "Market & Capabilities" },
      { href: "/dashboard", label: "Dashboard" },
      { href: "/ingestion", label: "Ingestion" },
      { href: "/appendix", label: "Appendix" },
    ],
  },
];

function VersionBanner() {
  return (
    <div className="bg-amber-500/10 border border-amber-500/30 rounded px-4 py-2 mb-6">
      <div className="flex items-center gap-3 text-xs">
        <span className="font-mono text-amber-400 font-semibold">v4.0-DRAFT.6</span>
        <span className="text-amber-300/80">|</span>
        <span className="text-amber-300/80">Public Draft (Not Canonical)</span>
        <span className="text-amber-300/80">|</span>
        <span className="text-muted-foreground">Last Updated: {new Date().toLocaleString("en-US", { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", timeZoneName: "short" })}</span>
        <span className="text-amber-300/80">|</span>
        <span className="text-muted-foreground">Convenor: Daavud Sheldon</span>
      </div>
    </div>
  );
}

function Breadcrumb() {
  const [location] = useLocation();
  const allItems = sidebarGroups.flatMap((g) => g.items);
  const current = allItems.find((i) => i.href === location);
  const group = sidebarGroups.find((g) => g.items.some((i) => i.href === location));

  if (location === "/") return null;

  return (
    <nav className="flex items-center gap-1.5 text-xs text-muted-foreground mb-4">
      <Link href="/" className="hover:text-foreground transition-colors">
        Home
      </Link>
      {group && (
        <>
          <ChevronRight className="w-3 h-3" />
          <span>{group.label}</span>
        </>
      )}
      {current && (
        <>
          <ChevronRight className="w-3 h-3" />
          <span className="text-foreground font-medium">{current.label}</span>
        </>
      )}
    </nav>
  );
}

function Sidebar({ className }: { className?: string }) {
  const [location] = useLocation();
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({});

  const toggle = (label: string) => {
    setCollapsed((prev) => ({ ...prev, [label]: !prev[label] }));
  };

  return (
    <aside className={`${className} overflow-y-auto`}>
      <div className="p-4">
        <Link href="/" className="flex items-center gap-2 mb-6 group">
          <div className="w-7 h-7 rounded-sm bg-primary/20 border border-primary/40 flex items-center justify-center">
            <span className="font-mono text-[10px] text-primary font-bold">Al</span>
          </div>
          <span className="font-display font-semibold text-sm text-foreground">
            Aluminum OS
          </span>
        </Link>

        <div className="space-y-1">
          {sidebarGroups.map((group) => {
            const isCollapsed = collapsed[group.label];
            const hasActive = group.items.some((i) => i.href === location);

            return (
              <div key={group.label}>
                <button
                  onClick={() => toggle(group.label)}
                  className={`w-full flex items-center justify-between px-2 py-1.5 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
                    hasActive ? "text-primary" : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {group.label}
                  {isCollapsed ? (
                    <ChevronRight className="w-3 h-3" />
                  ) : (
                    <ChevronDown className="w-3 h-3" />
                  )}
                </button>
                {!isCollapsed && (
                  <div className="ml-2 mt-0.5 space-y-0.5">
                    {group.items.map((item) => (
                      <Link
                        key={item.href}
                        href={item.href}
                        className={`block px-3 py-1.5 rounded text-xs transition-colors ${
                          location === item.href
                            ? "text-primary bg-primary/10 font-medium"
                            : "text-muted-foreground hover:text-foreground hover:bg-secondary"
                        }`}
                      >
                        {item.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="mt-6 pt-4 border-t border-border/50">
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-2 py-1.5 rounded text-xs text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
          >
            <Github className="w-3.5 h-3.5" />
            GitHub Repository
            <ExternalLink className="w-3 h-3 ml-auto" />
          </a>
          <a
            href={`${GITHUB_URL}/blob/master/docs/ORCS.md`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-2 py-1.5 rounded text-xs text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            ORCS Companion Standard
          </a>
          <div className="mt-3 px-2">
            <GlobalSearch />
          </div>
        </div>
      </div>
    </aside>
  );
}

interface SpecLayoutProps {
  children: React.ReactNode;
}

export default function SpecLayout({ children }: SpecLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background text-foreground flex">
      {/* Desktop sidebar */}
      <Sidebar className="hidden lg:block w-64 shrink-0 border-r border-border/50 sticky top-0 h-screen" />

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="lg:hidden fixed inset-0 z-50 flex">
          <div
            className="absolute inset-0 bg-black/50"
            onClick={() => setSidebarOpen(false)}
          />
          <Sidebar className="relative z-10 w-64 bg-background border-r border-border/50 h-full" />
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 min-w-0">
        {/* Mobile header */}
        <div className="lg:hidden sticky top-0 z-40 border-b border-border/50 bg-background/80 backdrop-blur-xl px-4 py-3 flex items-center gap-3">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-1.5 rounded text-muted-foreground hover:text-foreground hover:bg-secondary"
          >
            <Menu className="w-5 h-5" />
          </button>
          <Link href="/" className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-sm bg-primary/20 border border-primary/40 flex items-center justify-center">
              <span className="font-mono text-[9px] text-primary font-bold">Al</span>
            </div>
            <span className="font-display font-semibold text-sm">Aluminum OS</span>
          </Link>
        </div>

        <main className="max-w-5xl mx-auto px-6 py-8">
          <VersionBanner />
          <Breadcrumb />
          {children}
        </main>

        {/* Footer */}
        <footer className="border-t border-border/50 mt-16">
          <div className="max-w-5xl mx-auto px-6 py-6">
            <div className="flex flex-wrap items-center justify-between gap-4 text-xs text-muted-foreground">
              <div className="flex items-center gap-3">
                <span className="font-mono text-primary">v4.0-DRAFT.6</span>
                <span>|</span>
                <span>Public Draft — Not Canonical</span>
                <span>|</span>
                <span>CC BY-SA 4.0</span>
                <span>|</span>
                <a href={`${GITHUB_URL}/blob/master/docs/ORCS.md`} target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">ORCS</a>
              </div>
              <div className="flex items-center gap-3">
                <Link href="/glossary" className="hover:text-foreground transition-colors">
                  Glossary
                </Link>
                <span>|</span>
                <span className="font-mono text-[10px]">Machine-readable / LLM-parsable</span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
