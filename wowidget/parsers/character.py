from typing import Any


def safe_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def parse_name(profile: dict) -> str:
    return profile.get("name") or "Unknown"


def parse_realm(profile: dict) -> str:
    realm = safe_dict(profile.get("realm"))
    return realm.get("name") or "Unknown"


def parse_guild(profile: dict) -> str:
    guild = safe_dict(profile.get("guild"))
    return guild.get("name") or "---"


def parse_race(profile: dict) -> str:
    race = safe_dict(profile.get("race"))
    return race.get("name") or "Unknown"


def parse_class(profile: dict) -> str:
    character_class = safe_dict(profile.get("character_class"))

    return character_class.get("name") or "Unknown"


def parse_spec(profile: dict) -> str:
    active_spec = safe_dict(profile.get("active_spec"))

    return active_spec.get("name") or "Unknown"


def parse_faction(profile: dict) -> str:
    faction = safe_dict(profile.get("faction"))
    return faction.get("name") or "Unknown"


def parse_item_level(profile: dict) -> int | str:
    equipped_item_level = profile.get("equipped_item_level")

    if equipped_item_level is not None:
        try:
            return round(float(equipped_item_level))
        except (TypeError, ValueError):
            pass

    average_item_level = profile.get("average_item_level")

    if average_item_level is not None:
        try:
            return round(float(average_item_level))
        except (TypeError, ValueError):
            pass

    return "---"


def parse_achievement_points(profile: dict) -> int:
    try:
        return int(profile.get("achievement_points") or 0)
    except (TypeError, ValueError):
        return 0
