from typing import Any

from wowidget.data.season import CURRENT_SEASON


def safe_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def safe_list(value: Any) -> list:
    return value if isinstance(value, list) else []


def parse_raid_progression(
    raid_encounters: dict,
) -> str:
    raid_encounters = safe_dict(raid_encounters)

    expansions = safe_list(raid_encounters.get("expansions"))

    current_tier_raids = CURRENT_SEASON["raids"]

    progression = {
        "MYTHIC": {},
        "HEROIC": {},
        "NORMAL": {},
        "LFR": {},
    }

    difficulty_suffixes = {
        "MYTHIC": "M",
        "HEROIC": "H",
        "NORMAL": "N",
        "LFR": "LFR",
    }

    for expansion in expansions:
        expansion = safe_dict(expansion)

        for instance in safe_list(expansion.get("instances")):
            instance = safe_dict(instance)

            instance_data = safe_dict(instance.get("instance"))

            instance_name = instance_data.get("name")

            if instance_name not in current_tier_raids:
                continue

            for mode in safe_list(instance.get("modes")):
                mode = safe_dict(mode)

                difficulty = safe_dict(mode.get("difficulty"))

                difficulty_type = difficulty.get("type")

                if difficulty_type not in progression:
                    continue

                progress = safe_dict(mode.get("progress"))

                completed = progress.get("completed_count")

                try:
                    completed = int(completed)
                except (TypeError, ValueError):
                    continue

                previous_value = progression[difficulty_type].get(instance_name, 0)

                progression[difficulty_type][instance_name] = max(
                    previous_value,
                    completed,
                )

    total_bosses = sum(current_tier_raids.values())

    for difficulty_type in [
        "MYTHIC",
        "HEROIC",
        "NORMAL",
        "LFR",
    ]:
        completed_total = 0

        for raid_name, raid_total in current_tier_raids.items():
            completed = progression[difficulty_type].get(raid_name, 0)

            completed_total += min(
                completed,
                raid_total,
            )

        if completed_total > 0:
            suffix = difficulty_suffixes[difficulty_type]

            return f"{completed_total}/" f"{total_bosses} {suffix}"

    return "---"
