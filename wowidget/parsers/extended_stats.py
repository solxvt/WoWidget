from datetime import datetime, timezone
from typing import Any


def safe_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def safe_list(value: Any) -> list:
    return value if isinstance(value, list) else []


def parse_total_mounts(mounts_collection: dict) -> int:
    return len(safe_list(safe_dict(mounts_collection).get("mounts")))


def parse_total_pets(pets_collection: dict) -> int:
    return len(safe_list(safe_dict(pets_collection).get("pets")))


def parse_titles_owned(titles_summary: dict) -> int:
    return len(safe_list(safe_dict(titles_summary).get("titles")))


def parse_exalted_reputations(
    reputations_summary: dict,
) -> int:
    exalted_count = 0

    for reputation in safe_list(safe_dict(reputations_summary).get("reputations")):
        reputation = safe_dict(reputation)
        standing = safe_dict(reputation.get("standing"))

        standing_name = (
            str(
                standing.get(
                    "name",
                    standing.get("type", ""),
                )
            )
            .strip()
            .lower()
        )

        if standing_name == "exalted":
            exalted_count += 1

    return exalted_count


def parse_feats_of_strength(
    achievements_summary: dict,
) -> int:
    summary = safe_dict(achievements_summary)

    for key in (
        "category_progress",
        "categories",
    ):
        for entry in safe_list(summary.get(key)):
            entry = safe_dict(entry)
            category = safe_dict(entry.get("category"))

            category_name = (
                str(
                    category.get(
                        "name",
                        entry.get("name", ""),
                    )
                )
                .strip()
                .lower()
            )

            category_id = category.get("id") or entry.get("id")

            if category_name == "feats of strength" or category_id == 81:
                for quantity_key in (
                    "quantity",
                    "completed_count",
                    "completed_quantity",
                    "total",
                ):
                    try:
                        return max(
                            0,
                            int(entry.get(quantity_key)),
                        )
                    except (
                        TypeError,
                        ValueError,
                    ):
                        pass

                achievements = safe_list(entry.get("achievements"))

                if achievements:
                    return len(achievements)

    count = 0

    for entry in safe_list(summary.get("achievements")):
        entry = safe_dict(entry)
        achievement = safe_dict(entry.get("achievement"))
        category = safe_dict(achievement.get("category") or entry.get("category"))

        category_name = str(category.get("name", "")).strip().lower()

        if category_name == "feats of strength" or category.get("id") == 81:
            count += 1

    return count


def format_last_login(
    timestamp_milliseconds: Any,
) -> str:
    try:
        timestamp = int(timestamp_milliseconds)
    except (
        TypeError,
        ValueError,
    ):
        return "Unavailable"

    if timestamp <= 0:
        return "Unavailable"

    login_time = datetime.fromtimestamp(
        timestamp / 1000,
        tz=timezone.utc,
    )

    elapsed_seconds = max(
        0,
        int((datetime.now(timezone.utc) - login_time).total_seconds()),
    )

    elapsed_hours = elapsed_seconds // 3600

    if elapsed_hours < 1:
        return "Less than 1 hour ago"

    if elapsed_hours < 24:
        unit = "hour" if elapsed_hours == 1 else "hours"

        return f"{elapsed_hours} {unit} ago"

    elapsed_days = elapsed_hours // 24
    unit = "day" if elapsed_days == 1 else "days"

    return f"{elapsed_days} {unit} ago"
