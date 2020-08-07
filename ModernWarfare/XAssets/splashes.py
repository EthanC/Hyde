import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class SplashTable(TypedDict):
    """Structure of mp/splashtable.csv"""

    ref: str
    shortName: str
    name: str
    desc: str
    icon: str
    sound: str
    type: str
    displayLocation: str
    notifyScript: str  # bool
    headerStringParam: str
    useRectangleImage: str  # bool
    useRectangleBacking: str  # bool
    useHexDisplay: str
    priority: str
    alwaysShow: int  # bool
    altDisplayDesc: str
    altDisplayIcon: str
    altDisplaySound: str
    altDesc2: str
    unknown1: str  # Not defined in luashared/csvutils.lua
    unknown2: str  # Not defined in luashared/csvutils.lua
    unknown3: str  # Not defined in luashared/csvutils.lua
    unknown4: str  # Not defined in luashared/csvutils.lua
    unknown5: str  # Not defined in luashared/csvutils.lua
    unknown6: str  # Not defined in luashared/csvutils.lua
    unknown7: str  # Not defined in luashared/csvutils.lua
    unknown8: str  # Not defined in luashared/csvutils.lua
    unknown9: str  # Not defined in luashared/csvutils.lua
    unknown10: str  # Not defined in luashared/csvutils.lua


class Splashes:
    """Splash XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Splash XAssets."""

        splashes: List[Dict[str, Any]] = []

        splashes = Splashes.Table(self, splashes)

        Utility.WriteFile(self, f"{self.eXAssets}/splashes.json", splashes)

        log.info(f"Compiled {len(splashes):,} Splashes")

    def Table(self: Any, splashes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/splashtable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/splashtable.csv", SplashTable
        )

        if table is None:
            return splashes

        for entry in table:
            splashes.append(
                {
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "description": self.localize.get(entry.get("desc")),
                    "image": entry.get("icon"),
                    "audio": entry.get("sound"),
                }
            )

        return splashes
