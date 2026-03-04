"use client";

export function LearningGPS({ current = "Algebra", next = ["Functions", "Trigonometry", "Calculus"] }: { current?: string; next?: string[] }) {
  return (
    <div className="space-y-3 rounded-lg border border-cyan-700/40 bg-cyan-950/20 p-4">
      <p className="text-lg font-semibold">🧭 Learning GPS</p>
      <p>You are here: <span className="font-bold text-amber-300">{current}</span></p>
      <p className="text-sm text-slate-300">Next recommended topics:</p>
      <ol className="list-decimal pl-5">
        {next.map((n) => <li key={n}>{n}</li>)}
      </ol>
    </div>
  );
}
