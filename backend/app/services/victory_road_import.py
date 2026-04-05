from __future__ import annotations

import re
from collections import Counter
from datetime import date
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

from app.models.schemas import MetaSnapshotCreateRequest, VictoryRoadImportRequest
from app.services.meta_store import create_meta_snapshot


def import_victory_road_snapshot(payload: VictoryRoadImportRequest) -> dict:
    html = _fetch_html(payload.url)
    soup = BeautifulSoup(html, "html.parser")

    title = _extract_title(soup)
    imported_rows = _extract_top_cut_rows(soup)
    if not imported_rows:
        raise HTTPException(status_code=422, detail="No tournament rows found on the provided Victory Road page")

    snapshot_date = payload.snapshotDate or _extract_snapshot_date(soup) or date.today().isoformat()
    snapshot_id = _build_snapshot_id(title, snapshot_date)
    source = f"Victory Road import from {payload.url}"

    threats = _build_threats(imported_rows)
    meta_teams = _build_meta_teams(imported_rows, payload.format)
    weakness_summary = _build_weakness_summary(imported_rows)
    recommendations = _build_recommendations(imported_rows)

    snapshot_payload = MetaSnapshotCreateRequest(
        id=snapshot_id,
        format=payload.format,
        source=source,
        snapshotDate=snapshot_date,
        active=payload.active,
        weaknessSummary=weakness_summary,
        recommendations=recommendations,
        threats=threats,
        metaTeams=meta_teams,
    )

    return create_meta_snapshot(snapshot_payload)


def _fetch_html(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
      raise HTTPException(status_code=400, detail="Only http and https URLs are supported")

    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "VGC-Dashboard/1.0 meta snapshot importer"},
    )
    response.raise_for_status()
    return response.text


def _extract_title(soup: BeautifulSoup) -> str:
    for selector in ["h1.entry-title", "h1", "title"]:
        node = soup.select_one(selector)
        if node and node.get_text(strip=True):
            return node.get_text(strip=True)
    return "Victory Road Event"


def _extract_snapshot_date(soup: BeautifulSoup) -> str | None:
    time_tag = soup.find("time")
    if time_tag:
        datetime_value = time_tag.get("datetime")
        if datetime_value:
            return datetime_value[:10]
    return None


def _extract_top_cut_rows(soup: BeautifulSoup) -> list[dict]:
    table = soup.select_one("table.infobox2")
    if table is None:
        return []

    rows: list[dict] = []
    for row in table.select("tbody tr"):
        columns = row.find_all("td")
        if len(columns) < 6:
            continue

        player = columns[3].get_text(" ", strip=True)
        record = columns[1].get_text(" ", strip=True)
        team_column = columns[5]
        team = [
            image.get("title", "").strip()
            for image in team_column.find_all("img")
            if image.get("title")
        ]
        ots_link = ""
        if len(columns) > 6:
            link = columns[6].find("a")
            if link and link.get("href"):
                ots_link = link["href"]

        if not player or not team:
            continue

        rows.append({"player": player, "record": record, "team": team, "ots": ots_link})

    return rows


def _build_snapshot_id(title: str, snapshot_date: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return f"{slug[:80]}-{snapshot_date}"


def _build_threats(rows: list[dict]) -> list[dict]:
    usage = Counter(mon for row in rows for mon in row["team"])
    total_rows = max(len(rows), 1)
    threats: list[dict] = []
    for name, count in usage.most_common(5):
        if count / total_rows >= 0.75:
            level = "High"
        elif count / total_rows >= 0.4:
            level = "Medium"
        else:
            level = "Low"

        threats.append(
            {
                "name": name,
                "threatLevel": level,
                "reason": f"{name} appeared on {count} of {total_rows} imported top-cut teams.",
                "counterplay": f"Prepare a tested line for {name} before trusting this snapshot in matchup planning.",
            }
        )

    return threats


def _build_meta_teams(rows: list[dict], format_name: str) -> list[dict]:
    teams: list[dict] = []
    for index, row in enumerate(rows[:8], start=1):
        core = row["team"][:4]
        pressure_points = _infer_pressure_points(row["team"])
        plan = [
            f"Expect {row['player']} to lean on {' / '.join(core[:2])} as the first positioning engine.",
            f"Respect the published OTS line before committing your defensive tera. OTS: {row['ots'] or 'not available'}",
            f"Start prep by testing your default lead into {' / '.join(core[:2])}.",
        ]
        teams.append(
            {
                "id": f"vr-{index}-{_slugify(row['player'])}",
                "name": row["player"],
                "format": format_name,
                "archetype": _infer_archetype(row["team"]),
                "core": core,
                "pressurePoints": pressure_points,
                "plan": plan,
            }
        )
    return teams


def _build_weakness_summary(rows: list[dict]) -> list[str]:
    usage = Counter(mon for row in rows for mon in row["team"])
    common = [name for name, _ in usage.most_common(3)]
    return [
        f"Imported snapshot built from {len(rows)} top-cut teams.",
        f"Most common Pokemon in this event snapshot: {', '.join(common)}." if common else "No common-Pokemon note available.",
        "Use this as a dated event snapshot rather than a universal ladder truth.",
        "If the event OTS links are present, matchup planning can key off published tournament teams instead of guesses.",
    ]


def _build_recommendations(rows: list[dict]) -> list[str]:
    top_row = rows[0]
    lead_core = " / ".join(top_row["team"][:2])
    return [
        f"Start prep by testing your main lead into the winning core of {lead_core}.",
        "Focus your first matchup plans on the most repeated cores rather than every fringe top-cut team equally.",
        "Use tournament-result snapshots as the primary source of truth, then layer Showdown usage only as a secondary trend signal.",
        "Re-import fresh event pages as the format evolves so dated snapshots stay explicit.",
    ]


def _infer_pressure_points(team: list[str]) -> list[str]:
    names = {name.lower() for name in team}
    points: list[str] = []
    if {"incineroar", "rillaboom"} & names:
        points.append("pivot attrition")
    if {"landorus therian", "landorus"} & names:
        points.append("ground spread pressure")
    if {"flutter mane", "calyrex shadow rider", "calyrex-shadow"} & names:
        points.append("fast special pressure")
    if {"farigiraf", "ursaluna bloodmoon", "torkoal"} & names:
        points.append("trick room endgames")
    if {"urshifu rapid", "urshifu-rapid-strike", "ogerpon wellspring", "ogerpon-w"} & names:
        points.append("water pressure")
    if not points:
        points.append("high-level open team sheet pressure")
    return points


def _infer_archetype(team: list[str]) -> str:
    joined = " ".join(name.lower() for name in team)
    if "farigiraf" in joined or "bloodmoon" in joined or "torkoal" in joined:
        return "Trick Room"
    if "koraidon" in joined or "groudon" in joined or "torkoal" in joined:
        return "Sun"
    if "miraidon" in joined:
        return "Electric offense"
    return "Tournament balance"


def _slugify(value: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")
