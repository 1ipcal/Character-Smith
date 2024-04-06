character_model_schema = {
    "type": "object",
    "properties": {
        "character_name": {"type": "string"},
        "character_class": {"type": "string"},
        "race": {"type": "string"},
        "level": {"type": "integer"},
        "attributes": {
            "type": "object",
            "properties": {
                "strength": {"type": "integer"},
                "dexterity": {"type": "integer"},
                "constitution": {"type": "integer"},
                "intelligence": {"type": "integer"},
                "wisdom": {"type": "integer"},
                "charisma": {"type": "integer"}
            },
            "required": ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        },
        "hitpoints": {
            "type": "object",
            "properties": {
                "max": {"type": "integer"},
                "current": {"type": "integer"}
            },
            "required": ["max", "current"]
        },
        "armor_class": {"type": "integer"},
        "initiative": {"type": "integer"},
        "speed": {"type": "integer"},
        "saving_throws": {
            "type": "object",
            "properties": {
                "strength": {"type": "boolean"},
                "dexterity": {"type": "boolean"},
                "constitution": {"type": "boolean"},
                "intelligence": {"type": "boolean"},
                "wisdom": {"type": "boolean"},
                "charisma": {"type": "boolean"}
            },
            "required": ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        },
        "hit_dice": {
            "type": "object",
            "properties": {
                "total": {"type": "string"},
                "current": {"type": "string"}
            },
            "required": ["total", "current"]
        },
        "death_saves": {
            "type": "object",
            "properties": {
                "successes": {
                    "type": "array",
                    "items": {"type": "boolean"},
                    "minItems": 3,
                    "maxItems": 3
                },
                "failures": {
                    "type": "array",
                    "items": {"type": "boolean"},
                    "minItems": 3,
                    "maxItems": 3
                }
            },
            "required": ["successes", "failures"]
        },
        "weapon_attacks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "bonus_to_hit": {"type": "string"},
                    "damage": {"type": "string"}
                },
                "required": ["name", "bonus_to_hit", "damage"]
            }
        },
        "abilities": {"type": "string"},
        "skills": {
            "type": "object",
            "properties": {
                "acrobatics": {"type": "boolean"},
                "animal_handling": {"type": "boolean"},
                "arcana": {"type": "boolean"},
                "athletics": {"type": "boolean"},
                "deception": {"type": "boolean"},
                "history": {"type": "boolean"},
                "insight": {"type": "boolean"},
                "intimidation": {"type": "boolean"},
                "investigation": {"type": "boolean"},
                "medicine": {"type": "boolean"},
                "nature": {"type": "boolean"},
                "perception": {"type": "boolean"},
                "performance": {"type": "boolean"},
                "persuasion": {"type": "boolean"},
                "religion": {"type": "boolean"},
                "sleight_of_hand": {"type": "boolean"},
                "stealth": {"type": "boolean"},
                "survival": {"type": "boolean"}
            },
            "required": ["acrobatics", "animal_handling", "arcana", "athletics", "deception", "history", "insight", "intimidation", "investigation", "medicine", "nature", "perception", "performance", "persuasion", "religion", "sleight_of_hand", "stealth", "survival"]
        },
        "other_proficiencies": {"type": "string"},
        "inventory": {"type": "string"},
        "spells": {"type": "string"}
    },
    "required": ["character_name", "character_class", "race", "level", "attributes", "hitpoints", "armor_class", "initiative", "speed", "saving_throws", "hit_dice", "death_saves", "weapon_attacks", "abilities", "skills", "other_proficiencies", "inventory", "spells"]
}