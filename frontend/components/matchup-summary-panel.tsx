import { MatchupSummary } from "@/lib/types";

function dangerClasses(level: string) {
  if (level === "High") {
    return "bg-[var(--error-container)] text-[var(--error)]";
  }

  if (level === "Medium") {
    return "bg-[var(--tertiary-fixed)] text-[var(--on-surface)]";
  }

  return "bg-[var(--secondary-fixed)] text-[var(--secondary)]";
}

export function MatchupSummaryPanel({
  teamName,
  matchups
}: {
  teamName: string;
  matchups: MatchupSummary[];
}) {
  return (
    <section className="rounded-[1.5rem] bg-white p-8 shadow-sm">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <div className="font-label text-[11px] font-bold uppercase tracking-[0.32em] text-[var(--secondary)]">
            Compare vs Meta
          </div>
          <h2 className="mt-2 font-headline text-2xl font-bold">
            Matchup Summaries for {teamName}
          </h2>
          <p className="mt-2 max-w-3xl text-sm text-[var(--on-surface-variant)]">
            These are first-pass matchup reads generated from your saved team structure and the
            active snapshot teams.
          </p>
        </div>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        {matchups.map((matchup) => (
          <article
            key={matchup.meta_team_id}
            className="rounded-[1.25rem] bg-[var(--surface-container-low)] p-6"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <h3 className="font-headline text-xl font-bold">{matchup.meta_team_name}</h3>
                <p className="mt-2 text-sm leading-6 text-[var(--on-surface-variant)]">
                  {matchup.overview}
                </p>
              </div>
              <span
                className={`rounded-full px-3 py-1 font-label text-[10px] font-bold uppercase tracking-[0.18em] ${dangerClasses(matchup.danger_level)}`}
              >
                {matchup.danger_level}
              </span>
            </div>

            <div className="mt-5 grid gap-5 md:grid-cols-2">
              <div>
                <div className="font-label text-[10px] uppercase tracking-[0.22em] text-[var(--outline)]">
                  Suggested Leads
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  {matchup.suggested_leads.map((lead) => (
                    <span
                      key={lead}
                      className="rounded-full bg-white px-3 py-1 text-[11px] font-semibold text-[var(--on-surface-variant)]"
                    >
                      {lead}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <div className="font-label text-[10px] uppercase tracking-[0.22em] text-[var(--outline)]">
                  Danger Points
                </div>
                <div className="mt-3 space-y-2">
                  {matchup.danger_points.map((item) => (
                    <p
                      key={item}
                      className="rounded-xl bg-[var(--error-container)]/60 px-3 py-2 text-sm text-[var(--on-surface)]"
                    >
                      {item}
                    </p>
                  ))}
                </div>
              </div>
            </div>

            <div className="mt-5">
              <div className="font-label text-[10px] uppercase tracking-[0.22em] text-[var(--outline)]">
                Preserve Targets
              </div>
              <div className="mt-3 space-y-2">
                {matchup.preserve_targets.map((item) => (
                  <p
                    key={item}
                    className="rounded-xl bg-white px-3 py-2 text-sm text-[var(--on-surface-variant)]"
                  >
                    {item}
                  </p>
                ))}
              </div>
            </div>

            <div className="mt-5">
              <div className="font-label text-[10px] uppercase tracking-[0.22em] text-[var(--outline)]">
                Win Conditions
              </div>
              <div className="mt-3 space-y-2">
                {matchup.win_conditions.map((item) => (
                  <p
                    key={item}
                    className="rounded-xl bg-[var(--secondary-fixed)]/60 px-3 py-2 text-sm text-[var(--on-surface)]"
                  >
                    {item}
                  </p>
                ))}
              </div>
            </div>

            <div className="mt-5">
              <div className="font-label text-[10px] uppercase tracking-[0.22em] text-[var(--outline)]">
                Tera Notes
              </div>
              <div className="mt-3 space-y-2">
                {matchup.tera_notes.map((item) => (
                  <p
                    key={item}
                    className="rounded-xl bg-white px-3 py-2 text-sm text-[var(--on-surface-variant)]"
                  >
                    {item}
                  </p>
                ))}
              </div>
            </div>

            <div className="mt-5">
              <div className="font-label text-[10px] uppercase tracking-[0.22em] text-[var(--outline)]">
                Focus Points
              </div>
              <div className="mt-3 space-y-2">
                {matchup.focus_points.map((item) => (
                  <p
                    key={item}
                    className="rounded-xl bg-white px-3 py-2 text-sm text-[var(--on-surface-variant)]"
                  >
                    {item}
                  </p>
                ))}
              </div>
            </div>

            <div className="mt-5">
              <div className="font-label text-[10px] uppercase tracking-[0.22em] text-[var(--outline)]">
                Game Plan
              </div>
              <div className="mt-3 space-y-2">
                {matchup.game_plan.map((step) => (
                  <p
                    key={step}
                    className="rounded-xl bg-[var(--secondary-fixed)]/60 px-3 py-2 text-sm text-[var(--on-surface)]"
                  >
                    {step}
                  </p>
                ))}
              </div>
            </div>

            <div className="mt-5">
              <div className="font-label text-[10px] uppercase tracking-[0.22em] text-[var(--outline)]">
                Danger Checklist
              </div>
              <div className="mt-3 space-y-2">
                {matchup.danger_checklist.map((step) => (
                  <p
                    key={step}
                    className="rounded-xl bg-[var(--error-container)]/50 px-3 py-2 text-sm text-[var(--on-surface)]"
                  >
                    {step}
                  </p>
                ))}
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
