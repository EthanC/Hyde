import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class KillstreakIDs(TypedDict):
    """Structure of loot/killstreak_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class KillstreakTable(TypedDict):
    """Structure of mp/killstreaktable.csv"""

    index: int
    ref: str
    name: str
    desc: str
    kills: int
    supportCost: int
    scoreCost: int
    earnedDialog: str
    alliesDialog: str
    enemyDialog: str
    enemyUseDialog: int  # bool
    score: int
    icon: str
    overheadIcon: str
    dPadIcon: str
    unearnedIcon: str
    showInMenus: int  # bool
    fullImage: str
    smallImage: str
    streakType: str
    extraRecordType: str
    camera: str
    tutorialVideo: str
    animatedIcon: str
    tabletImage: str
    bgImageID: int
    progressionImage: str


class Killstreaks:
    """Killstreak XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Killstreak XAssets."""

        streaks: List[Dict[str, Any]] = []

        streaks = Killstreaks.IDs(self, streaks)
        streaks = Killstreaks.Table(self, streaks)

        Utility.WriteFile(self, f"{self.eXAssets}/killstreaks.json", streaks)

        log.info(f"Compiled {len(streaks):,} Killstreaks")

    def IDs(self: Any, streaks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/killstreak_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/killstreak_ids.csv", KillstreakIDs
        )

        if ids is None:
            return streaks

        for entry in ids:
            streaks.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "description": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "category": None,
                    "costKills": None,
                    "costScore": None,
                    "hidden": None,
                    "image": None,
                    "icon": None,
                    "video": None,
                }
            )

        return streaks

    def Table(self: Any, streaks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/killstreaktable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/killstreaktable.csv", KillstreakTable
        )

        if table is None:
            return streaks

        for streak in streaks:
            for entry in table:
                if streak.get("altId") != entry.get("ref"):
                    continue

                streak["name"] = self.localize.get(entry.get("name"))
                streak["description"] = self.localize.get(entry.get("desc"))
                streak["category"] = (
                    None if (c := entry.get("streakType")) is None else c.title()
                )
                streak["costKills"] = entry.get("kills")
                streak["costScore"] = entry.get("scoreCost")
                streak["hidden"] = not bool(entry.get("showInMenus"))
                streak["image"] = (
                    None
                    if (img := entry.get("progressionImage")) == "placeholder_x"
                    else img
                )
                streak["icon"] = entry.get("tabletImage")
                streak["video"] = entry.get("tutorialVideo")

        return streaks
