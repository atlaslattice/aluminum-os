// Design: Obsidian Substrate — Data Visualization Dashboard
// Network graph + connection matrix + relationship explorer
// Shows VIP ↔ House, VIP ↔ Doctrine, VIP ↔ Reference, VIP ↔ Module connections

import { useState, useMemo, useCallback, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import SpecLayout from "@/components/SpecLayout";
import {
  vipElements,
  houses,
  invariants,
  doctrines,
  routingModules,
  councilSeats,
  architectureLayers,
  GITHUB_URL,
} from "@/lib/data";
import { Network, Grid3x3, Search, Zap, Shield, BookOpen, Layers, Users } from "lucide-react";

// === RELATIONSHIP DATA ===
// Build edges between entities
interface GraphNode {
  id: string;
  label: string;
  type: "vip" | "house" | "invariant" | "doctrine" | "module" | "council";
  color: string;
  x: number;
  y: number;
  radius: number;
}

interface GraphEdge {
  source: string;
  target: string;
  type: "vip-house" | "vip-module" | "vip-invariant" | "vip-doctrine" | "vip-council";
  strength: number;
}

// Build the connection matrix data
interface MatrixCell {
  row: string;
  col: string;
  value: number;
  connections: string[];
}

// Compute relationships from data
function buildRelationships() {
  const edges: GraphEdge[] = [];

  // VIP → House connections (from housePairs)
  vipElements.forEach((vip) => {
    vip.housePairs.forEach((houseId) => {
      edges.push({ source: vip.id, target: houseId, type: "vip-house", strength: 3 });
    });
  });

  // VIP → Module connections (inferred from module descriptions and VIP scope)
  const moduleVipMap: Record<string, string[]> = {
    M0: ["E145"], M1: ["E145"], M2: ["E145"],
    M3: ["E145", "E150"], M4: ["E145", "E149"],
    M5: ["E149", "E152"], M6: ["E149", "E152"],
    M7: ["E149", "E145"], M8: ["E145", "E150"],
    M9: ["E155", "E145"], M10: ["E145", "E152"],
    M11: ["E145", "E155"],
    M13: ["E145", "E150"], M14: ["E145"],
    M15: ["E145", "E149"], M16: ["E149", "E145"],
    M17: ["E149", "E152"], M18: ["E153", "E148"],
    M19: ["E154", "E148"], M20: ["E155", "E145"],
    M21: ["E149", "E150"], M22: ["E145", "E152"],
  };

  Object.entries(moduleVipMap).forEach(([modId, vips]) => {
    vips.forEach((vipId) => {
      edges.push({ source: vipId, target: modId, type: "vip-module", strength: 2 });
    });
  });

  // VIP → Invariant connections
  const invVipMap: Record<string, string[]> = {
    "INV-0": ["E149", "E145"], "INV-1": ["E149"],
    "INV-3": ["E155", "E149"], "INV-7": ["E145", "E150"],
    "INV-7c": ["E145", "E150"], "INV-9": ["E145", "E154"],
    "INV-11": ["E149", "E150"], "INV-14": ["E152", "E149"],
    "INV-17": ["E155", "E145"], "INV-19": ["E155", "E152"],
    "INV-44": ["E149", "E152"],
  };

  Object.entries(invVipMap).forEach(([invId, vips]) => {
    vips.forEach((vipId) => {
      edges.push({ source: vipId, target: invId, type: "vip-invariant", strength: 4 });
    });
  });

  // VIP → Doctrine connections (top doctrines)
  const docVipMap: Record<string, string[]> = {
    "D-1": ["E149"], "D-2": ["E145", "E150"],
    "D-3": ["E155", "E149"], "D-4": ["E152"],
    "D-5": ["E145", "E154"], "D-6": ["E155"],
    "D-7": ["E149"], "D-8": ["E145"],
    "D-9": ["E149"], "D-10": ["E145"],
    "D-14": ["E149", "E152"], "D-20": ["E152"],
    "D-21": ["E152", "E145"], "D-98": ["E155", "E150"],
    "D-98-CN": ["E150", "E152"],
  };

  Object.entries(docVipMap).forEach(([docId, vips]) => {
    vips.forEach((vipId) => {
      edges.push({ source: vipId, target: docId, type: "vip-doctrine", strength: 2 });
    });
  });

  // VIP → Council connections
  const councilVipMap: Record<string, string[]> = {
    S1: ["E149", "E145"], S2: ["E150", "E145"],
    S3: ["E150", "E152"], S4: ["E145", "E154"],
    S5: ["E150", "E152"], S6: ["E150", "E149"],
    S7: ["E145", "E154"], S8: ["E150", "E152"],
    S9: ["E150", "E149"], S10: ["E154", "E148"],
    S11: ["E155", "E156"], S12: ["E156", "E147"],
  };

  Object.entries(councilVipMap).forEach(([seatId, vips]) => {
    vips.forEach((vipId) => {
      edges.push({ source: vipId, target: seatId, type: "vip-council", strength: 3 });
    });
  });

  return edges;
}

// Build adjacency matrix for VIP-to-VIP connections (via shared houses, modules, etc.)
function buildMatrix(): MatrixCell[] {
  const cells: MatrixCell[] = [];
  const edges = buildRelationships();

  vipElements.forEach((vipA) => {
    vipElements.forEach((vipB) => {
      if (vipA.id === vipB.id) {
        cells.push({ row: vipA.id, col: vipB.id, value: 0, connections: [] });
        return;
      }
      // Count shared connections
      const aTargets = new Set(edges.filter((e) => e.source === vipA.id).map((e) => e.target));
      const bTargets = new Set(edges.filter((e) => e.source === vipB.id).map((e) => e.target));
      const shared = Array.from(aTargets).filter((t) => bTargets.has(t));
      cells.push({ row: vipA.id, col: vipB.id, value: shared.length, connections: shared });
    });
  });

  return cells;
}

// === FORCE-DIRECTED GRAPH COMPONENT ===
interface EdgeTooltipData {
  x: number;
  y: number;
  source: string;
  target: string;
  type: string;
  strength: number;
}

function ForceGraph({ selectedVip, onSelectVip }: { selectedVip: string | null; onSelectVip: (id: string | null) => void }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [dimensions, setDimensions] = useState({ width: 900, height: 600 });
  const [hoveredEdge, setHoveredEdge] = useState<EdgeTooltipData | null>(null);
  const edges = useMemo(() => buildRelationships(), []);

  useEffect(() => {
    const updateDimensions = () => {
      if (svgRef.current?.parentElement) {
        const rect = svgRef.current.parentElement.getBoundingClientRect();
        setDimensions({ width: Math.max(rect.width, 600), height: Math.max(500, Math.min(rect.height, 700)) });
      }
    };
    updateDimensions();
    window.addEventListener("resize", updateDimensions);
    return () => window.removeEventListener("resize", updateDimensions);
  }, []);

  // Position nodes in a radial layout
  const nodes = useMemo(() => {
    const { width, height } = dimensions;
    const cx = width / 2;
    const cy = height / 2;
    const result: GraphNode[] = [];

    // VIP Elements — inner ring
    vipElements.forEach((vip, i) => {
      const angle = (i / vipElements.length) * Math.PI * 2 - Math.PI / 2;
      const r = Math.min(width, height) * 0.22;
      result.push({
        id: vip.id, label: vip.name, type: "vip",
        color: vip.color, x: cx + Math.cos(angle) * r, y: cy + Math.sin(angle) * r, radius: 18,
      });
    });

    // Houses — outer ring
    houses.forEach((house, i) => {
      const angle = (i / houses.length) * Math.PI * 2 - Math.PI / 2;
      const r = Math.min(width, height) * 0.38;
      result.push({
        id: house.id, label: house.name, type: "house",
        color: house.color, x: cx + Math.cos(angle) * r, y: cy + Math.sin(angle) * r, radius: 12,
      });
    });

    // Invariants — scattered top-left
    invariants.forEach((inv, i) => {
      const angle = (i / invariants.length) * Math.PI * 0.6 + Math.PI * 0.85;
      const r = Math.min(width, height) * 0.42;
      result.push({
        id: inv.id, label: inv.name, type: "invariant",
        color: "#ef5350", x: cx + Math.cos(angle) * r, y: cy + Math.sin(angle) * r, radius: 8,
      });
    });

    // Council seats — bottom cluster
    councilSeats.forEach((seat, i) => {
      const angle = (i / councilSeats.length) * Math.PI * 0.5 + Math.PI * 0.25;
      const r = Math.min(width, height) * 0.42;
      result.push({
        id: seat.id, label: seat.name, type: "council",
        color: "#4fc3f7", x: cx + Math.cos(angle) * r, y: cy + Math.sin(angle) * r, radius: 10,
      });
    });

    return result;
  }, [dimensions]);

  // Filter edges based on selection
  const visibleEdges = useMemo(() => {
    if (!selectedVip) return edges.slice(0, 60); // Show subset when nothing selected
    return edges.filter((e) => e.source === selectedVip || e.target === selectedVip);
  }, [edges, selectedVip]);

  const nodeMap = useMemo(() => {
    const map: Record<string, GraphNode> = {};
    nodes.forEach((n) => { map[n.id] = n; });
    return map;
  }, [nodes]);

  const highlightedNodes = useMemo(() => {
    if (!selectedVip) return new Set<string>();
    const connected = new Set<string>([selectedVip]);
    visibleEdges.forEach((e) => {
      connected.add(e.source);
      connected.add(e.target);
    });
    return connected;
  }, [selectedVip, visibleEdges]);

  return (
    <svg ref={svgRef} width="100%" height={dimensions.height} viewBox={`0 0 ${dimensions.width} ${dimensions.height}`} className="select-none">
      {/* Edges */}
      {visibleEdges.map((edge, i) => {
        const source = nodeMap[edge.source];
        const target = nodeMap[edge.target];
        if (!source || !target) return null;
        const opacity = selectedVip ? 0.6 : 0.15;
        const edgeColor = edge.type === "vip-house" ? "#00ffd5" :
          edge.type === "vip-invariant" ? "#ef5350" :
          edge.type === "vip-council" ? "#4fc3f7" :
          edge.type === "vip-doctrine" ? "#ce93d8" : "#7986cb";
        const midX = (source.x + target.x) / 2;
        const midY = (source.y + target.y) / 2;
        return (
          <g key={`edge-${i}`}>
            <line
              x1={source.x} y1={source.y}
              x2={target.x} y2={target.y}
              stroke={edgeColor}
              strokeWidth={edge.strength * 0.5}
              opacity={opacity}
              strokeDasharray={edge.type === "vip-doctrine" ? "4 2" : undefined}
            />
            {/* Invisible wider hit area for hover */}
            <line
              x1={source.x} y1={source.y}
              x2={target.x} y2={target.y}
              stroke="transparent"
              strokeWidth={12}
              className="cursor-pointer"
              onMouseEnter={() => setHoveredEdge({ x: midX, y: midY, source: source.label, target: target.label, type: edge.type, strength: edge.strength })}
              onMouseLeave={() => setHoveredEdge(null)}
            />
          </g>
        );
      })}

      {/* Nodes */}
      {nodes.map((node) => {
        const isHighlighted = !selectedVip || highlightedNodes.has(node.id);
        const isSelected = node.id === selectedVip;
        return (
          <g
            key={node.id}
            onClick={() => {
              if (node.type === "vip") onSelectVip(isSelected ? null : node.id);
            }}
            className={node.type === "vip" ? "cursor-pointer" : ""}
            opacity={isHighlighted ? 1 : 0.2}
          >
            {isSelected && (
              <circle cx={node.x} cy={node.y} r={node.radius + 6} fill="none" stroke={node.color} strokeWidth={2} opacity={0.5}>
                <animate attributeName="r" values={`${node.radius + 4};${node.radius + 8};${node.radius + 4}`} dur="2s" repeatCount="indefinite" />
              </circle>
            )}
            <circle
              cx={node.x} cy={node.y} r={node.radius}
              fill={isSelected ? node.color : `${node.color}33`}
              stroke={node.color}
              strokeWidth={isSelected ? 2.5 : 1.5}
            />
            {node.radius >= 12 && (
              <text
                x={node.x} y={node.y + node.radius + 14}
                textAnchor="middle"
                fill={isHighlighted ? "#e0e0e0" : "#555"}
                fontSize={node.type === "vip" ? 10 : 8}
                fontFamily="IBM Plex Sans, sans-serif"
              >
                {node.label.length > 16 ? node.label.slice(0, 14) + "…" : node.label}
              </text>
            )}
            {node.type === "vip" && (
              <text
                x={node.x} y={node.y + 4}
                textAnchor="middle"
                fill="#fff"
                fontSize={8}
                fontWeight="bold"
                fontFamily="JetBrains Mono, monospace"
              >
                {node.id.replace("E", "")}
              </text>
            )}
          </g>
        );
      })}

      {/* Edge Tooltip */}
      {hoveredEdge && (
        <g transform={`translate(${hoveredEdge.x}, ${hoveredEdge.y})`}>
          <rect
            x={-110} y={-50}
            width={220} height={46}
            rx={6}
            fill="#0a0f0d"
            stroke={hoveredEdge.type === "vip-house" ? "#00ffd5" : hoveredEdge.type === "vip-invariant" ? "#ef5350" : hoveredEdge.type === "vip-council" ? "#4fc3f7" : hoveredEdge.type === "vip-doctrine" ? "#ce93d8" : "#7986cb"}
            strokeWidth={1}
            opacity={0.95}
          />
          <text x={0} y={-30} textAnchor="middle" fill="#e0e0e0" fontSize={10} fontFamily="IBM Plex Sans, sans-serif" fontWeight="600">
            {hoveredEdge.source} → {hoveredEdge.target}
          </text>
          <text x={0} y={-14} textAnchor="middle" fill="#888" fontSize={9} fontFamily="JetBrains Mono, monospace">
            {hoveredEdge.type.replace("vip-", "VIP → ").replace(/^(.)/, (c) => c.toUpperCase())} · strength {hoveredEdge.strength}
          </text>
        </g>
      )}

      {/* Legend */}
      <g transform={`translate(16, ${dimensions.height - 100})`}>
        <rect x={0} y={0} width={160} height={90} rx={4} fill="#0a0a0a" stroke="#1a1a1a" strokeWidth={1} opacity={0.9} />
        {[
          { color: "#00ffd5", label: "VIP → House", y: 14 },
          { color: "#ef5350", label: "VIP → Invariant", y: 30 },
          { color: "#ce93d8", label: "VIP → Doctrine", y: 46 },
          { color: "#4fc3f7", label: "VIP → Council", y: 62 },
          { color: "#7986cb", label: "VIP → Module", y: 78 },
        ].map((item) => (
          <g key={item.label}>
            <line x1={10} y1={item.y} x2={30} y2={item.y} stroke={item.color} strokeWidth={2} />
            <text x={36} y={item.y + 4} fill="#aaa" fontSize={9} fontFamily="IBM Plex Sans, sans-serif">{item.label}</text>
          </g>
        ))}
      </g>
    </svg>
  );
}

// === CONNECTION MATRIX COMPONENT ===
function ConnectionMatrix({ onSelectVip }: { onSelectVip: (id: string | null) => void }) {
  const matrix = useMemo(() => buildMatrix(), []);
  const maxVal = useMemo(() => Math.max(...matrix.map((c) => c.value)), [matrix]);
  const [hoveredCell, setHoveredCell] = useState<MatrixCell | null>(null);

  const cellSize = 42;
  const labelWidth = 100;
  const vips = vipElements.map((v) => v.id);

  return (
    <div className="overflow-x-auto">
      <div className="inline-block">
        {/* Column headers */}
        <div className="flex" style={{ marginLeft: labelWidth }}>
          {vips.map((id) => {
            const vip = vipElements.find((v) => v.id === id)!;
            return (
              <div
                key={id}
                className="text-center cursor-pointer hover:text-primary transition-colors"
                style={{ width: cellSize, fontSize: 9 }}
                onClick={() => onSelectVip(id)}
              >
                <span className="font-mono" style={{ color: vip.color }}>{id.replace("E", "")}</span>
              </div>
            );
          })}
        </div>

        {/* Rows */}
        {vips.map((rowId) => {
          const rowVip = vipElements.find((v) => v.id === rowId)!;
          return (
            <div key={rowId} className="flex items-center">
              <div
                className="truncate text-right pr-2 cursor-pointer hover:text-primary transition-colors"
                style={{ width: labelWidth, fontSize: 9, color: rowVip.color }}
                onClick={() => onSelectVip(rowId)}
              >
                {rowVip.name}
              </div>
              {vips.map((colId) => {
                const cell = matrix.find((c) => c.row === rowId && c.col === colId)!;
                const intensity = cell.value / maxVal;
                const bg = rowId === colId
                  ? "rgba(0, 255, 213, 0.05)"
                  : `rgba(0, 255, 213, ${intensity * 0.7})`;
                return (
                  <div
                    key={`${rowId}-${colId}`}
                    className="border border-border/30 flex items-center justify-center cursor-pointer hover:border-primary/50 transition-all relative"
                    style={{ width: cellSize, height: cellSize, background: bg }}
                    onMouseEnter={() => setHoveredCell(cell)}
                    onMouseLeave={() => setHoveredCell(null)}
                  >
                    {cell.value > 0 && (
                      <span className="font-mono text-xs" style={{ color: intensity > 0.5 ? "#0a0a0a" : "#00ffd5" }}>
                        {cell.value}
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          );
        })}

        {/* Tooltip */}
        {hoveredCell && hoveredCell.value > 0 && (
          <div className="mt-3 p-3 rounded border border-primary/30 bg-card/80 backdrop-blur">
            <p className="text-sm font-mono text-primary">
              {hoveredCell.row} ↔ {hoveredCell.col}: <span className="text-foreground">{hoveredCell.value} shared connections</span>
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              via: {hoveredCell.connections.slice(0, 6).join(", ")}{hoveredCell.connections.length > 6 ? "…" : ""}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

// === RELATIONSHIP EXPLORER COMPONENT ===
function RelationshipExplorer({ selectedVip }: { selectedVip: string | null }) {
  const edges = useMemo(() => buildRelationships(), []);

  if (!selectedVip) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        <Network className="w-12 h-12 mx-auto mb-4 opacity-40" />
        <p className="text-lg">Select a VIP Element to explore its relationships</p>
        <p className="text-sm mt-2">Click any VIP node in the graph or matrix above</p>
      </div>
    );
  }

  const vip = vipElements.find((v) => v.id === selectedVip);
  if (!vip) return null;

  const relatedEdges = edges.filter((e) => e.source === selectedVip || e.target === selectedVip);

  const grouped = {
    houses: relatedEdges.filter((e) => e.type === "vip-house"),
    modules: relatedEdges.filter((e) => e.type === "vip-module"),
    invariants: relatedEdges.filter((e) => e.type === "vip-invariant"),
    doctrines: relatedEdges.filter((e) => e.type === "vip-doctrine"),
    council: relatedEdges.filter((e) => e.type === "vip-council"),
  };

  const getTargetLabel = (edge: GraphEdge) => {
    const targetId = edge.source === selectedVip ? edge.target : edge.source;
    const house = houses.find((h) => h.id === targetId);
    if (house) return `${house.id} — ${house.name}`;
    const inv = invariants.find((i) => i.id === targetId);
    if (inv) return `${inv.id} — ${inv.name}`;
    const doc = doctrines.find((d) => d.id === targetId);
    if (doc) return `${doc.id} — ${doc.name}`;
    const mod = routingModules.find((m) => m.id === targetId);
    if (mod) return `${mod.id} — ${mod.name}`;
    const seat = councilSeats.find((s) => s.id === targetId);
    if (seat) return `${seat.id} — ${seat.name} (${seat.role})`;
    return targetId;
  };

  const sections = [
    { key: "houses", label: "Connected Houses", icon: <Layers className="w-4 h-4" />, items: grouped.houses, color: "#00ffd5" },
    { key: "modules", label: "Routing Modules", icon: <Zap className="w-4 h-4" />, items: grouped.modules, color: "#7986cb" },
    { key: "invariants", label: "Constitutional Invariants", icon: <Shield className="w-4 h-4" />, items: grouped.invariants, color: "#ef5350" },
    { key: "doctrines", label: "Governance Doctrines", icon: <BookOpen className="w-4 h-4" />, items: grouped.doctrines, color: "#ce93d8" },
    { key: "council", label: "Council Seats", icon: <Users className="w-4 h-4" />, items: grouped.council, color: "#4fc3f7" },
  ];

  return (
    <div>
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: `${vip.color}22`, border: `1px solid ${vip.color}44` }}>
          <span className="font-mono text-sm font-bold" style={{ color: vip.color }}>{vip.code.replace("E", "")}</span>
        </div>
        <div>
          <h3 className="text-lg font-display font-semibold text-foreground">{vip.name}</h3>
          <p className="text-sm text-muted-foreground">{vip.subtitle} — {relatedEdges.length} total connections</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sections.map((section) => (
          <div key={section.key} className="p-4 rounded-lg border border-border/50 bg-card/30">
            <div className="flex items-center gap-2 mb-3">
              <span style={{ color: section.color }}>{section.icon}</span>
              <h4 className="text-sm font-medium text-foreground">{section.label}</h4>
              <span className="ml-auto text-xs font-mono px-1.5 py-0.5 rounded bg-secondary text-muted-foreground">
                {section.items.length}
              </span>
            </div>
            <div className="space-y-1.5">
              {section.items.map((edge, i) => (
                <div key={i} className="text-xs text-muted-foreground hover:text-foreground transition-colors py-0.5">
                  {getTargetLabel(edge)}
                </div>
              ))}
              {section.items.length === 0 && (
                <p className="text-xs text-muted-foreground/50 italic">No direct connections</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// === STATS SUMMARY ===
function StatsSummary() {
  const edges = useMemo(() => buildRelationships(), []);
  const stats = useMemo(() => {
    const byType: Record<string, number> = {};
    edges.forEach((e) => { byType[e.type] = (byType[e.type] || 0) + 1; });
    return byType;
  }, [edges]);

  const items = [
    { label: "Total Connections", value: edges.length, color: "#00ffd5" },
    { label: "VIP → House", value: stats["vip-house"] || 0, color: "#00ffd5" },
    { label: "VIP → Module", value: stats["vip-module"] || 0, color: "#7986cb" },
    { label: "VIP → Invariant", value: stats["vip-invariant"] || 0, color: "#ef5350" },
    { label: "VIP → Doctrine", value: stats["vip-doctrine"] || 0, color: "#ce93d8" },
    { label: "VIP → Council", value: stats["vip-council"] || 0, color: "#4fc3f7" },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      {items.map((item) => (
        <div key={item.label} className="p-3 rounded-lg border border-border/50 bg-card/30 text-center">
          <div className="text-2xl font-display font-bold" style={{ color: item.color }}>{item.value}</div>
          <div className="text-xs text-muted-foreground mt-1">{item.label}</div>
        </div>
      ))}
    </div>
  );
}

// === MAIN DASHBOARD PAGE ===
export default function Dashboard() {
  const [selectedVip, setSelectedVip] = useState<string | null>(null);
  const [activeView, setActiveView] = useState<"graph" | "matrix">("graph");

  const handleSelectVip = useCallback((id: string | null) => {
    setSelectedVip(id);
  }, []);

  return (
    <SpecLayout>
      

      <main className="pt-20 pb-24">
        <div className="container">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-10"
          >
            <h1 className="text-4xl md:text-5xl font-display font-bold">
              <span className="text-primary">Relationship</span>{" "}
              <span className="text-foreground">Dashboard</span>
            </h1>
            <p className="text-muted-foreground mt-3 max-w-2xl text-lg">
              Interactive visualization of connections between VIP Elements, Houses, Doctrines, Invariants, Modules, and Council Seats.
              Click any VIP node to explore its full relationship graph.
            </p>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="mb-8"
          >
            <StatsSummary />
          </motion.div>

          {/* View Toggle */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mb-6"
          >
            <div className="flex items-center gap-2">
              <button
                onClick={() => setActiveView("graph")}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeView === "graph"
                    ? "bg-primary/10 text-primary border border-primary/30"
                    : "text-muted-foreground hover:text-foreground hover:bg-secondary border border-transparent"
                }`}
              >
                <Network className="w-4 h-4" /> Network Graph
              </button>
              <button
                onClick={() => setActiveView("matrix")}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeView === "matrix"
                    ? "bg-primary/10 text-primary border border-primary/30"
                    : "text-muted-foreground hover:text-foreground hover:bg-secondary border border-transparent"
                }`}
              >
                <Grid3x3 className="w-4 h-4" /> Connection Matrix
              </button>
              {selectedVip && (
                <button
                  onClick={() => setSelectedVip(null)}
                  className="ml-auto flex items-center gap-2 px-3 py-1.5 rounded text-xs text-muted-foreground hover:text-foreground hover:bg-secondary border border-border/50 transition-all"
                >
                  Clear Selection
                </button>
              )}
            </div>
          </motion.div>

          {/* Visualization */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mb-10 rounded-xl border border-border/50 bg-card/20 backdrop-blur overflow-hidden"
          >
            {activeView === "graph" ? (
              <div className="p-4">
                <ForceGraph selectedVip={selectedVip} onSelectVip={handleSelectVip} />
              </div>
            ) : (
              <div className="p-6">
                <h3 className="text-lg font-display font-semibold text-foreground mb-1">VIP-to-VIP Shared Connections</h3>
                <p className="text-sm text-muted-foreground mb-6">
                  Each cell shows how many entities (Houses, Modules, Invariants, Doctrines, Council Seats) two VIP Elements share.
                  Higher values indicate tighter coupling.
                </p>
                <ConnectionMatrix onSelectVip={handleSelectVip} />
              </div>
            )}
          </motion.div>

          {/* Relationship Explorer */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="rounded-xl border border-border/50 bg-card/20 backdrop-blur p-6"
          >
            <RelationshipExplorer selectedVip={selectedVip} />
          </motion.div>

          {/* Architecture Layers Cross-Reference */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="mt-10 rounded-xl border border-border/50 bg-card/20 backdrop-blur p-6"
          >
            <h3 className="text-xl font-display font-semibold text-foreground mb-2">Architecture Layer Dependencies</h3>
            <p className="text-sm text-muted-foreground mb-6">
              How the 9 architectural layers interconnect — each layer depends on layers below it.
            </p>
            <div className="space-y-3">
              {architectureLayers.map((layer, i) => (
                <div key={layer.id} className="flex items-start gap-4 p-3 rounded-lg border border-border/30 hover:border-border/60 transition-colors">
                  <div className="flex-shrink-0 w-8 h-8 rounded flex items-center justify-center font-mono text-xs font-bold bg-primary/10 text-primary border border-primary/30">
                    L{i + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-sm text-foreground">{layer.name}</span>
                      <span className="text-xs text-muted-foreground">— {layer.description}</span>
                    </div>
                    <div className="flex flex-wrap gap-1.5 mt-1.5">
                      {layer.modules.split(", ").map((mod: string) => (
                        <span key={mod} className="text-xs font-mono px-1.5 py-0.5 rounded bg-secondary/50 text-muted-foreground">
                          {mod}
                        </span>
                      ))}
                    </div>
                  </div>
                  {i < architectureLayers.length - 1 && (
                    <div className="flex-shrink-0 text-xs text-muted-foreground/50 self-center">↓</div>
                  )}
                </div>
              ))}
            </div>
          </motion.div>

          {/* GitHub CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="mt-12 text-center"
          >
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg border border-primary/30 text-primary hover:bg-primary/10 transition-all font-medium"
            >
              <Network className="w-4 h-4" />
              Explore Full Ontology on GitHub
            </a>
          </motion.div>
        </div>
      </main>
    </SpecLayout>
  );
}
