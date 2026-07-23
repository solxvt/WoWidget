import os
from typing import Final

DEFAULT_ASSET_BASE_URL: Final[str] = (
    "https://pub-a0932ef3923a4020822651bac823465b.r2.dev/static"
)

ASSET_BASE_URL = os.getenv(
    "WOWIDGET_ASSET_BASE_URL",
    DEFAULT_ASSET_BASE_URL,
).rstrip("/")


SPEC_ICONS: Final[dict[tuple[str, str], str]] = {
    ("Death Knight", "Blood"): "specs/blood.png",
    ("Death Knight", "Frost"): "specs/frostdk.png",
    ("Death Knight", "Unholy"): "specs/unholy.png",
    ("Demon Hunter", "Havoc"): "specs/havoc.png",
    ("Demon Hunter", "Vengeance"): "specs/vengeance.png",
    ("Demon Hunter", "Devourer"): "specs/devourer.png",
    ("Druid", "Balance"): "specs/balance.png",
    ("Druid", "Feral"): "specs/feral.png",
    ("Druid", "Guardian"): "specs/guardian.png",
    ("Druid", "Restoration"): "specs/restodruid.png",
    ("Evoker", "Augmentation"): "specs/augmentation.png",
    ("Evoker", "Devastation"): "specs/devastation.png",
    ("Evoker", "Preservation"): "specs/preservation.png",
    ("Hunter", "Beast Mastery"): "specs/beastmastery.png",
    ("Hunter", "Marksmanship"): "specs/marksmanship.png",
    ("Hunter", "Survival"): "specs/survival.png",
    ("Mage", "Arcane"): "specs/arcane.png",
    ("Mage", "Fire"): "specs/fire.png",
    ("Mage", "Frost"): "specs/frostmage.png",
    ("Monk", "Brewmaster"): "specs/brewmaster.png",
    ("Monk", "Mistweaver"): "specs/mistweaver.png",
    ("Monk", "Windwalker"): "specs/windwalker.png",
    ("Paladin", "Holy"): "specs/holypaly.png",
    ("Paladin", "Protection"): "specs/protpaly.png",
    ("Paladin", "Retribution"): "specs/retribution.png",
    ("Priest", "Discipline"): "specs/discipline.png",
    ("Priest", "Holy"): "specs/holypriest.png",
    ("Priest", "Shadow"): "specs/shadow.png",
    ("Rogue", "Assassination"): "specs/assassination.png",
    ("Rogue", "Outlaw"): "specs/outlaw.png",
    ("Rogue", "Subtlety"): "specs/subtlety.png",
    ("Shaman", "Elemental"): "specs/elemental.png",
    ("Shaman", "Enhancement"): "specs/enhancement.png",
    ("Shaman", "Restoration"): "specs/restoshaman.png",
    ("Warlock", "Affliction"): "specs/affliction.png",
    ("Warlock", "Demonology"): "specs/demonology.png",
    ("Warlock", "Destruction"): "specs/destruction.png",
    ("Warrior", "Arms"): "specs/arms.png",
    ("Warrior", "Fury"): "specs/fury.png",
    ("Warrior", "Protection"): "specs/protwarrior.png",
}


ACHIEVEMENT_ICON: Final[str] = "icons/achievements-icon.png"


FACTION_ICONS: Final[dict[str, str]] = {
    "Alliance": "factions/Alliance.png",
    "Horde": "factions/horde.png",
}


def _normalize_lookup_value(value: str) -> str:
    return " ".join(str(value or "").strip().split()).casefold()


def build_asset_url(
    relative_path: str,
) -> str:
    relative_path = str(relative_path or "").strip()

    if not relative_path:
        return ""

    return f"{ASSET_BASE_URL}/" f"{relative_path.lstrip('/')}"


def get_spec_icon(
    class_name: str,
    spec_name: str,
) -> str:
    normalized_class = _normalize_lookup_value(class_name)
    normalized_spec = _normalize_lookup_value(spec_name)

    for (
        mapped_class,
        mapped_spec,
    ), relative_path in SPEC_ICONS.items():
        if (
            _normalize_lookup_value(mapped_class) == normalized_class
            and _normalize_lookup_value(mapped_spec) == normalized_spec
        ):
            return build_asset_url(relative_path)

    return ""


def get_faction_icon(
    faction_name: str,
) -> str:
    normalized_faction = _normalize_lookup_value(faction_name)

    for (
        mapped_faction,
        relative_path,
    ) in FACTION_ICONS.items():
        if _normalize_lookup_value(mapped_faction) == normalized_faction:
            return build_asset_url(relative_path)

    return ""


def get_achievement_icon() -> str:
    return build_asset_url(ACHIEVEMENT_ICON)
