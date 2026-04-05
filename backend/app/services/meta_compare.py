from __future__ import annotations

from collections import defaultdict

from app.models.schemas import ArchetypeMatchupResponse, MatchupSummaryResponse, TeamResponse
from app.services.meta_store import get_active_meta_snapshot
from app.services.team_analysis import build_team_analysis

PRESSURE_TYPE_MAP = {
    "ground": "Ground",
    "dragon": "Dragon",
    "water": "Water",
    "electric": "Electric",
    "fire": "Fire",
    "fairy": "Fairy",
    "ghost": "Ghost",
    "ice": "Ice",
    "dark": "Dark",
    "fighting": "Fighting",
    "rock": "Rock",
}

SUPPORT_MOVES = {"Fake Out", "Follow Me", "Rage Powder", "Icy Wind", "Tailwind", "Trick Room", "Thunder Wave"}


def build_meta_matchups(team: TeamResponse) -> list[MatchupSummaryResponse]:
    active_snapshot = get_active_meta_snapshot()
    team_analysis = build_team_analysis(team)
    team_names = {member.name.lower() for member in team.members if member.name}

    summaries: list[MatchupSummaryResponse] = []
    for meta_team in active_snapshot["metaTeams"]:
        pressure_types = _extract_pressure_types(meta_team["pressurePoints"])
        exposed_types = [entry.type for entry in team_analysis.shared_weaknesses]
        direct_overlap = sorted(team_names.intersection({name.lower() for name in meta_team["core"]}))
        overlap_count = len([pressure_type for pressure_type in pressure_types if pressure_type in exposed_types])

        danger_score = overlap_count * 2 + len(direct_overlap)
        if danger_score >= 4:
            danger_level = "High"
        elif danger_score >= 2:
            danger_level = "Medium"
        else:
            danger_level = "Low"

        suggested_leads = _suggest_leads(team, pressure_types)
        focus_points = _build_focus_points(team_analysis, meta_team["pressurePoints"], direct_overlap)
        danger_points = _build_danger_points(team_analysis, pressure_types, direct_overlap)
        preserve_targets = _build_preserve_targets(team, pressure_types, meta_team["pressurePoints"])
        win_conditions = _build_win_conditions(team, suggested_leads, direct_overlap)
        tera_notes = _build_tera_notes(team, pressure_types)
        game_plan = _build_game_plan(meta_team["plan"], team_analysis.recommendations, suggested_leads)
        danger_checklist = _build_danger_checklist(team_analysis, pressure_types, meta_team["pressurePoints"])
        overview = _build_overview(meta_team["name"], danger_level, focus_points)

        summaries.append(
            MatchupSummaryResponse(
                meta_team_id=meta_team["id"],
                meta_team_name=meta_team["name"],
                danger_level=danger_level,
                overview=overview,
                focus_points=focus_points[:3],
                suggested_leads=suggested_leads[:3],
                preserve_targets=preserve_targets[:3],
                win_conditions=win_conditions[:3],
                tera_notes=tera_notes[:3],
                game_plan=game_plan[:4],
                danger_points=danger_points[:3],
                danger_checklist=danger_checklist[:4],
            )
        )

    return sorted(
        summaries,
        key=lambda summary: (
            {"High": 0, "Medium": 1, "Low": 2}[summary.danger_level],
            summary.meta_team_name,
        ),
    )


def build_archetype_matchups(team: TeamResponse) -> list[ArchetypeMatchupResponse]:
    active_snapshot = get_active_meta_snapshot()
    grouped: dict[str, list[dict]] = defaultdict(list)
    for meta_team in active_snapshot["metaTeams"]:
        grouped[meta_team["archetype"]].append(meta_team)

    team_analysis = build_team_analysis(team)
    summaries: list[ArchetypeMatchupResponse] = []
    for archetype, teams in grouped.items():
        pressure_points = _dedupe(
            [point for meta_team in teams for point in meta_team["pressurePoints"]]
        )
        pressure_types = _extract_pressure_types(pressure_points)
        suggested_leads = _suggest_leads(team, pressure_types)
        focus_points = _build_focus_points(team_analysis, pressure_points, [])
        game_plan = _build_game_plan(
            [step for meta_team in teams[:2] for step in meta_team["plan"][:1]],
            team_analysis.recommendations,
            suggested_leads,
        )
        overview = (
            f"{archetype} appears {len(teams)} time(s) in the active snapshot. "
            f"Use this as the shared prep plan before drilling into individual teams."
        )
        summaries.append(
            ArchetypeMatchupResponse(
                archetype=archetype,
                team_count=len(teams),
                representative_teams=[meta_team["name"] for meta_team in teams[:3]],
                overview=overview,
                focus_points=focus_points[:3],
                suggested_leads=suggested_leads[:3],
                game_plan=game_plan[:4],
            )
        )

    return sorted(summaries, key=lambda item: (-item.team_count, item.archetype))


def _extract_pressure_types(pressure_points: list[str]) -> list[str]:
    found: list[str] = []
    joined = " ".join(pressure_points).lower()
    for keyword, attack_type in PRESSURE_TYPE_MAP.items():
        if keyword in joined:
            found.append(attack_type)
    return found


def _suggest_leads(team: TeamResponse, pressure_types: list[str]) -> list[str]:
    scored_members: list[tuple[int, str]] = []
    for member in team.members:
        if not member.name:
            continue

        score = 0
        move_set = set(member.moves)
        if SUPPORT_MOVES.intersection(move_set):
            score += 3
        if "Protect" in move_set:
            score += 1
        if "Intimidate" in member.ability:
            score += 2
        if any(member_type in {"Water", "Grass", "Flying", "Fairy", "Steel"} for member_type in member.types):
            score += 1
        if any(pressure_type in {"Ground", "Dragon", "Water"} for pressure_type in pressure_types):
            if any(member_type in {"Water", "Grass", "Flying", "Fairy"} for member_type in member.types):
                score += 2

        scored_members.append((score, member.name))

    scored_members.sort(key=lambda item: (-item[0], item[1]))
    return [name for _, name in scored_members[:2]]


def _build_focus_points(team_analysis, pressure_points: list[str], direct_overlap: list[str]) -> list[str]:
    focus_points: list[str] = []

    if direct_overlap:
        focus_points.append(
            f"Shared core pieces detected: {', '.join(name.title() for name in direct_overlap)}. Mirror-tech and speed ties matter more here."
        )

    if pressure_points:
        focus_points.append(
            f"The opposing shell advertises pressure through {', '.join(pressure_points[:2]).lower()}."
        )

    if team_analysis.coverage_checks:
        ready_checks = [check.label.lower() for check in team_analysis.coverage_checks if check.status == "ready"]
        if ready_checks:
            focus_points.append(
                f"Your cleanest structural tools in this pairing are {', '.join(ready_checks[:2])}."
            )

    return focus_points


def _build_danger_points(team_analysis, pressure_types: list[str], direct_overlap: list[str]) -> list[str]:
    danger_points: list[str] = []

    for weakness in team_analysis.shared_weaknesses:
        if weakness.type in pressure_types:
            danger_points.append(
                f"{weakness.type} pressure is dangerous because {weakness.weak_count} members are exposed."
            )

    if direct_overlap:
        danger_points.append("Mirror structures reduce surprise value, so small positioning mistakes are punished harder.")

    if not danger_points:
        danger_points.append("No immediate structural red flag stands out, so pilot discipline should matter more than matchup theory.")

    return danger_points


def _build_game_plan(meta_plan: list[str], recommendations: list[str], suggested_leads: list[str]) -> list[str]:
    plan: list[str] = []

    if suggested_leads:
        plan.append(f"Start testing openings around {' + '.join(suggested_leads[:2])}.")

    plan.extend(meta_plan[:2])
    plan.extend(recommendations[:2])

    deduped: list[str] = []
    seen: set[str] = set()
    for step in plan:
        if step not in seen:
            deduped.append(step)
            seen.add(step)

    return deduped


def _build_preserve_targets(team: TeamResponse, pressure_types: list[str], pressure_points: list[str]) -> list[str]:
    preserve: list[str] = []
    joined_pressure = " ".join(pressure_points).lower()
    for member in team.members:
        if not member.name:
            continue

        defending_types = {member_type.title() for member_type in member.types}
        if "Ground" in pressure_types and defending_types.intersection({"Flying", "Grass", "Water"}):
            preserve.append(f"Preserve {member.name} for the Ground-pressure turns.")
        if "Dragon" in pressure_types and "Fairy" in defending_types:
            preserve.append(f"Keep {member.name} healthy to absorb Dragon pressure.")
        if "water" in joined_pressure and defending_types.intersection({"Water", "Grass"}):
            preserve.append(f"{member.name} is important for stabilizing Water-heavy endgames.")

    if not preserve and team.members:
        preserve.append(f"Preserve {team.members[0].name} long enough to keep your primary pressure line online.")

    return _dedupe(preserve)


def _build_win_conditions(team: TeamResponse, suggested_leads: list[str], direct_overlap: list[str]) -> list[str]:
    conditions: list[str] = []
    if suggested_leads:
        conditions.append(f"Use {' + '.join(suggested_leads[:2])} to establish the first favorable board state.")

    heavy_hitters = [member.name for member in team.members if "breaker" in member.role.lower() or "sweeper" in member.role.lower()]
    if heavy_hitters:
        conditions.append(f"Create a clean endgame for {heavy_hitters[0]} once speed control or chip trades are in place.")

    if direct_overlap:
        conditions.append("Win the mirror tempo exchanges instead of assuming your standard line is automatically favored.")

    if not conditions:
        conditions.append("Trade evenly early, then convert your healthier positioning tools into the endgame.")

    return _dedupe(conditions)


def _build_tera_notes(team: TeamResponse, pressure_types: list[str]) -> list[str]:
    notes: list[str] = []
    for member in team.members:
        if not member.name or not member.teraType:
            continue
        tera = member.teraType.title()
        if "Ground" in pressure_types and tera in {"Water", "Grass", "Flying"}:
            notes.append(f"Tera {tera} on {member.name} can patch Ground pressure if you are forced defensive.")
        if "Dragon" in pressure_types and tera == "Fairy":
            notes.append(f"Tera Fairy on {member.name} is a strong emergency line into Dragon pressure.")
        if tera in {"Water", "Grass", "Fairy"}:
            notes.append(f"Tera {tera} on {member.name} is one of your cleaner defensive pivots in this matchup.")

    if not notes:
        notes.append("Avoid spending tera early unless it directly flips a pressure point the snapshot team is built around.")

    return _dedupe(notes)


def _build_danger_checklist(team_analysis, pressure_types: list[str], pressure_points: list[str]) -> list[str]:
    checklist: list[str] = []
    for weakness in team_analysis.shared_weaknesses:
        if weakness.type in pressure_types:
            checklist.append(f"Do not expose multiple {weakness.type}-weak pieces at the same time.")

    for point in pressure_points[:2]:
        checklist.append(f"Respect {point.lower()} from team preview onward.")

    if not checklist:
        checklist.append("This matchup looks manageable structurally, so avoid over-teraing or overextending early.")

    return _dedupe(checklist)


def _build_overview(meta_team_name: str, danger_level: str, focus_points: list[str]) -> str:
    if focus_points:
        return f"{meta_team_name} currently reads as a {danger_level.lower()}-pressure matchup. {focus_points[0]}"

    return f"{meta_team_name} currently reads as a {danger_level.lower()}-pressure matchup from the first deterministic pass."


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped
