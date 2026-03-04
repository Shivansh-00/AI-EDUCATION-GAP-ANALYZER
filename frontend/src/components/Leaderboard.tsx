"use client";

const leaders = [
  { name: "Ava", xp: 1280 },
  { name: "Liam", xp: 1160 },
  { name: "Noah", xp: 1085 },
  { name: "You", xp: 980 }
];

export function Leaderboard() {
  return (
    <div className="rounded-lg border border-slate-700 p-4">
      <h3 className="mb-2 text-lg font-semibold">🏆 Leaderboard</h3>
      <ul className="space-y-1 text-sm">
        {leaders.map((l, i) => <li key={l.name}>{i + 1}. {l.name} — {l.xp} XP</li>)}
      </ul>
    </div>
  );
}
