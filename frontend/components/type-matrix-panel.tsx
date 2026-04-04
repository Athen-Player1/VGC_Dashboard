import { TeamAnalysis } from "@/lib/types";

function cellTone(weak: number, resist: number, immune: number) {
  if (weak >= 2) {
    return "bg-[var(--error-container)] text-[var(--on-surface)]";
  }

  if (resist + immune >= 3) {
    return "bg-[var(--secondary-fixed)] text-[var(--on-surface)]";
  }

  return "bg-[var(--surface-container-low)] text-[var(--on-surface-variant)]";
}

export function TypeMatrixPanel({ analysis }: { analysis: TeamAnalysis }) {
  return (
    <div className="rounded-[1.25rem] bg-white p-6 shadow-sm">
      <div>
        <h3 className="font-headline text-xl font-bold">Weakness Chart</h3>
        <p className="mt-2 text-sm text-[var(--on-surface-variant)]">
          Full type matrix for the current shell. Red cells mean stacked exposure, while blue cells
          show healthier defensive buckets.
        </p>
      </div>
      <div className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {analysis.type_matrix.map((entry) => (
          <div
            key={entry.type}
            className={`rounded-2xl px-4 py-3 ${cellTone(entry.weak_count, entry.resist_count, entry.immune_count)}`}
          >
            <div className="font-headline text-base font-bold">{entry.type}</div>
            <div className="mt-2 text-xs">
              {entry.weak_count} weak • {entry.resist_count} resist • {entry.immune_count} immune
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
