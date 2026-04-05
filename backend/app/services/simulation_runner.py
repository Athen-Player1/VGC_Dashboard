from __future__ import annotations

import random
from collections import Counter
from typing import Any

from app.models.schemas import TeamResponse
from app.services.meta_compare import build_meta_matchups
from app.services.team_analysis import build_team_analysis
from app.services.team_store import get_team

STATUS_TO_WIN_RATE = {
    "Low": 0.68,
    "Medium": 0.52,
    "High": 0.36,
}


def run_simulation_job(job: dict[str, Any]) -> dict[str, Any]:
    team = TeamResponse.model_validate(get_team(job["team_id"]))
    opponent_payload = job["opponent_payload"]
    requested_games = int(job["requested_games"])

    base_win_rate, context = _calculate_base_win_rate(team, opponent_payload, job["opponent_mode"])
    rng = random.Random(job["id"])

    wins = 0
    losses = 0
    loss_causes: Counter[str] = Counter()
    threat_counts: Counter[str] = Counter()
    sample_logs: list[dict[str, Any]] = []

    for game_index in range(1, requested_games + 1):
        variance = rng.uniform(-0.12, 0.12)
        effective_win_rate = max(0.1, min(0.9, base_win_rate + variance))
        result = "win" if rng.random() <= effective_win_rate else "loss"

        if result == "win":
            wins += 1
            sample_logs.append(
                {
                    "game": game_index,
                    "result": "win",
                    "note": _build_win_note(team, context, rng),
                }
            )
        else:
            losses += 1
            cause = rng.choice(context["loss_causes"])
            loss_causes[cause] += 1
            if context["threats"]:
                threat_counts[rng.choice(context["threats"])] += 1
            sample_logs.append(
                {
                    "game": game_index,
                    "result": "loss",
                    "note": cause,
                }
            )

    repeated_issues = [item for item, _ in loss_causes.most_common(3)]
    top_threats = [item for item, _ in threat_counts.most_common(3)]
    recommendations = _build_recommendations(team, context, repeated_issues)

    return {
        "teamName": team.name,
        "opponentLabel": job["opponent_label"],
        "gamesRequested": requested_games,
        "wins": wins,
        "losses": losses,
        "winRate": round((wins / requested_games) * 100, 1) if requested_games else 0,
        "topThreats": top_threats,
        "repeatedIssues": repeated_issues,
        "recommendations": recommendations,
        "sampleGames": sample_logs[:5],
        "simulationEngine": "heuristic-v1",
        "engineNote": "Phase 6 MVP uses a deterministic background heuristic runner shaped around saved-team analysis and stored meta data. It is designed so a full Pokemon Showdown battle engine can replace the core runner later.",
    }


def _calculate_base_win_rate(
    team: TeamResponse, opponent_payload: dict[str, Any], opponent_mode: str
) -> tuple[float, dict[str, Any]]:
    team_analysis = build_team_analysis(team)
    default_threats = opponent_payload.get("core") or [
        member["name"] for member in opponent_payload.get("members", []) if member.get("name")
    ]

    if opponent_mode == "top_meta":
        meta_matchups = build_meta_matchups(team)
        target_id = opponent_payload.get("metaTeamId")
        matchup = next((item for item in meta_matchups if item.meta_team_id == target_id), None)
        if matchup is None:
            base = 0.5
            loss_causes = [
                "The top snapshot team kept forcing awkward positioning trades.",
                "Their default pressure line stayed ahead of your first pivot cycle.",
            ]
            recommendations = team_analysis.recommendations[:2]
        else:
            base = STATUS_TO_WIN_RATE.get(matchup.danger_level, 0.5)
            loss_causes = matchup.danger_checklist or matchup.danger_points or [
                "The snapshot team kept finding damage into your exposed slots."
            ]
            recommendations = matchup.game_plan[:2] + matchup.preserve_targets[:1]

        return base, {
            "label": opponent_payload.get("name", "Top Meta Team"),
            "threats": default_threats,
            "loss_causes": loss_causes,
            "recommendations": recommendations,
            "strengths": team_analysis.strengths[:2],
        }

    overlap = len(
        {member.name.lower() for member in team.members if member.name}.intersection(
            {name.lower() for name in default_threats}
        )
    )
    support_count = sum(
        1
        for member in team.members
        if {"Fake Out", "Tailwind", "Trick Room", "Icy Wind", "Rage Powder", "Follow Me"}.intersection(
            set(member.moves)
        )
    )
    warnings = len(team_analysis.warnings)
    base = 0.48 + (support_count * 0.03) - (warnings * 0.02) - (overlap * 0.03)
    base = max(0.18, min(0.78, base))
    loss_causes = [
        "The imported opponent forced uncomfortable damage races before your support pieces stabilized.",
        "You lost too many turns respecting their likely tech options from preview.",
        "Their board position snowballed once your first pivot line broke down.",
    ]
    if team_analysis.shared_weaknesses:
        weakness = team_analysis.shared_weaknesses[0].type
        loss_causes.append(f"The opponent repeatedly punished your stacked {weakness} exposure.")

    return base, {
        "label": opponent_payload.get("name", "Imported Team"),
        "threats": default_threats,
        "loss_causes": loss_causes,
        "recommendations": team_analysis.recommendations[:3],
        "strengths": team_analysis.strengths[:2],
    }


def _build_win_note(team: TeamResponse, context: dict[str, Any], rng: random.Random) -> str:
    if context["strengths"]:
        return f"{rng.choice(context['strengths'])} That gave {team.name} enough room to close cleanly."
    return f"{team.name} converted the early board position into a stable endgame."


def _build_recommendations(
    team: TeamResponse, context: dict[str, Any], repeated_issues: list[str]
) -> list[str]:
    recommendations = list(context["recommendations"])
    if repeated_issues:
        recommendations.append(f"Scrim the opening turns until you stop losing to: {repeated_issues[0]}")
    recommendations.append(
        f"Use the Testing lane to rerun {team.name} after each builder adjustment and compare the repeated loss patterns."
    )

    deduped: list[str] = []
    seen: set[str] = set()
    for item in recommendations:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)

    return deduped[:4]
