"use client";

import { MasteryHeatmap } from "@/components/MasteryHeatmap";
import { LearningPath } from "@/components/LearningPath";
import { AITutorChat } from "@/components/AITutorChat";
import { useSessionStore } from "@/stores/useSessionStore";
import { useDashboard } from "@/hooks/useDashboard";
import { KnowledgeGraph } from "@/components/KnowledgeGraph";
import { LearningTimeline } from "@/components/LearningTimeline";
import { LearningGPS } from "@/components/LearningGPS";
import { Leaderboard } from "@/components/Leaderboard";
import { Badges } from "@/components/Badges";

export default function HomePage() {
  const { token, studentId } = useSessionStore();
  const { data } = useDashboard(studentId, token);

  const mastery = data?.mastery ?? { Arithmetic: 0.72, Algebra: 0.34, Functions: 0.62, Calculus: 0.21 };
  const steps = data?.learning_path?.steps ?? [
    { concept: "Algebra basics", reason: "Root-cause dependency for Functions and Calculus", estimated_minutes: 35 },
    { concept: "Functions review", reason: "Insufficient mapping and graph intuition", estimated_minutes: 35 },
    { concept: "Calculus", reason: "Re-enter target concept after prerequisite closure", estimated_minutes: 45 }
  ];

  const weak = (data?.weakest_concepts ?? []).map((x: [string, number]) => x[0]);

  return (
    <main className="mx-auto max-w-6xl p-6 space-y-6">
      <h1 className="text-3xl font-bold">AI Education Gap Analyzer</h1>
      <LearningGPS current={weak[0] ?? "Algebra"} next={steps.slice(0, 3).map((s: { concept: string }) => s.concept)} />
      <section className="rounded-xl border border-slate-800 p-4">
        <h2 className="mb-3 text-xl">Concept Mastery Heatmap</h2>
        <MasteryHeatmap mastery={mastery} />
      </section>
      <section className="rounded-xl border border-slate-800 p-4">
        <h2 className="mb-3 text-xl">Knowledge Graph Visualization</h2>
        <KnowledgeGraph mastery={mastery} />
      </section>
      <section className="rounded-xl border border-slate-800 p-4">
        <h2 className="mb-3 text-xl">Learning Path (Connected to Inference Pipeline)</h2>
        <LearningPath steps={steps} />
      </section>
      <section className="rounded-xl border border-slate-800 p-4">
        <h2 className="mb-3 text-xl">Learning Timeline Analytics</h2>
        <LearningTimeline />
      </section>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Leaderboard />
        <Badges />
      </div>
      <section className="rounded-xl border border-slate-800 p-4">
        <h2 className="mb-3 text-xl">AI Tutor</h2>
        <AITutorChat token={token} studentId={studentId} />
      </section>
      <section className="rounded-xl border border-slate-800 p-4 text-sm text-slate-300">
        <h2 className="mb-2 text-xl text-slate-100">Live Aggregated Analytics</h2>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </section>
    </main>
  );
}
