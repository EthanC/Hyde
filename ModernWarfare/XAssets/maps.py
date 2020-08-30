import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class MapInfo(TypedDict):
    """Structure of mp/mapinfo.csv"""

    ref: str
    name: str
    caps: str
    isNightMap: int  # bool
    zoomFactorForCroppedMode: float
    minimapHeightForCroppedMode: str
    minimapWidthForCroppedMode: int
    minimapShouldRotateForCodCaster: int  # bool
    minimapOffsetXForCodCaster: float
    minimapOffsetYForCodCaster: float
    team1Faction: str
    team2Faction: str
    team3Faction: str
    team4Faction: str
    team5Faction: str
    team6Faction: str
    team0Faction: str
    bigMapMinimap: int  # bool
    arenaMenuMinimap: str
    bigMapMaxRange: int
    bigMapMaxRangeExpanded: int
    image: str
    loadingImage: str
    bradleyEnabled: int  # bool
    baseName: str
    bigMapTabletRange: int
    dxr: str
    cpMissionImage: str
    hideInMapSelect: int  # bool
    MLG_ID: int
    MLG_aerial_min_height: int
    MLG_aerial_max_height: int
    MLG_aerial_enabled: int  # bool
    cpMissionName: str
    smallMinimapOffsetXForCodCaster: float
    smallMinimapOffsetYForCodCaster: float
    locSelSizeMulDirectional: float
    locSelSizeMulScrambler: float
    locSelSizeMulCUAV: float
    locSelSizeMulEMPDrone: float
    locSelSizeMulDefault: float
    unknown1: int  # Not defined in luashared/csvutils.lua
    unknown2: int  # Not defined in luashared/csvutils.lua
    unknown3: int  # Not defined in luashared/csvutils.lua
    unknown4: int  # Not defined in luashared/csvutils.lua
    unknown5: int  # Not defined in luashared/csvutils.lua
    hasMultipleModes: int  # bool


class Maps:
    """Map XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Map XAssets."""

        maps: List[Dict[str, Any]] = []

        maps = Maps.Table(self, maps)

        Utility.WriteFile(self, f"{self.eXAssets}/maps.json", maps)

        log.info(f"Compiled {len(maps):,} Maps")

    def Table(self: Any, maps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/mapinfo.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/mapinfo.csv", MapInfo
        )

        if table is None:
            return maps

        for entry in table:
            maps.append(
                {
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "night": bool(entry.get("isNightMap")),
                    "raytracing": True if entry.get("dxr") == "DXR_ON" else False,
                    "image": entry.get("loadingImage"),
                    "hidden": bool(entry.get("hideInMapSelect")),
                }
            )

        return maps
