"use client";

type Step = { concept: string; reason: string; estimated_minutes?: number };

export function LearningPath({ steps }: { steps: Step[] }) {
  return (
    <ol className="space-y-2 list-decimal pl-6">
      {steps.map((step, idx) => (
        <li key={idx} className="rounded-md border border-slate-700 p-2">
          <p className="font-medium">{step.concept}</p>
          <p className="text-xs text-slate-300">{step.reason}</p>
          {step.estimated_minutes ? <p className="text-xs text-cyan-300">~{step.estimated_minutes} min</p> : null}
        </li>
      ))}
    </ol>
  );
}
