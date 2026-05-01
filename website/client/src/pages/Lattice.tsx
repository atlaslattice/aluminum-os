import { useState, useMemo, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import SpecLayout from "@/components/SpecLayout";
import { houses, GITHUB_URL } from "@/lib/data";

// === CANONICAL SUB-SPHERE DATA ===
// Source: shared/house-00_directory/registries/sub_sphere_registry.yaml
// Status: PARTIAL — 30 entries populated; enumeration ongoing
// Only Council-ratified entries are shown. No AI-generated additions.
interface SubSphere {
  id: string;
  name: string;
  status: "RATIFIED" | "PROPOSED";
}

const canonicalSubSpheres: Record<string, SubSphere[]> = {
  // H5 Arts — Sport & Physical Culture (S-051 → sphere index 0-based within H5... but we key by "H5-S5" style)
  // Using parent sphere name as key for clarity
  "H5-Visual Arts": [],
  "H5-Music": [],
  "H5-Film & Cinema": [],
  "H5-Architecture": [],
  "H5-Design": [],
  "H5-Photography": [],
  "H5-Performing Arts": [
    { id: "SS-0481", name: "Olympic & Paralympic Sport", status: "RATIFIED" },
    { id: "SS-0482", name: "Combat Sports & Martial Arts", status: "RATIFIED" },
    { id: "SS-0483", name: "Team Ball Sports", status: "RATIFIED" },
    { id: "SS-0484", name: "Endurance & Adventure Sport", status: "RATIFIED" },
    { id: "SS-0485", name: "Esports & Competitive Gaming", status: "RATIFIED" },
  ],
  "H5-Crafts & Applied Arts": [
    { id: "SS-0486", name: "Gastronomy & Molecular Cuisine", status: "RATIFIED" },
    { id: "SS-0487", name: "Fermentation & Preservation", status: "RATIFIED" },
    { id: "SS-0488", name: "Regional Culinary Traditions", status: "RATIFIED" },
    { id: "SS-0489", name: "Food Science & Nutrition Engineering", status: "RATIFIED" },
    { id: "SS-0490", name: "Sustainable Agriculture & Farm-to-Table", status: "RATIFIED" },
  ],
  // H4 Humanities — Indigenous Knowledge (S-041 = Cultural Studies)
  "H4-Cultural Studies": [
    { id: "SS-0491", name: "Aboriginal Australian Knowledge", status: "RATIFIED" },
    { id: "SS-0492", name: "First Nations (Americas) Knowledge", status: "RATIFIED" },
    { id: "SS-0493", name: "Māori & Pacific Islander Knowledge", status: "RATIFIED" },
    { id: "SS-0494", name: "African Traditional Knowledge Systems", status: "RATIFIED" },
    { id: "SS-0495", name: "South & Southeast Asian Indigenous Knowledge", status: "RATIFIED" },
  ],
  // H3 Social Sciences — Digital Sociology (S-025 = Sociology)
  "H3-Sociology": [
    { id: "SS-0496", name: "Platform Governance & Digital Commons", status: "RATIFIED" },
    { id: "SS-0497", name: "Algorithmic Bias & Social Impact", status: "RATIFIED" },
    { id: "SS-0498", name: "Digital Labour & Gig Economy", status: "RATIFIED" },
  ],
  // H9 Health — Integrative Medicine (S-097 = General Medicine)
  "H9-General Medicine": [
    { id: "SS-0499", name: "Psychedelic-Assisted Therapy", status: "RATIFIED" },
    { id: "SS-0500", name: "Longevity & Anti-Aging Science", status: "RATIFIED" },
    { id: "SS-0501", name: "Telemedicine & Remote Diagnostics", status: "RATIFIED" },
  ],
  "H9-Rehabilitation": [
    { id: "SS-0502", name: "Neuroplasticity & Brain Rehabilitation", status: "RATIFIED" },
    { id: "SS-0503", name: "Wearable Health Monitoring", status: "RATIFIED" },
  ],
  // H6 Engineering — Emerging Tech
  "H6-Nanotechnology": [
    { id: "SS-0504", name: "Molecular Machines & Nanobots", status: "RATIFIED" },
    { id: "SS-0505", name: "Quantum Materials & Metamaterials", status: "RATIFIED" },
  ],
  "H6-Aerospace": [
    { id: "SS-0506", name: "Orbital Manufacturing & In-Space Assembly", status: "RATIFIED" },
  ],
  // H11 Infrastructure — Climate Resilience
  "H11-Energy": [
    { id: "SS-0507", name: "Green Hydrogen & Fusion Energy", status: "RATIFIED" },
    { id: "SS-0508", name: "Grid-Scale Battery Storage", status: "RATIFIED" },
  ],
  "H11-Water Systems": [
    { id: "SS-0509", name: "Desalination & Water Recycling", status: "RATIFIED" },
  ],
  "H11-Urban Planning": [
    { id: "SS-0510", name: "Climate-Adaptive Urban Design", status: "RATIFIED" },
  ],
};

function getSubSpheres(houseId: string, sphereName: string): SubSphere[] {
  const key = `${houseId}-${sphereName}`;
  return canonicalSubSpheres[key] || [];
}

// Sphere numbering: H1 = S-001..S-012, H2 = S-013..S-024, etc.
function getSphereId(houseNumber: number, sphereIndex: number): string {
  const num = (houseNumber - 1) * 12 + sphereIndex + 1;
  return `S-${String(num).padStart(3, "0")}`;
}

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Lattice() {
  const [selectedHouse, setSelectedHouse] = useState<number | null>(null);
  const [selectedSphere, setSelectedSphere] = useState<{ houseId: string; sphereName: string; sphereId: string } | null>(null);
  const [viewMode, setViewMode] = useState<"radial" | "grid">("radial");

  // Zoom/pan state
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const [panStart, setPanStart] = useState({ x: 0, y: 0 });
  const svgContainerRef = useRef<HTMLDivElement>(null);

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -0.1 : 0.1;
    setZoom((prev) => Math.min(3, Math.max(0.5, prev + delta)));
  }, []);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if (e.button === 1 || e.altKey) {
      setIsPanning(true);
      setPanStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  }, [pan]);

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (isPanning) {
      setPan({ x: e.clientX - panStart.x, y: e.clientY - panStart.y });
    }
  }, [isPanning, panStart]);

  const handleMouseUp = useCallback(() => {
    setIsPanning(false);
  }, []);

  const resetView = useCallback(() => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  }, []);

  const selectedHouseData = useMemo(
    () => (selectedHouse !== null ? houses.find((h) => h.number === selectedHouse) : null),
    [selectedHouse]
  );

  const subSpheres = useMemo(
    () => (selectedSphere ? getSubSpheres(selectedSphere.houseId, selectedSphere.sphereName) : []),
    [selectedSphere]
  );

  const handleHouseClick = useCallback((houseNumber: number) => {
    setSelectedHouse((prev) => (prev === houseNumber ? null : houseNumber));
    setSelectedSphere(null);
  }, []);

  const handleSphereClick = useCallback(
    (houseId: string, sphereName: string, sphereId: string) => {
      setSelectedSphere((prev) =>
        prev?.sphereId === sphereId ? null : { houseId, sphereName, sphereId }
      );
    },
    []
  );

  // SVG radial layout calculations
  const centerX = 300;
  const centerY = 300;
  const houseRadius = 220;
  const sphereRadius = 130;

  return (
    <SpecLayout>
      <div className="pt-24 pb-16">
        <div className="container max-w-7xl">
          {/* Hero */}
          <motion.div initial="hidden" animate="visible" variants={fadeUp}>
            <div className="flex items-center justify-between flex-wrap gap-4 mb-2">
              <h1 className="text-4xl font-display font-bold">
                The 12×12 <span className="text-gradient-teal">Lattice</span>
              </h1>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setViewMode("radial")}
                  className={`px-3 py-1.5 rounded text-xs font-mono transition-colors ${
                    viewMode === "radial"
                      ? "bg-primary/20 text-primary border border-primary/30"
                      : "bg-card/30 text-muted-foreground border border-border/30 hover:bg-card/50"
                  }`}
                >
                  Radial
                </button>
                <button
                  onClick={() => setViewMode("grid")}
                  className={`px-3 py-1.5 rounded text-xs font-mono transition-colors ${
                    viewMode === "grid"
                      ? "bg-primary/20 text-primary border border-primary/30"
                      : "bg-card/30 text-muted-foreground border border-border/30 hover:bg-card/50"
                  }`}
                >
                  Grid
                </button>
              </div>
            </div>
            <p className="text-muted-foreground text-lg mb-2">
              12 Houses × 12 Spheres = 144 canonical knowledge nodes. ~499 sub-spheres enumerated (ongoing).
            </p>
            <p className="text-muted-foreground/60 text-xs mb-1 font-mono">
              Canon locked. No AI-generated additions. Source: Council-ratified ontology, Build Plan v2.3.
            </p>
            <div className="substrate-line mb-8" />
          </motion.div>

          {/* Configuration C Delta Notice */}
          <motion.div
            initial="hidden"
            animate="visible"
            variants={fadeUp}
            className="mb-4 p-4 rounded border border-red-500/20 bg-red-500/5"
          >
            <div className="flex items-start gap-3">
              <span className="text-red-400 text-lg mt-0.5">⚠</span>
              <div>
                <p className="text-sm text-red-200/80 font-medium">Configuration C Structural Delta (Convenor Review Pending)</p>
                <p className="text-xs text-red-200/50 mt-1">
                  This page displays the v3-era House structure (Natural Sciences, Formal Sciences, Social Sciences,
                  Humanities, etc.) with H[n].S[m] dot addressing. Configuration C (v4.0) proposes structural changes:
                  Agriculture, Security, and Philosophy/Ethics/Religion as standalone Houses; Cognition as tier-1 in H1;
                  H#-S# hyphenated addressing. The Convenor has not yet issued a final ruling on whether Configuration C
                  supersedes the v3 structure for public canon. Until resolved, this page reflects the last ratified structure.
                </p>
              </div>
            </div>
          </motion.div>

          {/* Canon Lock Notice */}
          <motion.div
            initial="hidden"
            animate="visible"
            variants={fadeUp}
            className="mb-8 p-4 rounded border border-amber-500/20 bg-amber-500/5"
          >
            <div className="flex items-start gap-3">
              <span className="text-amber-400 text-lg mt-0.5">⚠</span>
              <div>
                <p className="text-sm text-amber-200/80 font-medium">Canon Integrity Notice</p>
                <p className="text-xs text-amber-200/50 mt-1">
                  House names, sphere names, and sub-sphere entries shown here are the working canon established
                  through Council deliberation. The sub-sphere registry is partial (~499 enumerated of a projected
                  larger set). Entries marked RATIFIED have passed Council review. No sphere may be added, renamed,
                  or reordered without Convenor approval per Doctrine 97-a.
                </p>
              </div>
            </div>
          </motion.div>

          {/* Radial View */}
          {viewMode === "radial" && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mb-12"
            >
              <div className="flex flex-col lg:flex-row gap-8">
                {/* SVG Visualization with Zoom/Pan */}
                <div
                  ref={svgContainerRef}
                  className="flex-1 flex justify-center relative overflow-hidden rounded border border-border/20"
                  onWheel={handleWheel}
                  onMouseDown={handleMouseDown}
                  onMouseMove={handleMouseMove}
                  onMouseUp={handleMouseUp}
                  onMouseLeave={handleMouseUp}
                  style={{ cursor: isPanning ? 'grabbing' : 'default' }}
                >
                  {/* Zoom controls */}
                  <div className="absolute top-3 right-3 z-10 flex flex-col gap-1">
                    <button onClick={() => setZoom(z => Math.min(3, z + 0.2))} className="w-7 h-7 rounded bg-card/80 border border-border/30 text-primary text-sm font-mono hover:bg-card flex items-center justify-center">+</button>
                    <button onClick={() => setZoom(z => Math.max(0.5, z - 0.2))} className="w-7 h-7 rounded bg-card/80 border border-border/30 text-primary text-sm font-mono hover:bg-card flex items-center justify-center">−</button>
                    <button onClick={resetView} className="w-7 h-7 rounded bg-card/80 border border-border/30 text-muted-foreground text-[9px] font-mono hover:bg-card flex items-center justify-center" title="Reset view">1:1</button>
                  </div>
                  <div className="absolute bottom-2 left-3 z-10 text-[10px] font-mono text-muted-foreground/40">
                    {Math.round(zoom * 100)}% | Scroll to zoom · Alt+drag to pan
                  </div>
                  <svg
                    viewBox="0 0 600 600"
                    className="w-full max-w-[600px] h-auto"
                    style={{ minHeight: 400, transform: `scale(${zoom}) translate(${pan.x / zoom}px, ${pan.y / zoom}px)`, transformOrigin: 'center center', transition: isPanning ? 'none' : 'transform 0.15s ease-out' }}
                  >
                    {/* Background rings */}
                    <circle cx={centerX} cy={centerY} r={houseRadius + 30} fill="none" stroke="rgba(0,255,213,0.05)" strokeWidth="1" />
                    <circle cx={centerX} cy={centerY} r={houseRadius - 30} fill="none" stroke="rgba(0,255,213,0.03)" strokeWidth="1" />
                    <circle cx={centerX} cy={centerY} r={sphereRadius + 20} fill="none" stroke="rgba(0,255,213,0.03)" strokeWidth="1" />

                    {/* Center label */}
                    <text x={centerX} y={centerY - 12} textAnchor="middle" fill="#00ffd5" fontSize="14" fontFamily="Space Grotesk" fontWeight="bold">
                      12×12
                    </text>
                    <text x={centerX} y={centerY + 6} textAnchor="middle" fill="rgba(255,255,255,0.5)" fontSize="10" fontFamily="JetBrains Mono">
                      144 Spheres
                    </text>
                    <text x={centerX} y={centerY + 20} textAnchor="middle" fill="rgba(255,255,255,0.3)" fontSize="8" fontFamily="JetBrains Mono">
                      ~499 Sub-Spheres
                    </text>

                    {/* House nodes */}
                    {houses.map((house, i) => {
                      const angle = (i / 12) * Math.PI * 2 - Math.PI / 2;
                      const x = centerX + Math.cos(angle) * houseRadius;
                      const y = centerY + Math.sin(angle) * houseRadius;
                      const isSelected = selectedHouse === house.number;

                      return (
                        <g
                          key={house.id}
                          onClick={() => handleHouseClick(house.number)}
                          className="cursor-pointer"
                          role="button"
                          tabIndex={0}
                        >
                          {/* Connection line to center */}
                          <line
                            x1={centerX}
                            y1={centerY}
                            x2={x}
                            y2={y}
                            stroke={isSelected ? house.color : "rgba(255,255,255,0.06)"}
                            strokeWidth={isSelected ? 2 : 1}
                            strokeDasharray={isSelected ? "none" : "4,4"}
                          />

                          {/* House circle */}
                          <circle
                            cx={x}
                            cy={y}
                            r={isSelected ? 28 : 22}
                            fill={isSelected ? `${house.color}20` : "rgba(255,255,255,0.03)"}
                            stroke={house.color}
                            strokeWidth={isSelected ? 2 : 1}
                            opacity={isSelected ? 1 : 0.7}
                            className="transition-all duration-300"
                          />

                          {/* House ID */}
                          <text
                            x={x}
                            y={y - 4}
                            textAnchor="middle"
                            fill={house.color}
                            fontSize="10"
                            fontFamily="JetBrains Mono"
                            fontWeight="bold"
                          >
                            {house.id}
                          </text>

                          {/* House name (abbreviated) */}
                          <text
                            x={x}
                            y={y + 8}
                            textAnchor="middle"
                            fill="rgba(255,255,255,0.5)"
                            fontSize="6"
                            fontFamily="IBM Plex Sans"
                          >
                            {house.name.length > 12 ? house.name.slice(0, 11) + "…" : house.name}
                          </text>

                          {/* Sphere count badge */}
                          <text
                            x={x}
                            y={y + 16}
                            textAnchor="middle"
                            fill="rgba(255,255,255,0.25)"
                            fontSize="6"
                            fontFamily="JetBrains Mono"
                          >
                            12 spheres
                          </text>
                        </g>
                      );
                    })}

                    {/* Selected house spheres (inner ring) */}
                    {selectedHouseData && selectedHouseData.spheres.map((sphere, i) => {
                      const angle = (i / 12) * Math.PI * 2 - Math.PI / 2;
                      const x = centerX + Math.cos(angle) * sphereRadius;
                      const y = centerY + Math.sin(angle) * sphereRadius;
                      const sphereId = getSphereId(selectedHouseData.number, i);
                      const isSelectedSphere = selectedSphere?.sphereId === sphereId;
                      const subs = getSubSpheres(selectedHouseData.id, sphere);
                      const hasSubs = subs.length > 0;

                      return (
                        <g
                          key={`sphere-${i}`}
                          onClick={(e) => {
                            e.stopPropagation();
                            handleSphereClick(selectedHouseData.id, sphere, sphereId);
                          }}
                          className="cursor-pointer"
                          role="button"
                          tabIndex={0}
                        >
                          <motion.circle
                            initial={{ r: 0, opacity: 0 }}
                            animate={{ r: isSelectedSphere ? 18 : 14, opacity: 1 }}
                            transition={{ delay: i * 0.04, duration: 0.3 }}
                            cx={x}
                            cy={y}
                            fill={isSelectedSphere ? `${selectedHouseData.color}30` : "rgba(255,255,255,0.04)"}
                            stroke={isSelectedSphere ? selectedHouseData.color : `${selectedHouseData.color}60`}
                            strokeWidth={isSelectedSphere ? 2 : 1}
                          />

                          {/* Sub-sphere indicator dot */}
                          {hasSubs && (
                            <circle
                              cx={x + 10}
                              cy={y - 10}
                              r={3}
                              fill="#ffd54f"
                              opacity={0.8}
                            />
                          )}

                          <motion.text
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: i * 0.04 + 0.2 }}
                            x={x}
                            y={y - 2}
                            textAnchor="middle"
                            fill="rgba(255,255,255,0.7)"
                            fontSize="6"
                            fontFamily="JetBrains Mono"
                          >
                            {sphereId}
                          </motion.text>

                          <motion.text
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: i * 0.04 + 0.2 }}
                            x={x}
                            y={y + 7}
                            textAnchor="middle"
                            fill="rgba(255,255,255,0.4)"
                            fontSize="5"
                            fontFamily="IBM Plex Sans"
                          >
                            {sphere.length > 10 ? sphere.slice(0, 9) + "…" : sphere}
                          </motion.text>
                        </g>
                      );
                    })}
                  </svg>
                </div>

                {/* Detail Panel */}
                <div className="lg:w-80 flex-shrink-0">
                  <AnimatePresence mode="wait">
                    {!selectedHouseData && (
                      <motion.div
                        key="instructions"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="p-5 rounded border border-border/30 bg-card/20"
                      >
                        <p className="text-sm text-muted-foreground">
                          Click a <span className="text-primary font-mono">House</span> node on the radial map to expand its 12 Spheres.
                          Click a Sphere to see its ratified Sub-Spheres.
                        </p>
                        <div className="mt-4 space-y-2">
                          <div className="flex items-center gap-2 text-xs text-muted-foreground/60">
                            <span className="w-3 h-3 rounded-full border border-primary/50" /> House node
                          </div>
                          <div className="flex items-center gap-2 text-xs text-muted-foreground/60">
                            <span className="w-3 h-3 rounded-full border border-primary/30 bg-primary/10" /> Sphere node
                          </div>
                          <div className="flex items-center gap-2 text-xs text-muted-foreground/60">
                            <span className="w-2 h-2 rounded-full bg-[#ffd54f]" /> Has ratified sub-spheres
                          </div>
                        </div>
                      </motion.div>
                    )}

                    {selectedHouseData && !selectedSphere && (
                      <motion.div
                        key={`house-${selectedHouse}`}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        className="p-5 rounded border border-border/30 bg-card/20"
                      >
                        <div className="flex items-center gap-3 mb-4">
                          <div className="w-4 h-4 rounded-full" style={{ backgroundColor: selectedHouseData.color }} />
                          <div>
                            <h3 className="font-display font-bold text-sm">{selectedHouseData.id} — {selectedHouseData.name}</h3>
                            <p className="text-[10px] font-mono text-muted-foreground/60">
                              {getSphereId(selectedHouseData.number, 0)} – {getSphereId(selectedHouseData.number, 11)}
                            </p>
                          </div>
                        </div>
                        <div className="space-y-1.5">
                          {selectedHouseData.spheres.map((sphere, i) => {
                            const sid = getSphereId(selectedHouseData.number, i);
                            const subs = getSubSpheres(selectedHouseData.id, sphere);
                            return (
                              <button
                                key={i}
                                onClick={() => handleSphereClick(selectedHouseData.id, sphere, sid)}
                                className="w-full text-left p-2 rounded border border-border/20 bg-background/30 hover:border-primary/30 hover:bg-primary/5 transition-colors flex items-center gap-2"
                              >
                                <span className="text-[10px] font-mono text-primary/70 w-10">{sid}</span>
                                <span className="text-xs text-foreground/70 flex-1">{sphere}</span>
                                {subs.length > 0 && (
                                  <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-[#ffd54f]/10 text-[#ffd54f]">
                                    {subs.length} sub
                                  </span>
                                )}
                              </button>
                            );
                          })}
                        </div>
                      </motion.div>
                    )}

                    {selectedSphere && selectedHouseData && (
                      <motion.div
                        key={`sphere-${selectedSphere.sphereId}`}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        className="p-5 rounded border border-border/30 bg-card/20"
                      >
                        <button
                          onClick={() => setSelectedSphere(null)}
                          className="text-xs text-primary hover:underline mb-3 flex items-center gap-1"
                        >
                          ← Back to {selectedHouseData.id}
                        </button>
                        <div className="flex items-center gap-2 mb-3">
                          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: selectedHouseData.color }} />
                          <div>
                            <h3 className="font-display font-bold text-sm">{selectedSphere.sphereName}</h3>
                            <p className="text-[10px] font-mono text-muted-foreground/60">
                              {selectedSphere.sphereId} · {selectedHouseData.id} · {selectedHouseData.name}
                            </p>
                          </div>
                        </div>

                        {subSpheres.length > 0 ? (
                          <div className="space-y-1.5">
                            <p className="text-[10px] font-mono text-muted-foreground/50 mb-2">
                              {subSpheres.length} ratified sub-sphere{subSpheres.length !== 1 ? "s" : ""}
                            </p>
                            {subSpheres.map((ss) => (
                              <div
                                key={ss.id}
                                className="p-2 rounded border border-border/20 bg-background/30"
                              >
                                <div className="flex items-center justify-between">
                                  <span className="text-xs text-foreground/70">{ss.name}</span>
                                  <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400">
                                    {ss.status}
                                  </span>
                                </div>
                                <span className="text-[9px] font-mono text-muted-foreground/40">{ss.id}</span>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div className="p-4 rounded border border-border/10 bg-background/20 text-center">
                            <p className="text-xs text-muted-foreground/50">No ratified sub-spheres in registry yet.</p>
                            <p className="text-[10px] text-muted-foreground/30 mt-1">Enumeration ongoing — Council review required.</p>
                          </div>
                        )}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </div>
            </motion.div>
          )}

          {/* Grid View */}
          {viewMode === "grid" && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mb-12"
            >
              {/* 12x12 Matrix */}
              <div className="overflow-x-auto mb-8">
                <div className="min-w-[800px]">
                  {/* Header row */}
                  <div className="flex gap-0.5 mb-0.5">
                    <div className="w-28 flex-shrink-0" />
                    {Array.from({ length: 12 }, (_, i) => (
                      <div key={i} className="flex-1 text-center text-[9px] font-mono text-muted-foreground/50 py-1">
                        S{i + 1}
                      </div>
                    ))}
                  </div>

                  {/* House rows */}
                  {houses.map((house) => (
                    <div key={house.id} className="flex gap-0.5 mb-0.5">
                      <button
                        onClick={() => handleHouseClick(house.number)}
                        className={`w-28 flex-shrink-0 flex items-center gap-1.5 px-2 py-1.5 rounded-l text-left transition-colors ${
                          selectedHouse === house.number
                            ? "bg-primary/10 border border-primary/30"
                            : "bg-card/20 border border-border/20 hover:bg-card/40"
                        }`}
                      >
                        <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: house.color }} />
                        <span className="text-[9px] font-mono text-foreground/70 truncate">{house.id} {house.name}</span>
                      </button>
                      {house.spheres.map((sphere, si) => {
                        const sid = getSphereId(house.number, si);
                        const subs = getSubSpheres(house.id, sphere);
                        const isSelected = selectedSphere?.sphereId === sid;
                        return (
                          <button
                            key={si}
                            onClick={() => {
                              setSelectedHouse(house.number);
                              handleSphereClick(house.id, sphere, sid);
                            }}
                            className={`flex-1 p-1 rounded text-center transition-all group relative ${
                              isSelected
                                ? "bg-primary/20 border border-primary/40"
                                : "bg-card/10 border border-border/10 hover:bg-card/30 hover:border-primary/20"
                            }`}
                            title={`${sid}: ${sphere}${subs.length > 0 ? ` (${subs.length} sub-spheres)` : ""}`}
                          >
                            <div
                              className="w-full h-3 rounded-sm opacity-60 group-hover:opacity-100 transition-opacity"
                              style={{ backgroundColor: `${house.color}40` }}
                            />
                            {subs.length > 0 && (
                              <div className="absolute top-0 right-0 w-1.5 h-1.5 rounded-full bg-[#ffd54f]" />
                            )}
                          </button>
                        );
                      })}
                    </div>
                  ))}
                </div>
              </div>

              {/* Selected detail below grid */}
              <AnimatePresence>
                {selectedSphere && selectedHouseData && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="overflow-hidden"
                  >
                    <div className="p-5 rounded border border-border/30 bg-card/20 mb-6">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: selectedHouseData.color }} />
                          <h3 className="font-display font-bold text-sm">
                            {selectedSphere.sphereId}: {selectedSphere.sphereName}
                          </h3>
                          <span className="text-[10px] font-mono text-muted-foreground/50">
                            {selectedHouseData.id} · {selectedHouseData.name}
                          </span>
                        </div>
                        <button onClick={() => setSelectedSphere(null)} className="text-xs text-primary hover:underline">
                          Close
                        </button>
                      </div>
                      {subSpheres.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                          {subSpheres.map((ss) => (
                            <div key={ss.id} className="p-2 rounded border border-border/20 bg-background/30 flex items-center justify-between">
                              <div>
                                <span className="text-xs text-foreground/70">{ss.name}</span>
                                <span className="block text-[9px] font-mono text-muted-foreground/40">{ss.id}</span>
                              </div>
                              <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400">
                                {ss.status}
                              </span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-xs text-muted-foreground/50">No ratified sub-spheres in registry yet. Enumeration ongoing.</p>
                      )}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )}

          {/* Full House Reference List */}
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
          >
            <h2 className="text-2xl font-display font-bold mb-2">Complete House Registry</h2>
            <p className="text-muted-foreground/60 text-xs font-mono mb-6">
              12 Houses × 12 Spheres = 144 nodes. Addresses follow H[n].S[m] convention. Sub-sphere count from sub_sphere_registry.yaml.
            </p>
            <div className="space-y-4">
              {houses.map((house) => {
                const totalSubs = house.spheres.reduce(
                  (acc, s) => acc + getSubSpheres(house.id, s).length,
                  0
                );
                return (
                  <div
                    key={house.id}
                    className="p-5 rounded border border-border/50 bg-card/20 hover:bg-card/40 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: house.color }} />
                        <h3 className="font-display font-semibold">
                          <span className="font-mono text-primary text-sm mr-2">{house.id}</span>
                          {house.name}
                        </h3>
                      </div>
                      <div className="flex items-center gap-3 text-[10px] font-mono text-muted-foreground/50">
                        <span>{getSphereId(house.number, 0)}–{getSphereId(house.number, 11)}</span>
                        {totalSubs > 0 && (
                          <span className="px-1.5 py-0.5 rounded bg-[#ffd54f]/10 text-[#ffd54f]">
                            {totalSubs} sub-spheres
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {house.spheres.map((sphere, i) => {
                        const subs = getSubSpheres(house.id, sphere);
                        return (
                          <span
                            key={i}
                            className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-secondary/50 text-xs group relative"
                          >
                            <span className="font-mono text-primary/70 text-[10px]">{getSphereId(house.number, i)}</span>
                            <span className="text-foreground/70">{sphere}</span>
                            {subs.length > 0 && (
                              <span className="w-1.5 h-1.5 rounded-full bg-[#ffd54f] ml-0.5" />
                            )}
                          </span>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>

          {/* Source Links */}
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
            className="mt-12 p-5 rounded border border-border/30 bg-card/10"
          >
            <h3 className="font-display font-semibold text-sm mb-3">Source Traceability</h3>
            <div className="grid sm:grid-cols-2 gap-3 text-xs">
              <a
                href={`${GITHUB_URL}/blob/master/docs/architecture/SOURCE_OF_TRUTH.md`}
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 rounded border border-border/20 bg-background/30 hover:border-primary/30 transition-colors flex items-center gap-2"
              >
                <span className="text-primary">→</span>
                <span className="text-foreground/70">SOURCE_OF_TRUTH.md</span>
                <span className="text-muted-foreground/40 ml-auto font-mono">GitHub</span>
              </a>
              <a
                href={`${GITHUB_URL}/tree/master/architecture`}
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 rounded border border-border/20 bg-background/30 hover:border-primary/30 transition-colors flex items-center gap-2"
              >
                <span className="text-primary">→</span>
                <span className="text-foreground/70">Architecture Specs</span>
                <span className="text-muted-foreground/40 ml-auto font-mono">GitHub</span>
              </a>
              <a
                href={`${GITHUB_URL}/tree/master/governance`}
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 rounded border border-border/20 bg-background/30 hover:border-primary/30 transition-colors flex items-center gap-2"
              >
                <span className="text-primary">→</span>
                <span className="text-foreground/70">Governance Documents</span>
                <span className="text-muted-foreground/40 ml-auto font-mono">GitHub</span>
              </a>
              <a
                href={`${GITHUB_URL}/tree/master/council`}
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 rounded border border-border/20 bg-background/30 hover:border-primary/30 transition-colors flex items-center gap-2"
              >
                <span className="text-primary">→</span>
                <span className="text-foreground/70">Council Records</span>
                <span className="text-muted-foreground/40 ml-auto font-mono">GitHub</span>
              </a>
            </div>
          </motion.div>
        </div>
      </div>
    </SpecLayout>
  );
}
