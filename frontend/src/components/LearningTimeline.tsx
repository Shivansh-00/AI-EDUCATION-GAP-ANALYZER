"use client";

import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from "recharts";

export function LearningTimeline() {
  const data = [
    { day: "Day 1", Algebra: 35, Calculus: 15 },
    { day: "Day 10", Algebra: 60, Calculus: 28 },
    { day: "Day 20", Algebra: 72, Calculus: 40 },
    { day: "Day 30", Algebra: 81, Calculus: 56 }
  ];

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Algebra" stroke="#22c55e" strokeWidth={2} />
          <Line type="monotone" dataKey="Calculus" stroke="#38bdf8" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
