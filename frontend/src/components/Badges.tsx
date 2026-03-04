"use client";

const badges = ["7-Day Streak", "Algebra Pathfinder", "Quiz Sprinter", "Consistency Pro"];

export function Badges() {
  return (
    <div className="rounded-lg border border-slate-700 p-4">
      <h3 className="mb-2 text-lg font-semibold">🎖️ Badges</h3>
      <div className="flex flex-wrap gap-2">
        {badges.map((b) => <span key={b} className="rounded-full bg-emerald-800 px-3 py-1 text-xs">{b}</span>)}
      </div>
    </div>
  );
}
