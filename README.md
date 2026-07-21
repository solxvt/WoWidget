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

## License

WoWidget is licensed under the GNU General Public License v3.0.

You are free to use, modify, and redistribute this software under the terms of the GPLv3.

The WoWidget name, logo, branding, documentation, screenshots, and other original artwork remain
the property of their respective copyright holders and are not licensed for reuse except as
permitted by law or with permission.

## Disclaimer

WoWidget is an independent fan project.

World of Warcraft®, Blizzard Entertainment®, and Discord® are trademarks of their respective owners.

WoWidget is not affiliated with, endorsed by, or sponsored by Blizzard Entertainment or Discord.

# WoWidget
# Copyright (C) 2026 Austin Brownell
#
# SPDX-License-Identifier: GPL-3.0-or-later
