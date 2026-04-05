import { ArchetypeMatchup } from "@/lib/types";

export function ArchetypeMatchupPanel({
  teamName,
  matchups
}: {
  teamName: string;
  matchups: ArchetypeMatchup[];
}) {
  return (
    <section className="rounded-[1.5rem] bg-white p-8 shadow-sm">
      <div>
        <div className="font-label text-[11px] font-bold uppercase tracking-[0.32em] text-[var(--secondary)]">
          Common Archetypes
        </div>
        <h2 className="mt-2 font-headline text-2xl font-bold">
          Archetype Prep for {teamName}
        </h2>
        <p className="mt-2 text-sm text-[var(--on-surface-variant)]">
          Shared plans for repeated archetypes in the active snapshot, so you can prep broad lines
          before drilling into individual top teams.
        </p>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        {matchups.map((matchup) => (
          <article
            key={matchup.archetype}
            className="rounded-[1.25rem] bg-[var(--surface-container-low)] p-6"
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="font-headline text-xl font-bold">{matchup.archetype}</h3>
                <p className="mt-2 text-sm text-[var(--on-surface-variant)]">{matchup.overview}</p>
              </div>
              <span className="rounded-full bg-white px-3 py-1 font-label text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--secondary)]">
                {matchup.team_count} team{matchup.team_count === 1 ? "" : "s"}
              </span>
            </div>

            <div className="mt-5">
              <div className="font-label text-[10px] uppercase tracking-[0.22em] text-[var(--outline)]">
                Representative Teams
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                {matchup.representative_teams.map((team) => (
                  <span
                    key={team}
                    className="rounded-full bg-white px-3 py-1 text-[11px] font-semibold text-[var(--on-surface-variant)]"
                  >
                    {team}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-5">
              <div className="font-label text-[10px] uppercase tracking-[0.22em] text-[var(--outline)]">
                Suggested Leads
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                {matchup.suggested_leads.map((lead) => (
                  <span
                    key={lead}
                    className="rounded-full bg-[var(--secondary-fixed)]/60 px-3 py-1 text-[11px] font-semibold text-[var(--on-surface)]"
                  >
                    {lead}
                  </span>
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
                    className="rounded-xl bg-[var(--secondary-fixed)]/50 px-3 py-2 text-sm text-[var(--on-surface)]"
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
