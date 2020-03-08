# Hyde

Hyde is a Call of Duty XAsset compiler that converts raw assets into digestible data. Its main purpose is to produce the data which powers the [COD Tracker Database](https://cod.tracker.gg/).

This program is intended for use with [Jekyll](https://github.com/EthanC/Jekyll), a Call of Duty XAsset exporter. Raw XAssets will not be provided, you must obtain them yourself.

<p align="center">
    <img src="https://i.imgur.com/lHH1QyS.png" draggable="false">
</p>

## Requirements

-   [Python 3.8](https://www.python.org/downloads/)
-   [coloredlogs](https://pypi.org/project/coloredlogs/)

## Usage

Obtain the required raw XAssets, as indicated by running the program without XAssets present, and place them in the designated import directory.

Then, simply run Hyde! All data is exported to the designated files in the export directory.

```py
python hyde.py
```

## Supported XAssets

### Call of Duty: Modern Warfare

-   Accessories
-   Bundles
-   Calling Cards
-   Camos
-   Charms
-   Emblems
-   Finishing Moves
-   Operator Quips
-   Operator Skins
-   Sprays
-   Stickers
-   Weekly Challenges

## Disclaimer

All XAssets compiled by Hyde are property of their respective owners. Hyde is in no way, shape, or form associated with or endorsed by Activision or the subsidiary studios.
