from app.services.showdown_parser import parse_showdown_team


def test_parse_showdown_team_reads_multiple_members() -> None:
    team = parse_showdown_team(
        """Flutter Mane @ Focus Sash
Ability: Protosynthesis
Tera Type: Fairy
EVs: 4 HP / 252 SpA / 252 Spe
- Moonblast
- Shadow Ball
- Icy Wind
- Protect

Incineroar @ Sitrus Berry
Ability: Intimidate
Tera Type: Grass
- Fake Out
- Flare Blitz
- Knock Off
- Parting Shot
"""
    )

    assert len(team) == 2
    assert team[0].name == "Flutter Mane"
    assert team[0].item == "Focus Sash"
    assert team[0].tera_type == "Fairy"
    assert team[0].moves == ["Moonblast", "Shadow Ball", "Icy Wind", "Protect"]
    assert team[0].evs == {"hp": 4, "spa": 252, "spe": 252}
    assert team[1].name == "Incineroar"
    assert team[1].ability == "Intimidate"

