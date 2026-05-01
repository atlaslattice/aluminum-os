// Design: Obsidian Substrate — Market Research & Capabilities Graph
// Dark brutalist data cathedral with electric teal signal and gold VIP accents

import { motion } from "framer-motion";
import SpecLayout from "@/components/SpecLayout";
import { marketPlayers, architectureLayers, abScoringFramework, sovereignPathways } from "@/lib/data";

export default function Market() {
  return (
    <SpecLayout>
    <div className="pt-8 pb-20">
      <div className="max-w-7xl mx-auto px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="text-[#00ffd5]">Market Research</span>{" "}
            <span className="text-white/60">& Capabilities</span>
          </h1>
          <p className="text-white/50 text-lg max-w-3xl">
            Competitive landscape analysis, provider capability mapping, layered architecture, and A/B scoring framework. 
            Each market player maps to a Council seat — the standard absorbs the market rather than competing with it.
          </p>
        </motion.div>

        {/* Layered Architecture */}
        <section className="mb-20">
          <h2 className="text-2xl font-bold text-white mb-2 flex items-center gap-2">
            <span className="text-[#00ffd5]">◈</span> 9-Layer Architecture
          </h2>
          <p className="text-white/40 mb-8 text-sm">Substrate layers are cross-cutting constraints, not linear steps</p>
          <div className="space-y-2">
            {architectureLayers.map((layer, i: number) => {
              const statusColor = layer.status === "OPERATIONAL" ? "#81c784" : layer.status === "IN PROGRESS" ? "#00ffd5" : "#ffd54f";
              return (
                <motion.div
                  key={layer.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className="flex items-stretch border border-white/5 rounded-lg overflow-hidden bg-white/[0.02] hover:bg-white/[0.04] transition-colors"
                >
                  <div
                    className="w-2 flex-shrink-0"
                    style={{ backgroundColor: statusColor }}
                  />
                  <div className="flex-1 p-4 flex items-center gap-6">
                    <div className="w-8 text-center font-mono text-white/30 text-sm">{layer.id}</div>
                    <div className="flex-1">
                      <div className="font-semibold text-white text-sm">{layer.name}</div>
                      <div className="text-white/40 text-xs mt-0.5">{layer.description}</div>
                    </div>
                    <div className="flex flex-wrap gap-1 max-w-xs">
                      <span className="px-2 py-0.5 bg-white/5 rounded text-[10px] text-white/50 font-mono">{layer.modules}</span>
                    </div>
                    <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded`} style={{ color: statusColor, borderColor: statusColor, border: "1px solid" }}>
                      {layer.status}
                    </span>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </section>

        {/* Market Players */}
        <section className="mb-20">
          <h2 className="text-2xl font-bold text-white mb-2 flex items-center gap-2">
            <span className="text-[#ffd54f]">◈</span> Competitive Landscape
          </h2>
          <p className="text-white/40 mb-8 text-sm">Key competitors and how the Atlas Lattice differentiates</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {marketPlayers.map((player: { name: string; approach: string; weakness: string }, i: number) => (
              <motion.div
                key={player.name}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
                className="border border-white/5 rounded-lg p-5 bg-white/[0.02] hover:bg-white/[0.04] transition-colors"
              >
                <h3 className="font-semibold text-white mb-2">{player.name}</h3>
                <div className="mb-3">
                  <div className="text-[10px] text-[#81c784] uppercase tracking-wider mb-1">Approach</div>
                  <div className="text-xs text-white/50 leading-relaxed">{player.approach}</div>
                </div>
                <div>
                  <div className="text-[10px] text-[#ef5350] uppercase tracking-wider mb-1">Gap vs Atlas Lattice</div>
                  <div className="text-xs text-white/50 leading-relaxed">{player.weakness}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </section>

        {/* A/B Scoring Framework */}
        <section className="mb-20">
          <h2 className="text-2xl font-bold text-white mb-2 flex items-center gap-2">
            <span className="text-[#7986cb]">◈</span> A/B Scoring Framework
          </h2>
          <p className="text-white/40 mb-8 text-sm">Routing capability (Matrix A) is strictly separated from market power analysis (Matrix B) — no pay-for-priority</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border border-[#00ffd5]/20 rounded-lg p-6 bg-[#00ffd5]/[0.02]">
              <h3 className="text-lg font-bold text-[#00ffd5] mb-2">Matrix A</h3>
              <div className="text-xs text-white/70 font-semibold mb-1">{abScoringFramework.matrixA.name}</div>
              <p className="text-xs text-white/40 mb-3">{abScoringFramework.matrixA.purpose}</p>
              <p className="text-xs text-white/30">{abScoringFramework.matrixA.usage}</p>
              <div className="mt-3 text-[10px] text-white/20 font-mono">{abScoringFramework.matrixA.file}</div>
            </div>
            <div className="border border-[#ef5350]/20 rounded-lg p-6 bg-[#ef5350]/[0.02]">
              <h3 className="text-lg font-bold text-[#ef5350] mb-2">Matrix B</h3>
              <div className="text-xs text-white/70 font-semibold mb-1">{abScoringFramework.matrixB.name}</div>
              <p className="text-xs text-white/40 mb-3">{abScoringFramework.matrixB.purpose}</p>
              <div className="mb-3">
                <div className="text-[10px] text-white/50 uppercase tracking-wider mb-1">Axes</div>
                {abScoringFramework.matrixB.axes.map((axis: string) => (
                  <div key={axis} className="text-xs text-white/40 leading-relaxed">• {axis}</div>
                ))}
              </div>
              <p className="text-xs text-[#ef5350]/70 font-semibold">{abScoringFramework.matrixB.note}</p>
              <div className="mt-3 text-[10px] text-white/20 font-mono">{abScoringFramework.matrixB.file}</div>
            </div>
          </div>
          <div className="mt-4 p-4 border border-white/5 rounded-lg bg-white/[0.02]">
            <div className="text-[10px] text-white/50 uppercase tracking-wider mb-1">Disambiguation Example</div>
            <p className="text-xs text-white/40">{abScoringFramework.disambiguationExample}</p>
          </div>
        </section>

        {/* Sovereign Deployment Pathways */}
        <section className="mb-20">
          <h2 className="text-2xl font-bold text-white mb-2 flex items-center gap-2">
            <span className="text-[#b388ff]">◈</span> Sovereign Deployment Pathways
          </h2>
          <p className="text-white/40 mb-8 text-sm">Jurisdiction-specific sovereign deployments with full stack sovereignty</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {sovereignPathways.map((d: { name: string; region: string; stack: string; status: string; target: string }) => (
              <div key={d.name} className="border border-white/5 rounded-lg p-4 bg-white/[0.02]">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-white">{d.name}</span>
                  <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded ${
                    d.status === 'DESIGNED' ? 'bg-[#00ffd5]/20 text-[#00ffd5]' :
                    d.status === 'SPECIFIED' ? 'bg-[#ffd54f]/20 text-[#ffd54f]' :
                    'bg-white/5 text-white/30'
                  }`}>
                    {d.status}
                  </span>
                </div>
                <div className="text-xs text-white/50 mb-1">{d.region} — Target: {d.target}</div>
                <div className="text-[10px] text-white/30">{d.stack}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Bottom CTA */}
        <div className="text-center border-t border-white/5 pt-12">
          <p className="text-white/30 text-sm max-w-2xl mx-auto">
            The standard absorbs the market by design. Every major AI provider maps to a Council seat. 
            INV-7c ensures no single provider exceeds 47% of queries. The Indiana Pattern detects and remediates concentration.
          </p>
          <a
            href="https://github.com/atlaslattice/aluminum-os"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block mt-6 px-6 py-3 border border-[#00ffd5]/30 text-[#00ffd5] rounded-lg text-sm hover:bg-[#00ffd5]/5 transition-colors"
          >
            View Full Source on GitHub
          </a>
        </div>
      </div>
    </div>
    </SpecLayout>
  );
}
