"use client";

export function MasteryHeatmap({ mastery }: { mastery: Record<string, number> }) {
  return (
    <div className="grid grid-cols-3 gap-3">
      {Object.entries(mastery).map(([concept, score]) => (
        <div key={concept} className="rounded-lg p-3" style={{ backgroundColor: `rgba(34,197,94,${score})` }}>
          <p className="font-semibold">{concept}</p>
          <p>{Math.round(score * 100)}%</p>
        </div>
      ))}
    </div>
  );
}
