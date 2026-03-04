"use client";

import { useState } from "react";
import { apiPost } from "@/lib/api";

export function AITutorChat({ token, studentId }: { token: string; studentId: string }) {
  const [q, setQ] = useState("How does algebra affect calculus?");
  const [a, setA] = useState("Tutor response will appear here.");

  async function ask() {
    const data = await apiPost("/tutor/chat", token, { student_id: studentId, message: q, concept_context: ["Algebra", "Calculus"] });
    setA(data.answer);
  }

  return (
    <div className="space-y-2">
      <textarea className="w-full rounded bg-slate-900 p-2" value={q} onChange={(e) => setQ(e.target.value)} />
      <button className="rounded bg-emerald-600 px-4 py-2" onClick={ask}>Ask Tutor</button>
      <p className="text-sm text-slate-200">{a}</p>
    </div>
  );
}
