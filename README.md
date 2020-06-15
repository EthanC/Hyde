# Hyde

Hyde is a Call of Duty XAsset compiler that converts raw assets into digestible data. Its main purpose is to produce the data which powers the [COD Tracker Database](https://tracker.gg/warzone/db/loot).

Hyde is intended for use with [Jekyll](https://github.com/EthanC/Jekyll), a Call of Duty XAsset exporter. Raw XAssets are not provided, you must obtain them yourself.

<p align="center">
    <img src="https://i.imgur.com/lHH1QyS.png" draggable="false">
</p>

## Requirements

-   [Python 3.8](https://www.python.org/downloads/)
-   [coloredlogs](https://pypi.org/project/coloredlogs/)
-   [Pillow](https://pillow.readthedocs.io/en/stable/installation.html)
-   [FFmpeg](http://ffmpeg.org/download.html)

## Usage

Obtain the required raw XAssets, as indicated by running the program without XAssets present, and place them in the designated import directory. Then, simply run Hyde!

All data is exported to the designated files in the export directory.

```py
python hyde.py
```

## Supported XAssets

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
-   Executions
-   Features
-   Gestures
-   Missions
-   Mission Items
-   Officer Challenges
-   Operators
-   Operator Quips
-   Operator Skins
-   Special Items
-   Sprays
-   Stickers
-   Vehicles
-   Vehicle Camos
-   Vehicle Horns
-   Weapons
-   Weapon Unlock Challenges
-   Weekly Multiplayer Challenges
-   Weekly Warzone Challenges

## Disclaimer

All XAssets compiled by Hyde are property of their respective owners. Hyde is in no way, shape, or form associated with or endorsed by Activision or its subsidiary studios.
