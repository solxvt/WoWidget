from typing import Any


def safe_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def safe_list(value: Any) -> list:
    return value if isinstance(value, list) else []


def parse_highest_pvp_rating(
    pvp_brackets: list,
) -> int | str:
    highest_rating = 0

    for bracket in safe_list(pvp_brackets):
        bracket = safe_dict(bracket)
        rating = bracket.get("rating")

        try:
            parsed_rating = int(rating)
        except (TypeError, ValueError):
            continue

        highest_rating = max(
            highest_rating,
            parsed_rating,
        )

    if highest_rating <= 0:
        return "---"

    return highest_rating
