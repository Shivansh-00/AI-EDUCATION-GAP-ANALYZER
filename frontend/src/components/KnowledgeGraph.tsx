"use client";

import ReactFlow, { Background, Controls, Edge, Node } from "reactflow";
import "reactflow/dist/style.css";

const concepts = ["Arithmetic", "Algebra", "Functions", "Calculus"];
const deps = [["Arithmetic", "Algebra"], ["Algebra", "Functions"], ["Functions", "Calculus"]];

function color(score: number) {
  if (score < 0.45) return "#ef4444";
  if (score < 0.7) return "#f59e0b";
  return "#22c55e";
}

export function KnowledgeGraph({ mastery }: { mastery: Record<string, number> }) {
  const nodes: Node[] = concepts.map((c, i) => ({
    id: c,
    data: { label: `${c} (${Math.round((mastery[c] ?? 0.5) * 100)}%)` },
    position: { x: 60 + i * 200, y: 80 },
    style: { background: color(mastery[c] ?? 0.5), color: "white", border: 0, borderRadius: 10, padding: 10 }
  }));

  const edges: Edge[] = deps.map(([a, b], i) => ({ id: `e-${i}`, source: a, target: b, animated: true }));

  return (
    <div className="h-64 w-full rounded-lg border border-slate-800">
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}
