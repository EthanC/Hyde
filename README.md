# Hyde

Hyde is a Call of Duty XAsset compiler that transforms raw assets into digestible data. Its main purpose is to produce the data which powers the [COD Tracker Database](https://tracker.gg/warzone/db/loot).

Hyde is intended for use with [Jekyll](https://github.com/EthanC/Jekyll), a Call of Duty XAsset exporter. Raw XAssets are not provided, you must obtain them yourself.

<p align="center">
    <img src="https://i.imgur.com/0rPZTzB.png" draggable="false">
</p>

## Requirements

-   [Python 3.9](https://www.python.org/downloads/)
-   [coloredlogs](https://pypi.org/project/coloredlogs/)
-   [Pillow](https://pillow.readthedocs.io/en/stable/installation.html)
-   [FFmpeg](http://ffmpeg.org/download.html)

## Usage

Obtain the required raw XAssets, as indicated by running the program without XAssets present, and place them in the designated import directory. Then, simply run Hyde!

All data is exported to the designated files in the export directory.

```py
python hyde.py
```

## Supported Titles

### Call of Duty: Modern Warfare

-   Accessories
-   Battle Passes
-   Battle Pass Items
-   Bundles
-   Calling Cards
-   Camos
-   Charms
-   Consumables
-   Emblems
-   Equipment
-   Executions
-   Features
-   Game Types
-   Gestures
-   Item Sources
-   Killstreaks
-   Maps
-   Mastery Challenges
-   Miscellaneous Challenges
-   Mission Items
-   Missions
-   Officer Challenges
-   Operators
-   Quips
-   Skins
-   Special Items
-   Splashes
-   Sprays
-   Stickers
-   Turbo Challenges
-   Vehicle Camos
-   Vehicle Horns
-   Vehicles
-   Vehicle Tracks
-   Weapons
-   Weapon Unlock Challenges
-   Weekly Warzone Challenges
-   Weekly Multiplayer Challenges

## Disclaimer

All XAssets compiled by Hyde are property of their respective owners. Hyde is in no way, shape, or form associated with or endorsed by Activision or its subsidiary studios.
