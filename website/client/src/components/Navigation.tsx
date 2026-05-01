import { Link, useLocation } from "wouter";
import { useState } from "react";
import { Menu, X, Github } from "lucide-react";
import { GITHUB_URL } from "@/lib/data";
import GlobalSearch from "./GlobalSearch";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/lattice", label: "12×12 Lattice" },
  { href: "/elements", label: "VIP Elements" },
  { href: "/routing", label: "Routing Pack" },
  { href: "/governance", label: "Governance" },
  { href: "/mirror", label: "As Above, So Below" },
  { href: "/strategy", label: "Battle Strategy" },
  { href: "/market", label: "Market & Capabilities" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/appendix", label: "Appendix" },
  { href: "/ingestion", label: "Ingestion" },
];

export default function Navigation() {
  const [location] = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-border/50 backdrop-blur-xl bg-background/80">
      <div className="container flex items-center justify-between h-16">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-8 h-8 rounded-sm bg-primary/20 border border-primary/40 flex items-center justify-center group-hover:glow-teal transition-all">
            <span className="font-mono text-xs text-primary font-bold">Al</span>
          </div>
          <span className="font-display font-semibold text-foreground hidden sm:block">
            Aluminum OS
          </span>
        </Link>

        {/* Desktop nav */}
        <div className="hidden lg:flex items-center gap-1">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`px-3 py-1.5 rounded text-sm transition-colors ${
                location === item.href
                  ? "text-primary bg-primary/10 font-medium"
                  : "text-muted-foreground hover:text-foreground hover:bg-secondary"
              }`}
            >
              {item.label}
            </Link>
          ))}
          <div className="ml-2">
            <GlobalSearch />
          </div>
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="ml-1 p-2 rounded text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
          >
            <Github className="w-4 h-4" />
          </a>
        </div>

        {/* Mobile: search + toggle */}
        <div className="lg:hidden flex items-center gap-2">
          <GlobalSearch />
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="p-2 text-muted-foreground hover:text-foreground"
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="lg:hidden border-t border-border/50 bg-background/95 backdrop-blur-xl">
          <div className="container py-4 flex flex-col gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileOpen(false)}
                className={`px-4 py-2.5 rounded text-sm transition-colors ${
                  location === item.href
                    ? "text-primary bg-primary/10 font-medium"
                    : "text-muted-foreground hover:text-foreground hover:bg-secondary"
                }`}
              >
                {item.label}
              </Link>
            ))}
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2.5 rounded text-sm text-muted-foreground hover:text-foreground hover:bg-secondary flex items-center gap-2"
            >
              <Github className="w-4 h-4" /> GitHub Repository
            </a>
          </div>
        </div>
      )}
    </nav>
  );
}
