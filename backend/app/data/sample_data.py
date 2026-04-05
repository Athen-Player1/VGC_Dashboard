dashboard_data = {
    "activeFormat": "Regulation H Snapshot",
    "teams": [
        {
            "id": "sun-offense",
            "name": "Sun Pressure Core",
            "format": "Regulation H",
            "archetype": "Sun Balance",
            "elo": 1658,
            "notes": "Strong into slower balance and redirect-heavy shells, but still wants cleaner counterplay into fast Ground and Dragon pressure.",
            "tags": ["Sun", "Balance", "Open Team Sheet"],
            "members": [
                {
                    "name": "Koraidon",
                    "item": "Clear Amulet",
                    "ability": "Orichalcum Pulse",
                    "types": ["Fire", "Fighting"],
                    "moves": ["Collision Course", "Flare Blitz", "Protect", "Taunt"],
                    "role": "Primary breaker",
                    "teraType": "Fire",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/koraidon.png"
                },
                {
                    "name": "Flutter Mane",
                    "item": "Focus Sash",
                    "ability": "Protosynthesis",
                    "types": ["Ghost", "Fairy"],
                    "moves": ["Moonblast", "Shadow Ball", "Icy Wind", "Protect"],
                    "role": "Speed control",
                    "teraType": "Fairy",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/flutter-mane.png"
                },
                {
                    "name": "Ogerpon-W",
                    "item": "Wellspring Mask",
                    "ability": "Water Absorb",
                    "types": ["Grass", "Water"],
                    "moves": ["Ivy Cudgel", "Horn Leech", "Spiky Shield", "Follow Me"],
                    "role": "Pivot",
                    "teraType": "Water",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/ogerpon-wellspring.png"
                },
                {
                    "name": "Iron Hands",
                    "item": "Assault Vest",
                    "ability": "Quark Drive",
                    "types": ["Fighting", "Electric"],
                    "moves": ["Fake Out", "Drain Punch", "Wild Charge", "Low Kick"],
                    "role": "Fake Out support",
                    "teraType": "Grass",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/iron-hands.png"
                },
                {
                    "name": "Amoonguss",
                    "item": "Sitrus Berry",
                    "ability": "Regenerator",
                    "types": ["Grass", "Poison"],
                    "moves": ["Spore", "Rage Powder", "Pollen Puff", "Protect"],
                    "role": "Redirection",
                    "teraType": "Water",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/amoonguss.png"
                },
                {
                    "name": "Chi-Yu",
                    "item": "Choice Specs",
                    "ability": "Beads of Ruin",
                    "types": ["Dark", "Fire"],
                    "moves": ["Heat Wave", "Dark Pulse", "Snarl", "Overheat"],
                    "role": "Special nuke",
                    "teraType": "Ghost",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/chi-yu.png"
                }
            ]
        },
        {
            "id": "tr-room",
            "name": "Standard Trick Room",
            "format": "Regulation H",
            "archetype": "Hard Trick Room",
            "elo": 1542,
            "notes": "Bulky mode for best-of-three sets where speed reversal gives us a cleaner line into hyper offense.",
            "tags": ["Trick Room", "Bulky", "Bo3"],
            "members": [
                {
                    "name": "Bloodmoon Ursaluna",
                    "item": "Life Orb",
                    "ability": "Mind's Eye",
                    "types": ["Ground", "Normal"],
                    "moves": ["Blood Moon", "Earth Power", "Protect", "Hyper Voice"],
                    "role": "Room sweeper",
                    "teraType": "Normal",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/ursaluna-bloodmoon.png"
                },
                {
                    "name": "Farigiraf",
                    "item": "Safety Goggles",
                    "ability": "Armor Tail",
                    "types": ["Normal", "Psychic"],
                    "moves": ["Trick Room", "Helping Hand", "Hyper Voice", "Protect"],
                    "role": "Setter",
                    "teraType": "Water",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/farigiraf.png"
                },
                {
                    "name": "Incineroar",
                    "item": "Sitrus Berry",
                    "ability": "Intimidate",
                    "types": ["Fire", "Dark"],
                    "moves": ["Fake Out", "Parting Shot", "Flare Blitz", "Knock Off"],
                    "role": "Pivot",
                    "teraType": "Grass",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/incineroar.png"
                },
                {
                    "name": "Amoonguss",
                    "item": "Rocky Helmet",
                    "ability": "Regenerator",
                    "types": ["Grass", "Poison"],
                    "moves": ["Rage Powder", "Spore", "Pollen Puff", "Protect"],
                    "role": "Support",
                    "teraType": "Water",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/amoonguss.png"
                },
                {
                    "name": "Torkoal",
                    "item": "Charcoal",
                    "ability": "Drought",
                    "types": ["Fire"],
                    "moves": ["Eruption", "Heat Wave", "Earth Power", "Protect"],
                    "role": "Endgame pressure",
                    "teraType": "Fire",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/torkoal.png"
                },
                {
                    "name": "Iron Hands",
                    "item": "Assault Vest",
                    "ability": "Quark Drive",
                    "types": ["Fighting", "Electric"],
                    "moves": ["Fake Out", "Drain Punch", "Wild Charge", "Heavy Slam"],
                    "role": "Glue",
                    "teraType": "Bug",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/iron-hands.png"
                }
            ]
        }
    ],
    "threats": [
        {
            "name": "Landorus",
            "threatLevel": "High",
            "reason": "Ground spread damage and Intimidate cycling put repeated pressure on Koraidon, Chi-Yu, and Iron Hands.",
            "counterplay": "Preserve Ogerpon-W and force tempo with Icy Wind plus Water-pressure lines."
        },
        {
            "name": "Miraidon",
            "threatLevel": "Medium",
            "reason": "Electric terrain offense can outpace your neutral positioning if Flutter Mane is forced defensive too early.",
            "counterplay": "Lead Fake Out plus speed control and keep Chi-Yu off the field until trades are favorable."
        },
        {
            "name": "Calyrex-Shadow",
            "threatLevel": "Medium",
            "reason": "Special snowball pressure punishes passive openings and makes sash management important.",
            "counterplay": "Use Koraidon pressure or AV Iron Hands to deny free setup turns and force immediate trades."
        }
    ],
    "weaknessSummary": [
        "Team stacks Ground pressure across Chi-Yu, Iron Hands, and sun positioning turns.",
        "Only one consistently safe Water answer when Ogerpon-W is forced defensive early.",
        "Trick Room denial exists, but reverse-speed endgames still need cleaner play patterns.",
        "Defensive switching is thinner than offensive momentum, especially in open sheets."
    ],
    "recommendations": [
        "Add a second Ground resilience layer through tera planning or a more stable pivot slot.",
        "Promote one move slot into speed control redundancy so Flutter Mane is not carrying the entire burden.",
        "Create lead presets for Landorus balance, Miraidon offense, and hard Trick Room.",
        "Track which restricted-level breakers force your tera most often so matchup plans stay honest."
    ],
    "metaTeams": [
        {
            "id": "balance-lando",
            "name": "Landorus Balance",
            "format": "Regulation H",
            "archetype": "Intimidate Balance",
            "core": ["Landorus", "Incineroar", "Rillaboom", "Flutter Mane"],
            "pressurePoints": ["Ground spread pressure", "Fake Out cycling", "pivot attrition"],
            "plan": [
                "Protect Ogerpon-W from early chip so it remains your cleanest Landorus punishment.",
                "Lead with immediate speed control to punish their default pivot turns.",
                "Use Koraidon aggressively before Intimidate loops slow the game down."
            ],
            "otsUrl": "seeded://balance-lando",
            "showdownText": "Landorus-Therian @ Choice Scarf\nAbility: Intimidate\nTera Type: Flying\n- Stomping Tantrum\n- Rock Slide\n- U-turn\n- Tera Blast\n\nIncineroar @ Sitrus Berry\nAbility: Intimidate\nTera Type: Grass\n- Fake Out\n- Parting Shot\n- Flare Blitz\n- Knock Off\n\nRillaboom @ Assault Vest\nAbility: Grassy Surge\nTera Type: Fire\n- Fake Out\n- Grassy Glide\n- Wood Hammer\n- U-turn\n\nFlutter Mane @ Focus Sash\nAbility: Protosynthesis\nTera Type: Fairy\n- Moonblast\n- Shadow Ball\n- Icy Wind\n- Protect\n\nUrshifu-Rapid-Strike @ Mystic Water\nAbility: Unseen Fist\nTera Type: Water\n- Surging Strikes\n- Close Combat\n- Aqua Jet\n- Detect\n\nAmoonguss @ Rocky Helmet\nAbility: Regenerator\nTera Type: Water\n- Spore\n- Rage Powder\n- Pollen Puff\n- Protect",
            "members": [
                {
                    "name": "Landorus-Therian",
                    "item": "Choice Scarf",
                    "ability": "Intimidate",
                    "types": ["Ground", "Flying"],
                    "moves": ["Stomping Tantrum", "Rock Slide", "U-turn", "Tera Blast"],
                    "role": "Speed control",
                    "teraType": "Flying",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/landorus-therian.png"
                },
                {
                    "name": "Incineroar",
                    "item": "Sitrus Berry",
                    "ability": "Intimidate",
                    "types": ["Fire", "Dark"],
                    "moves": ["Fake Out", "Parting Shot", "Flare Blitz", "Knock Off"],
                    "role": "Pivot",
                    "teraType": "Grass",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/incineroar.png"
                },
                {
                    "name": "Rillaboom",
                    "item": "Assault Vest",
                    "ability": "Grassy Surge",
                    "types": ["Grass"],
                    "moves": ["Fake Out", "Grassy Glide", "Wood Hammer", "U-turn"],
                    "role": "Fake Out support",
                    "teraType": "Fire",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/rillaboom.png"
                },
                {
                    "name": "Flutter Mane",
                    "item": "Focus Sash",
                    "ability": "Protosynthesis",
                    "types": ["Ghost", "Fairy"],
                    "moves": ["Moonblast", "Shadow Ball", "Icy Wind", "Protect"],
                    "role": "Speed control",
                    "teraType": "Fairy",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/flutter-mane.png"
                },
                {
                    "name": "Urshifu-Rapid-Strike",
                    "item": "Mystic Water",
                    "ability": "Unseen Fist",
                    "types": ["Fighting", "Water"],
                    "moves": ["Surging Strikes", "Close Combat", "Aqua Jet", "Detect"],
                    "role": "Breaker",
                    "teraType": "Water",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/urshifu-rapid-strike.png"
                },
                {
                    "name": "Amoonguss",
                    "item": "Rocky Helmet",
                    "ability": "Regenerator",
                    "types": ["Grass", "Poison"],
                    "moves": ["Spore", "Rage Powder", "Pollen Puff", "Protect"],
                    "role": "Redirection",
                    "teraType": "Water",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/amoonguss.png"
                }
            ]
        },
        {
            "id": "tr-ursaluna",
            "name": "Farigiraf Ursaluna Room",
            "format": "Regulation H",
            "archetype": "Hard Trick Room",
            "core": ["Farigiraf", "Bloodmoon Ursaluna", "Amoonguss", "Torkoal"],
            "pressurePoints": ["Priority denial", "slow-mode nukes", "redirection support"],
            "plan": [
                "Respect Armor Tail and avoid overcommitting to Fake Out based lines.",
                "Bring Taunt or heavy double-target pressure into the setter slot immediately.",
                "If room goes up, pivot into bulkier trades and preserve Water tera for Torkoal turns."
            ],
            "otsUrl": "seeded://tr-ursaluna",
            "showdownText": "Farigiraf @ Safety Goggles\nAbility: Armor Tail\nTera Type: Water\n- Trick Room\n- Helping Hand\n- Hyper Voice\n- Protect\n\nUrsaluna-Bloodmoon @ Life Orb\nAbility: Mind's Eye\nTera Type: Normal\n- Blood Moon\n- Earth Power\n- Hyper Voice\n- Protect\n\nAmoonguss @ Rocky Helmet\nAbility: Regenerator\nTera Type: Water\n- Spore\n- Rage Powder\n- Pollen Puff\n- Protect\n\nTorkoal @ Charcoal\nAbility: Drought\nTera Type: Fire\n- Eruption\n- Heat Wave\n- Earth Power\n- Protect\n\nIncineroar @ Sitrus Berry\nAbility: Intimidate\nTera Type: Grass\n- Fake Out\n- Parting Shot\n- Flare Blitz\n- Knock Off\n\nIron Hands @ Assault Vest\nAbility: Quark Drive\nTera Type: Bug\n- Fake Out\n- Drain Punch\n- Wild Charge\n- Heavy Slam",
            "members": [
                {
                    "name": "Farigiraf",
                    "item": "Safety Goggles",
                    "ability": "Armor Tail",
                    "types": ["Normal", "Psychic"],
                    "moves": ["Trick Room", "Helping Hand", "Hyper Voice", "Protect"],
                    "role": "Setter",
                    "teraType": "Water",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/farigiraf.png"
                },
                {
                    "name": "Ursaluna-Bloodmoon",
                    "item": "Life Orb",
                    "ability": "Mind's Eye",
                    "types": ["Ground", "Normal"],
                    "moves": ["Blood Moon", "Earth Power", "Hyper Voice", "Protect"],
                    "role": "Room sweeper",
                    "teraType": "Normal",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/ursaluna-bloodmoon.png"
                },
                {
                    "name": "Amoonguss",
                    "item": "Rocky Helmet",
                    "ability": "Regenerator",
                    "types": ["Grass", "Poison"],
                    "moves": ["Spore", "Rage Powder", "Pollen Puff", "Protect"],
                    "role": "Redirection",
                    "teraType": "Water",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/amoonguss.png"
                },
                {
                    "name": "Torkoal",
                    "item": "Charcoal",
                    "ability": "Drought",
                    "types": ["Fire"],
                    "moves": ["Eruption", "Heat Wave", "Earth Power", "Protect"],
                    "role": "Endgame pressure",
                    "teraType": "Fire",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/torkoal.png"
                },
                {
                    "name": "Incineroar",
                    "item": "Sitrus Berry",
                    "ability": "Intimidate",
                    "types": ["Fire", "Dark"],
                    "moves": ["Fake Out", "Parting Shot", "Flare Blitz", "Knock Off"],
                    "role": "Pivot",
                    "teraType": "Grass",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/incineroar.png"
                },
                {
                    "name": "Iron Hands",
                    "item": "Assault Vest",
                    "ability": "Quark Drive",
                    "types": ["Fighting", "Electric"],
                    "moves": ["Fake Out", "Drain Punch", "Wild Charge", "Heavy Slam"],
                    "role": "Glue",
                    "teraType": "Bug",
                    "image": "https://img.pokemondb.net/sprites/scarlet-violet/normal/iron-hands.png"
                }
            ]
        }
    ]
}
