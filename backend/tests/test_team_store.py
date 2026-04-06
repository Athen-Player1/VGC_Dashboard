from app.services.team_store import _normalize_member, _species_identity, _slugify_species


def test_slugify_species_supports_common_form_aliases() -> None:
    assert _slugify_species("Ogerpon-W") == "ogerpon-wellspring"
    assert _slugify_species("Bloodmoon Ursaluna") == "ursaluna-bloodmoon"
    assert _slugify_species("Landorus") == "landorus-therian"


def test_species_identity_groups_common_aliases() -> None:
    assert _species_identity("Ogerpon-W") == _species_identity("Ogerpon-Wellspring")
    assert _species_identity("Bloodmoon Ursaluna") == _species_identity("Ursaluna-Bloodmoon")
    assert _species_identity("Landorus") == _species_identity("Landorus-Therian")


def test_normalize_member_rebuilds_image_from_current_species() -> None:
    normalized = _normalize_member(
        {
            "name": "Landorus",
            "item": "Choice Scarf",
            "ability": "Intimidate",
            "types": ["Ground", "Flying"],
            "moves": ["Earthquake", "U-turn"],
            "role": "Pivot",
            "teraType": "Poison",
            "image": "https://example.com/stale.png",
        }
    )

    assert normalized["image"].endswith("/landorus-therian.png")
