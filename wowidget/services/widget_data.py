from typing import Any

from wowidget.parsers.character import (
    parse_achievement_points,
    parse_class,
    parse_faction,
    parse_guild,
    parse_item_level,
    parse_name,
    parse_race,
    parse_realm,
    parse_spec,
)
from wowidget.parsers.extended_stats import (
    format_last_login,
    parse_exalted_reputations,
    parse_feats_of_strength,
    parse_titles_owned,
    parse_total_mounts,
    parse_total_pets,
)
from wowidget.parsers.mythic_plus import (
    parse_mythic_score,
)
from wowidget.parsers.pvp import (
    parse_highest_pvp_rating,
)
from wowidget.parsers.raids import (
    parse_raid_progression,
)


def safe_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def get_character_render_url(
    character_media: dict,
) -> str:
    character_media = safe_dict(character_media)

    assets = character_media.get("assets")

    if not isinstance(assets, list):
        return ""

    for asset in assets:
        asset = safe_dict(asset)

        if asset.get("key") == "main-raw":
            return asset.get("value") or ""

    return ""


def build_widget_data(
    bundle: dict,
) -> dict:
    profile = safe_dict(bundle.get("profile"))
    mythic_plus = safe_dict(bundle.get("mythic_plus"))
    raid_encounters = safe_dict(bundle.get("raid_encounters"))
    character_media = safe_dict(bundle.get("character_media"))
    mounts_collection = safe_dict(bundle.get("mounts_collection"))
    pets_collection = safe_dict(bundle.get("pets_collection"))
    titles_summary = safe_dict(bundle.get("titles_summary"))
    reputations_summary = safe_dict(bundle.get("reputations_summary"))
    achievements_summary = safe_dict(bundle.get("achievements_summary"))

    pvp_brackets = bundle.get("pvp_brackets")

    if not isinstance(pvp_brackets, list):
        pvp_brackets = []

    race_name = parse_race(profile)
    class_name = parse_class(profile)

    last_login_timestamp = profile.get("last_login_timestamp") or 0

    return {
        "character_id": profile.get("id"),
        "character_name": parse_name(profile),
        "character_level": profile.get("level") or 0,
        "realm": parse_realm(profile),
        "guild_name": parse_guild(profile),
        "race": race_name,
        "class": class_name,
        "spec": parse_spec(profile),
        "race_class": (f"{race_name} {class_name}"),
        "faction": parse_faction(profile),
        "achievement_points": (parse_achievement_points(profile)),
        "item_level": parse_item_level(profile),
        "mythic_score": (parse_mythic_score(mythic_plus)),
        "pvp_rating": (parse_highest_pvp_rating(pvp_brackets)),
        "raid_progression": (parse_raid_progression(raid_encounters)),
        "total_mounts": (parse_total_mounts(mounts_collection)),
        "total_pets": (parse_total_pets(pets_collection)),
        "feats_of_strength": (parse_feats_of_strength(achievements_summary)),
        "exalted_reputations": (parse_exalted_reputations(reputations_summary)),
        "last_login": (format_last_login(last_login_timestamp)),
        "titles_owned": (parse_titles_owned(titles_summary)),
        "main_raw_url": (get_character_render_url(character_media)),
    }
