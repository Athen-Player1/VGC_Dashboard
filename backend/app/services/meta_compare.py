from __future__ import annotations

from app.models.schemas import MatchupSummaryResponse, TeamResponse
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
        game_plan = _build_game_plan(meta_team["plan"], team_analysis.recommendations, suggested_leads)
        overview = _build_overview(meta_team["name"], danger_level, focus_points)

        summaries.append(
            MatchupSummaryResponse(
                meta_team_id=meta_team["id"],
                meta_team_name=meta_team["name"],
                danger_level=danger_level,
                overview=overview,
                focus_points=focus_points[:3],
                suggested_leads=suggested_leads[:3],
                game_plan=game_plan[:4],
                danger_points=danger_points[:3],
            )
        )

    return sorted(
        summaries,
        key=lambda summary: (
            {"High": 0, "Medium": 1, "Low": 2}[summary.danger_level],
            summary.meta_team_name,
        ),
    )


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


def _build_overview(meta_team_name: str, danger_level: str, focus_points: list[str]) -> str:
    if focus_points:
        return f"{meta_team_name} currently reads as a {danger_level.lower()}-pressure matchup. {focus_points[0]}"

    return f"{meta_team_name} currently reads as a {danger_level.lower()}-pressure matchup from the first deterministic pass."
