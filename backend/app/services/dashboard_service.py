from app.services.meta_store import get_active_meta_snapshot
from app.services.team_store import list_teams


def build_dashboard_payload() -> dict:
    active_snapshot = get_active_meta_snapshot()

    return {
        "activeFormat": active_snapshot["format"],
        "teams": list_teams(),
        "threats": active_snapshot["threats"],
        "weaknessSummary": active_snapshot["weaknessSummary"],
        "recommendations": active_snapshot["recommendations"],
        "metaTeams": active_snapshot["metaTeams"],
    }
