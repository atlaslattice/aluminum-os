import { motion } from "framer-motion";
import { ArrowUpDown } from "lucide-react";
import SpecLayout from "@/components/SpecLayout";
import { MIRROR_IMAGE, pairedLogic } from "@/lib/data";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Mirror() {
  return (
    <SpecLayout>
      

      <div className="pt-24 pb-16">
        <div className="container max-w-5xl">
          {/* Hero */}
          <div className="relative rounded-lg overflow-hidden mb-12">
            <img src={MIRROR_IMAGE} alt="As Above So Below" className="w-full h-56 object-cover opacity-30" />
            <div className="absolute inset-0 bg-gradient-to-t from-background via-background/70 to-transparent" />
            <div className="absolute inset-0 flex items-end p-8">
              <motion.div initial="hidden" animate="visible" variants={fadeUp}>
                <h1 className="text-4xl font-display font-bold mb-2">
                  As Above, <span className="text-gradient-gold">So Below</span>
                </h1>
                <p className="text-muted-foreground max-w-xl">
                  Every VIP Element (above) is grounded in specific Houses and Spheres (below).
                  The substrate is the concept; the lattice is the implementation.
                </p>
              </motion.div>
            </div>
          </div>

          {/* Explanation */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <div className="p-6 rounded border border-accent/30 bg-accent/5">
              <h2 className="font-display font-bold text-lg mb-3">The Pairing Principle</h2>
              <p className="text-muted-foreground leading-relaxed">
                The Atlas Lattice operates on a fundamental duality: <strong className="text-foreground">VIP Elements</strong> represent
                civilizational substrates — abstract forces that shape human existence. <strong className="text-foreground">Houses and Spheres</strong> represent
                the concrete disciplines that study, implement, and govern those substrates.
                The "above" is the <em>what</em>; the "below" is the <em>how</em>.
                This pairing makes cross-domain retrieval cheap: to find everything about water sovereignty,
                you don't search — you traverse the graph from E147 down to its paired houses.
              </p>
            </div>
          </motion.div>

          {/* Paired Logic Cards */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
            <div className="space-y-6">
              {pairedLogic.map((pair, i) => (
                <div
                  key={i}
                  className="rounded border border-border/50 bg-card/20 overflow-hidden"
                >
                  {/* Above */}
                  <div className="p-5 border-b border-border/30">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-[10px] font-mono text-primary bg-primary/10 px-2 py-0.5 rounded">ABOVE</span>
                      <span className="font-display font-semibold">{pair.above.name}</span>
                    </div>
                    <p className="text-sm text-muted-foreground">{pair.above.principle}</p>
                  </div>

                  {/* Connection */}
                  <div className="flex items-center gap-3 px-5 py-3 bg-background/50">
                    <ArrowUpDown className="w-4 h-4 text-accent shrink-0" />
                    <p className="text-xs text-accent italic">{pair.connection}</p>
                  </div>

                  {/* Below */}
                  <div className="p-5">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-[10px] font-mono text-accent bg-accent/10 px-2 py-0.5 rounded">BELOW</span>
                      <span className="font-display font-semibold">{pair.below.name}</span>
                    </div>
                    <p className="text-sm text-muted-foreground">{pair.below.principle}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Substrate Retrieval Doctrine */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mt-12">
            <div className="p-6 rounded border border-primary/30 bg-primary/5">
              <h2 className="font-display font-bold text-lg mb-3">Substrate Retrieval Doctrine</h2>
              <p className="text-muted-foreground leading-relaxed mb-4">
                The Atlas Lattice is a <strong className="text-foreground">substrate-organized retrieval graph</strong>, not a keyword index.
                VIP Elements are addressing primitives for retrieval. This means:
              </p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">1.</span>
                  <span>Cross-domain retrieval is cheap because adjacency is encoded at schema time</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">2.</span>
                  <span>Novel insights emerge from traversal, not from keyword matching</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">3.</span>
                  <span>LCC parity is the validation criterion; structural difference is the value proposition</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary mt-1">4.</span>
                  <span>Ingestion is Convenor-grounded: verified-first, then scale</span>
                </li>
              </ul>
            </div>
          </motion.div>
        </div>
      </div>
    </SpecLayout>
  );
}
