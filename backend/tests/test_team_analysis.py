import pytest

from app.models.schemas import TeamMember, TeamResponse
from app.services.team_analysis import build_team_analysis
from app.services.victory_road_import import _build_recommendations


def _member(
    name: str,
    *,
    item: str = "",
    ability: str = "",
    types: list[str] | None = None,
    moves: list[str] | None = None,
    role: str = "",
    tera_type: str | None = None,
) -> TeamMember:
    return TeamMember(
        name=name,
        item=item,
        ability=ability,
        types=types or [],
        moves=moves or [],
        role=role,
        teraType=tera_type,
        image="",
    )


def _assert_coherent_mode(team: TeamResponse, expected_mode: str, forbidden_phrase: str) -> None:
    analysis = build_team_analysis(team)

    mode_check = next(check for check in analysis.coverage_checks if check.label == "Mode cohesion")
    assert mode_check.status == "ready"
    assert expected_mode.lower() in mode_check.detail.lower()
    assert not any(forbidden_phrase.lower() in item.lower() for item in analysis.recommendations)
    assert not any(forbidden_phrase.lower() in item.lower() for item in analysis.warnings)


def test_team_analysis_marks_coherent_sun_mode_ready() -> None:
    team = TeamResponse(
        id="sun-mode",
        name="Sun Mode",
        format="Regulation H",
        archetype="Sun",
        notes="",
        members=[
            _member("Torkoal", item="Charcoal", ability="Drought", types=["Fire"], moves=["Eruption", "Protect"], role="Sun setter"),
            _member("Flutter Mane", item="Focus Sash", ability="Protosynthesis", types=["Ghost", "Fairy"], moves=["Moonblast", "Icy Wind", "Protect"], role="Speed control"),
            _member("Lilligant", item="Focus Sash", ability="Chlorophyll", types=["Grass"], moves=["Sleep Powder", "After You", "Leaf Storm", "Protect"], role="Sun support"),
            _member("Incineroar", item="Sitrus Berry", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Flare Blitz", "Knock Off"], role="Pivot"),
            _member("Ogerpon-W", item="Wellspring Mask", ability="Water Absorb", types=["Grass", "Water"], moves=["Ivy Cudgel", "Follow Me", "Spiky Shield", "Horn Leech"], role="Support"),
            _member("Landorus-Therian", item="Choice Scarf", ability="Intimidate", types=["Ground", "Flying"], moves=["Stomping Tantrum", "U-turn", "Rock Slide", "Tera Blast"], role="Pivot"),
        ],
    )

    analysis = build_team_analysis(team)

    mode_check = next(check for check in analysis.coverage_checks if check.label == "Mode cohesion")
    assert mode_check.status == "ready"
    assert "sun" in mode_check.detail.lower()
    assert not any("reliable sun setter" in item for item in analysis.recommendations)
    assert analysis.recommendation_details
    assert all(detail.summary for detail in analysis.recommendation_details)
    assert all(detail.severity in {"high", "medium", "low"} for detail in analysis.recommendation_details)


def test_team_analysis_flags_unsupported_weather_payoffs() -> None:
    team = TeamResponse(
        id="floating-rain",
        name="Floating Rain",
        format="Regulation H",
        archetype="Balance",
        notes="",
        members=[
            _member("Zapdos", item="Safety Goggles", ability="Pressure", types=["Electric", "Flying"], moves=["Thunder", "Tailwind", "Protect", "Heat Wave"], role="Speed control"),
            _member("Ludicolo", item="Assault Vest", ability="Swift Swim", types=["Water", "Grass"], moves=["Fake Out", "Muddy Water", "Giga Drain", "Ice Beam"], role="Rain payoff"),
            _member("Incineroar", item="Sitrus Berry", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Flare Blitz", "Knock Off"], role="Pivot"),
            _member("Amoonguss", item="Rocky Helmet", ability="Regenerator", types=["Grass", "Poison"], moves=["Rage Powder", "Spore", "Pollen Puff", "Protect"], role="Support"),
            _member("Garchomp", item="Clear Amulet", ability="Rough Skin", types=["Dragon", "Ground"], moves=["Stomping Tantrum", "Protect", "Dragon Claw", "Rock Slide"], role="Breaker"),
            _member("Gholdengo", item="Leftovers", ability="Good as Gold", types=["Steel", "Ghost"], moves=["Make It Rain", "Shadow Ball", "Protect", "Nasty Plot"], role="Special breaker"),
        ],
    )

    analysis = build_team_analysis(team)

    assert any("reliable rain setter" in item for item in analysis.recommendations)
    assert any("rain payoffs without a reliable setter" in item for item in analysis.warnings)
    assert any(detail.category == "mode" for detail in analysis.recommendation_details)
    assert any("rain" in detail.summary.lower() for detail in analysis.recommendation_details)


def test_team_analysis_rain_shell_does_not_create_fake_sun_mode_from_weather_ball() -> None:
    team = TeamResponse(
        id="clean-rain",
        name="Clean Rain",
        format="Regulation H",
        archetype="Rain",
        notes="",
        members=[
            _member("Pelipper", item="Damp Rock", ability="Drizzle", types=["Water", "Flying"], moves=["Weather Ball", "Hurricane", "U-turn", "Protect"], role="Rain setter"),
            _member("Ludicolo", item="Life Orb", ability="Swift Swim", types=["Water", "Grass"], moves=["Hydro Pump", "Ice Beam", "Energy Ball", "Protect"], role="Rain payoff"),
            _member("Kingdra", item="Choice Specs", ability="Swift Swim", types=["Water", "Dragon"], moves=["Hydro Pump", "Draco Meteor", "Surf", "Ice Beam"], role="Rain payoff"),
            _member("Floatzel", item="Choice Band", ability="Swift Swim", types=["Water"], moves=["Waterfall", "Aqua Jet", "Ice Spinner", "Crunch"], role="Rain payoff"),
            _member("Jolteon", item="Assault Vest", ability="Volt Absorb", types=["Electric"], moves=["Thunder", "Rain Dance", "Shadow Ball", "Alluring Voice"], role="Rain support"),
            _member("Swampert", item="Mystic Water", ability="Damp", types=["Water", "Ground"], moves=["Waterfall", "Earthquake", "Ice Punch", "Protect"], role="Breaker"),
        ],
    )

    analysis = build_team_analysis(team)

    mode_check = next(check for check in analysis.coverage_checks if check.label == "Mode cohesion")
    assert mode_check.status == "ready"
    assert "rain" in mode_check.detail.lower()
    assert not any("reliable sun setter" in item.lower() for item in analysis.recommendations)
    assert not any("sun" in item.lower() for item in analysis.warnings)


def test_team_analysis_weather_speed_package_counts_as_speed_control() -> None:
    team = TeamResponse(
        id="rain-speed",
        name="Rain Speed",
        format="Regulation H",
        archetype="Rain",
        notes="",
        members=[
            _member("Pelipper", item="Damp Rock", ability="Drizzle", types=["Water", "Flying"], moves=["Hurricane", "U-turn", "Protect", "Wide Guard"], role="Rain setter"),
            _member("Kingdra", item="Choice Specs", ability="Swift Swim", types=["Water", "Dragon"], moves=["Hydro Pump", "Draco Meteor", "Surf", "Ice Beam"], role="Rain payoff"),
            _member("Ludicolo", item="Life Orb", ability="Swift Swim", types=["Water", "Grass"], moves=["Hydro Pump", "Ice Beam", "Fake Out", "Protect"], role="Rain payoff"),
            _member("Archaludon", item="Assault Vest", ability="Stamina", types=["Steel", "Dragon"], moves=["Electro Shot", "Flash Cannon", "Draco Meteor", "Body Press"], role="Breaker"),
            _member("Rillaboom", item="Miracle Seed", ability="Grassy Surge", types=["Grass"], moves=["Fake Out", "Wood Hammer", "Grassy Glide", "U-turn"], role="Support"),
            _member("Incineroar", item="Safety Goggles", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Knock Off", "Flare Blitz"], role="Pivot"),
        ],
    )

    analysis = build_team_analysis(team)

    speed_check = next(check for check in analysis.coverage_checks if check.label == "Speed control")
    assert speed_check.status == "ready"
    assert "weather-enabled speed packages" in speed_check.detail
    assert not any("Add Icy Wind, Tailwind, Trick Room, Thunder Wave" in item for item in analysis.recommendations)
    assert any("Examples:" in detail.suggestedFix for detail in analysis.recommendation_details)


def test_team_analysis_recommendations_include_examples_for_missing_support() -> None:
    team = TeamResponse(
        id="support-gap",
        name="Support Gap",
        format="Regulation H",
        archetype="Balance",
        notes="",
        members=[
            _member("Gholdengo", item="Leftovers", ability="Good as Gold", types=["Steel", "Ghost"], moves=["Make It Rain", "Shadow Ball", "Nasty Plot", "Protect"], role="Special breaker"),
            _member("Hydreigon", item="Life Orb", ability="Levitate", types=["Dark", "Dragon"], moves=["Draco Meteor", "Dark Pulse", "Heat Wave", "Protect"], role="Breaker"),
            _member("Rotom-Wash", item="Sitrus Berry", ability="Levitate", types=["Electric", "Water"], moves=["Hydro Pump", "Thunderbolt", "Protect", "Will-O-Wisp"], role="Pivot"),
            _member("Ogerpon-Wellspring", item="Wellspring Mask", ability="Water Absorb", types=["Grass", "Water"], moves=["Ivy Cudgel", "Horn Leech", "Spiky Shield", "Taunt"], role="Pressure"),
            _member("Dragonite", item="Choice Band", ability="Inner Focus", types=["Dragon", "Flying"], moves=["Extreme Speed", "Low Kick", "Ice Spinner", "Stomping Tantrum"], role="Cleaner"),
            _member("Heatran", item="Shuca Berry", ability="Flash Fire", types=["Fire", "Steel"], moves=["Heat Wave", "Flash Cannon", "Earth Power", "Protect"], role="Bulky offense"),
        ],
    )

    analysis = build_team_analysis(team)

    support_detail = next(detail for detail in analysis.recommendation_details if detail.category == "support")
    assert "Incineroar or Iron Hands for Fake Out" in support_detail.suggestedFix


def test_team_analysis_flags_single_source_support_dependency() -> None:
    team = TeamResponse(
        id="one-fake-out",
        name="One Fake Out",
        format="Regulation H",
        archetype="Balance",
        notes="",
        members=[
            _member("Incineroar", item="Safety Goggles", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Knock Off", "Flare Blitz"], role="Pivot"),
            _member("Gholdengo", item="Leftovers", ability="Good as Gold", types=["Steel", "Ghost"], moves=["Make It Rain", "Shadow Ball", "Protect", "Nasty Plot"], role="Special breaker"),
            _member("Hydreigon", item="Life Orb", ability="Levitate", types=["Dark", "Dragon"], moves=["Draco Meteor", "Dark Pulse", "Protect", "Heat Wave"], role="Breaker"),
            _member("Ogerpon-Wellspring", item="Wellspring Mask", ability="Water Absorb", types=["Grass", "Water"], moves=["Ivy Cudgel", "Horn Leech", "Spiky Shield", "Taunt"], role="Pressure"),
            _member("Raging Bolt", item="Assault Vest", ability="Protosynthesis", types=["Electric", "Dragon"], moves=["Thunderclap", "Draco Meteor", "Snarl", "Volt Switch"], role="Bulky offense"),
            _member("Heatran", item="Shuca Berry", ability="Flash Fire", types=["Fire", "Steel"], moves=["Heat Wave", "Flash Cannon", "Earth Power", "Protect"], role="Bulky offense"),
        ],
    )

    analysis = build_team_analysis(team)

    assert any("single source" in warning.lower() and "fake out" in warning.lower() for warning in analysis.warnings)
    support_detail = next(
        detail for detail in analysis.recommendation_details if detail.category == "support" and "backup fake out line" in detail.summary.lower()
    )
    assert support_detail.affectedMembers == ["Incineroar"]


def test_team_analysis_flags_overloaded_primary_lead_pair() -> None:
    team = TeamResponse(
        id="lead-burden",
        name="Lead Burden",
        format="Regulation H",
        archetype="Balance",
        notes="",
        members=[
            _member("Incineroar", item="Safety Goggles", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Protect", "Flare Blitz"], role="Pivot"),
            _member("Tornadus", item="Covert Cloak", ability="Prankster", types=["Flying"], moves=["Tailwind", "Taunt", "Protect", "Bleakwind Storm"], role="Speed control"),
            _member("Gholdengo", item="Life Orb", ability="Good as Gold", types=["Steel", "Ghost"], moves=["Make It Rain", "Shadow Ball", "Nasty Plot", "Protect"], role="Special breaker"),
            _member("Dragonite", item="Choice Band", ability="Inner Focus", types=["Dragon", "Flying"], moves=["Extreme Speed", "Ice Spinner", "Low Kick", "Stomping Tantrum"], role="Cleaner"),
            _member("Heatran", item="Shuca Berry", ability="Flash Fire", types=["Fire", "Steel"], moves=["Heat Wave", "Flash Cannon", "Earth Power", "Protect"], role="Bulky offense"),
            _member("Rillaboom", item="Miracle Seed", ability="Grassy Surge", types=["Grass"], moves=["Wood Hammer", "Grassy Glide", "Protect", "Knock Off"], role="Support"),
        ],
    )

    analysis = build_team_analysis(team)

    lead_detail = next(detail for detail in analysis.recommendation_details if detail.category == "lead-plan")
    assert "Incineroar + Tornadus" in lead_detail.summary
    assert lead_detail.affectedMembers == ["Incineroar", "Tornadus"]


def test_team_analysis_flags_primary_weakness_tera_dependency() -> None:
    team = TeamResponse(
        id="ground-tera-tax",
        name="Ground Tera Tax",
        format="Regulation H",
        archetype="Balance",
        notes="",
        members=[
            _member("Incineroar", item="Safety Goggles", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Knock Off", "Flare Blitz"], role="Pivot", tera_type="Grass"),
            _member("Heatran", item="Leftovers", ability="Flash Fire", types=["Fire", "Steel"], moves=["Heat Wave", "Earth Power", "Protect", "Flash Cannon"], role="Bulky offense"),
            _member("Gholdengo", item="Life Orb", ability="Good as Gold", types=["Steel", "Ghost"], moves=["Make It Rain", "Shadow Ball", "Nasty Plot", "Protect"], role="Special breaker"),
            _member("Raging Bolt", item="Assault Vest", ability="Protosynthesis", types=["Electric", "Dragon"], moves=["Thunderclap", "Draco Meteor", "Snarl", "Volt Switch"], role="Bulky offense"),
            _member("Amoonguss", item="Rocky Helmet", ability="Regenerator", types=["Grass", "Poison"], moves=["Rage Powder", "Spore", "Pollen Puff", "Protect"], role="Support"),
            _member("Ogerpon-Wellspring", item="Wellspring Mask", ability="Water Absorb", types=["Grass", "Water"], moves=["Ivy Cudgel", "Horn Leech", "Spiky Shield", "Follow Me"], role="Support"),
        ],
    )

    analysis = build_team_analysis(team)

    tera_detail = next(detail for detail in analysis.recommendation_details if detail.category == "tera-dependency")
    assert "Ground" in tera_detail.summary
    assert tera_detail.affectedMembers == ["Incineroar"]


@pytest.mark.parametrize(
    ("team", "expected_mode", "forbidden_phrase"),
    [
        (
            TeamResponse(
                id="sand-mode",
                name="Sand Mode",
                format="Regulation H",
                archetype="Sand",
                notes="",
                members=[
                    _member("Tyranitar", item="Assault Vest", ability="Sand Stream", types=["Rock", "Dark"], moves=["Rock Slide", "Knock Off", "Low Kick", "Protect"], role="Sand setter"),
                    _member("Excadrill", item="Clear Amulet", ability="Sand Rush", types=["Ground", "Steel"], moves=["High Horsepower", "Iron Head", "Protect", "Rock Slide"], role="Sand payoff"),
                    _member("Landorus-Therian", item="Choice Scarf", ability="Intimidate", types=["Ground", "Flying"], moves=["Stomping Tantrum", "U-turn", "Rock Slide", "Tera Blast"], role="Pivot"),
                    _member("Amoonguss", item="Rocky Helmet", ability="Regenerator", types=["Grass", "Poison"], moves=["Spore", "Rage Powder", "Pollen Puff", "Protect"], role="Support"),
                    _member("Incineroar", item="Safety Goggles", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Flare Blitz", "Knock Off"], role="Pivot"),
                    _member("Raging Bolt", item="Leftovers", ability="Protosynthesis", types=["Electric", "Dragon"], moves=["Thunderclap", "Draco Meteor", "Protect", "Snarl"], role="Bulky offense"),
                ],
            ),
            "sand",
            "reliable sand setter",
        ),
        (
            TeamResponse(
                id="snow-mode",
                name="Snow Mode",
                format="Regulation H",
                archetype="Snow",
                notes="",
                members=[
                    _member("Ninetales-Alola", item="Light Clay", ability="Snow Warning", types=["Ice", "Fairy"], moves=["Aurora Veil", "Blizzard", "Moonblast", "Protect"], role="Snow setter"),
                    _member("Baxcalibur", item="Loaded Dice", ability="Thermal Exchange", types=["Dragon", "Ice"], moves=["Icicle Spear", "Ice Shard", "Protect", "Glaive Rush"], role="Snow payoff"),
                    _member("Cetitan", item="Assault Vest", ability="Slush Rush", types=["Ice"], moves=["Icicle Crash", "Ice Spinner", "Heavy Slam", "Liquidation"], role="Snow payoff"),
                    _member("Amoonguss", item="Rocky Helmet", ability="Regenerator", types=["Grass", "Poison"], moves=["Spore", "Rage Powder", "Pollen Puff", "Protect"], role="Support"),
                    _member("Incineroar", item="Safety Goggles", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Flare Blitz", "Knock Off"], role="Pivot"),
                    _member("Urshifu-Rapid-Strike", item="Mystic Water", ability="Unseen Fist", types=["Water", "Fighting"], moves=["Surging Strikes", "Close Combat", "Aqua Jet", "Detect"], role="Breaker"),
                ],
            ),
            "snow",
            "reliable snow setter",
        ),
        (
            TeamResponse(
                id="electric-mode",
                name="Electric Mode",
                format="Regulation H",
                archetype="Electric Terrain",
                notes="",
                members=[
                    _member("Miraidon", item="Life Orb", ability="Hadron Engine", types=["Electric", "Dragon"], moves=["Electro Drift", "Draco Meteor", "Protect", "Volt Switch"], role="Setter"),
                    _member("Iron Hands", item="Assault Vest", ability="Quark Drive", types=["Fighting", "Electric"], moves=["Fake Out", "Drain Punch", "Wild Charge", "Heavy Slam"], role="Terrain payoff"),
                    _member("Iron Bundle", item="Booster Energy", ability="Quark Drive", types=["Ice", "Water"], moves=["Icy Wind", "Freeze-Dry", "Hydro Pump", "Protect"], role="Speed control"),
                    _member("Farigiraf", item="Safety Goggles", ability="Armor Tail", types=["Normal", "Psychic"], moves=["Helping Hand", "Hyper Voice", "Protect", "Dazzling Gleam"], role="Support"),
                    _member("Incineroar", item="Safety Goggles", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Flare Blitz", "Knock Off"], role="Pivot"),
                    _member("Landorus-Therian", item="Choice Scarf", ability="Intimidate", types=["Ground", "Flying"], moves=["Stomping Tantrum", "U-turn", "Rock Slide", "Tera Blast"], role="Pivot"),
                ],
            ),
            "electric terrain",
            "dependable Electric Terrain setter",
        ),
        (
            TeamResponse(
                id="psychic-mode",
                name="Psychic Mode",
                format="Regulation H",
                archetype="Psychic Terrain",
                notes="",
                members=[
                    _member("Indeedee-F", item="Safety Goggles", ability="Psychic Surge", types=["Psychic", "Normal"], moves=["Follow Me", "Helping Hand", "Protect", "Psychic"], role="Setter"),
                    _member("Armarouge", item="Life Orb", ability="Flash Fire", types=["Fire", "Psychic"], moves=["Expanding Force", "Armor Cannon", "Protect", "Wide Guard"], role="Terrain payoff"),
                    _member("Hatterene", item="Leftovers", ability="Magic Bounce", types=["Psychic", "Fairy"], moves=["Dazzling Gleam", "Protect", "Mystical Fire", "Expanding Force"], role="Terrain payoff"),
                    _member("Incineroar", item="Safety Goggles", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Flare Blitz", "Knock Off"], role="Pivot"),
                    _member("Amoonguss", item="Rocky Helmet", ability="Regenerator", types=["Grass", "Poison"], moves=["Spore", "Rage Powder", "Pollen Puff", "Protect"], role="Support"),
                    _member("Urshifu-Rapid-Strike", item="Mystic Water", ability="Unseen Fist", types=["Water", "Fighting"], moves=["Surging Strikes", "Close Combat", "Aqua Jet", "Detect"], role="Breaker"),
                ],
            ),
            "psychic terrain",
            "dependable Psychic Terrain setter",
        ),
        (
            TeamResponse(
                id="room-mode",
                name="Room Mode",
                format="Regulation H",
                archetype="Trick Room",
                notes="",
                members=[
                    _member("Farigiraf", item="Safety Goggles", ability="Armor Tail", types=["Normal", "Psychic"], moves=["Trick Room", "Helping Hand", "Hyper Voice", "Protect"], role="Setter"),
                    _member("Ursaluna-Bloodmoon", item="Life Orb", ability="Mind's Eye", types=["Ground", "Normal"], moves=["Blood Moon", "Earth Power", "Hyper Voice", "Protect"], role="Slow mode payoff"),
                    _member("Torkoal", item="Charcoal", ability="Drought", types=["Fire"], moves=["Eruption", "Heat Wave", "Earth Power", "Protect"], role="Endgame"),
                    _member("Amoonguss", item="Rocky Helmet", ability="Regenerator", types=["Grass", "Poison"], moves=["Spore", "Rage Powder", "Pollen Puff", "Protect"], role="Support"),
                    _member("Iron Hands", item="Assault Vest", ability="Quark Drive", types=["Fighting", "Electric"], moves=["Fake Out", "Drain Punch", "Wild Charge", "Heavy Slam"], role="Bulky endgame"),
                    _member("Incineroar", item="Safety Goggles", ability="Intimidate", types=["Fire", "Dark"], moves=["Fake Out", "Parting Shot", "Flare Blitz", "Knock Off"], role="Pivot"),
                ],
            ),
            "trick room",
            "dedicated Trick Room setter",
        ),
    ],
)
def test_team_analysis_core_strategies_keep_coherent_modes(team: TeamResponse, expected_mode: str, forbidden_phrase: str) -> None:
    _assert_coherent_mode(team, expected_mode, forbidden_phrase)


def test_victory_road_recommendations_reflect_common_modes() -> None:
    rows = [
        {"player": "A", "record": "8-1", "team": ["Torkoal", "Lilligant", "Farigiraf", "Ursaluna-Bloodmoon", "Incineroar", "Amoonguss"], "ots": ""},
        {"player": "B", "record": "8-2", "team": ["Koraidon", "Flutter Mane", "Walking Wake", "Incineroar", "Rillaboom", "Ogerpon-W"], "ots": ""},
        {"player": "C", "record": "7-2", "team": ["Farigiraf", "Torkoal", "Amoonguss", "Iron Hands", "Ursaluna-Bloodmoon", "Pelipper"], "ots": ""},
    ]

    recommendations = _build_recommendations(rows)

    assert any("trick room" in item.lower() or "sun mode" in item.lower() for item in recommendations)
