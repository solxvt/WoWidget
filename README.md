# WoWidget

WoWidget is a Windows desktop application that publishes World of Warcraft
character information to Discord profile widgets.

It retrieves supported character data from Blizzard, prepares a custom
portrait, and updates the User Variables configured in Discord's Widget Editor.

## Documentation

Setup instructions, variable references, FAQs, and troubleshooting are
available on the WoWidget documentation site:

https://solxvt.github.io/WoWidget/

## Current User Variables

`character_model`, `character_name`, `character_level`, `race_class`, `realm`,
`guild`, `faction_icon`, `spec_name`, `spec_icon`, `gear_score`,
`mythic_score`, `pvp_score`, `raid_score`, `a_score`, `mount_score`,
`pet_score`, `title_score`, `feats_score`, `rep_score`, and `last_login`.

Variable names are case-sensitive. Their Discord Presentation Types must match
the documentation.

## Development

WoWidget currently targets Windows and Python 3.14.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python main.py
```

## Disclaimer

WoWidget is a fan-built project and is not affiliated with or endorsed by
Blizzard Entertainment or Discord.
