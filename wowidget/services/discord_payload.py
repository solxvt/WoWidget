from typing import Any


def safe_int(
    value: Any,
    fallback: int = 0,
) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def format_exact_number(
    value: Any,
) -> str:
    return f"{safe_int(value):,}"


def _append_image_field(
    dynamic_fields: list[dict],
    *,
    name: str,
    url: str,
) -> None:
    cleaned_url = str(url or "").strip()

    if not cleaned_url:
        return

    dynamic_fields.append(
        {
            "type": 3,
            "name": name,
            "value": {
                "url": cleaned_url,
            },
        }
    )


def build_discord_payload(
    widget_data: dict,
) -> dict:
    dynamic_fields = [
        {
            "type": 1,
            "name": "character_name",
            "value": str(
                widget_data.get(
                    "character_name",
                    "Unknown",
                )
            ),
        },
        {
            "type": 2,
            "name": "character_level",
            "value": safe_int(
                widget_data.get(
                    "character_level",
                    0,
                )
            ),
        },
        {
            "type": 1,
            "name": "realm",
            "value": str(
                widget_data.get(
                    "realm",
                    "Unknown",
                )
            ),
        },
        {
            "type": 1,
            "name": "guild",
            "value": str(
                widget_data.get(
                    "guild_name",
                    "---",
                )
            ),
        },
        {
            "type": 1,
            "name": "spec_name",
            "value": str(
                widget_data.get(
                    "spec",
                    "Unknown",
                )
            ),
        },
        {
            "type": 1,
            "name": "race_class",
            "value": str(
                widget_data.get(
                    "race_class",
                    "Unknown",
                )
            ),
        },
        {
            "type": 2,
            "name": "a_score",
            "value": safe_int(
                widget_data.get(
                    "achievement_points",
                    0,
                )
            ),
        },
        {
            "type": 1,
            "name": "a_score2",
            "value": format_exact_number(
                widget_data.get(
                    "achievement_points",
                    0,
                )
            ),
        },
        {
            "type": 2,
            "name": "mythic_score",
            "value": safe_int(
                widget_data.get(
                    "mythic_score",
                    0,
                )
            ),
        },
        {
            "type": 1,
            "name": "mythic_score2",
            "value": format_exact_number(
                widget_data.get(
                    "mythic_score",
                    0,
                )
            ),
        },
        {
            "type": 1,
            "name": "pvp_score",
            "value": str(
                widget_data.get(
                    "pvp_rating",
                    "---",
                )
            ),
        },
        {
            "type": 2,
            "name": "gear_score",
            "value": safe_int(
                widget_data.get(
                    "item_level",
                    0,
                )
            ),
        },
        {
            "type": 1,
            "name": "raid_score",
            "value": str(
                widget_data.get(
                    "raid_progression",
                    "---",
                )
            ),
        },
        {
            "type": 2,
            "name": "mount_score",
            "value": safe_int(
                widget_data.get(
                    "total_mounts",
                    0,
                )
            ),
        },
        {
            "type": 2,
            "name": "pet_score",
            "value": safe_int(
                widget_data.get(
                    "total_pets",
                    0,
                )
            ),
        },
        {
            "type": 2,
            "name": "feats_score",
            "value": safe_int(
                widget_data.get(
                    "feats_of_strength",
                    0,
                )
            ),
        },
        {
            "type": 2,
            "name": "rep_score",
            "value": safe_int(
                widget_data.get(
                    "exalted_reputations",
                    0,
                )
            ),
        },
        {
            "type": 1,
            "name": "last_login",
            "value": str(
                widget_data.get(
                    "last_login",
                    "Unavailable",
                )
            ),
        },
        {
            "type": 2,
            "name": "title_score",
            "value": safe_int(
                widget_data.get(
                    "titles_owned",
                    0,
                )
            ),
        },
    ]

    _append_image_field(
        dynamic_fields,
        name="character_model",
        url=widget_data.get(
            "character_image_url",
            "",
        ),
    )

    _append_image_field(
        dynamic_fields,
        name="spec_icon",
        url=widget_data.get(
            "spec_icon_url",
            "",
        ),
    )

    _append_image_field(
        dynamic_fields,
        name="faction_icon",
        url=widget_data.get(
            "faction_icon_url",
            "",
        ),
    )

    _append_image_field(
        dynamic_fields,
        name="a_icon",
        url=widget_data.get(
            "achievement_icon_url",
            "",
        ),
    )

    return {
        "data": {
            "dynamic": dynamic_fields,
        }
    }
