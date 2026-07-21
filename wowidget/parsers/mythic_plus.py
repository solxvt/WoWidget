from typing import Any


def safe_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def parse_mythic_score(
    mythic_profile: dict,
) -> int:
    mythic_profile = safe_dict(mythic_profile)

    current_rating = safe_dict(mythic_profile.get("current_mythic_rating"))

    score = current_rating.get("rating")

    try:
        return round(float(score or 0))
    except (TypeError, ValueError):
        return 0
