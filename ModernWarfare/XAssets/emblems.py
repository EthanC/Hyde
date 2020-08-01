import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class EmblemsIDs(TypedDict):
    """Structure of loot/emblems_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class EmblemTable(TypedDict):
    """Structure of mp/emblemtable.csv"""

    index: int
    ref: str
    image: str
    name: str
    category: str
    unknown1: str
    botValid: str  # bool
    hideInUI: int  # bool
    unlockType: str
    unlockString: str
    availableOffline: int  # bool
    officerSeason: int


class Emblems:
    """Emblem XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Emblem XAssets."""

        emblems: List[Dict[str, Any]] = []

        emblems = Emblems.IDs(self, emblems)
        emblems = Emblems.Table(self, emblems)

        Utility.WriteFile(self, f"{self.eXAssets}/emblems.json", emblems)

        log.info(f"Compiled {len(emblems):,} Emblems")

    def IDs(self: Any, emblems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/emblems_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/emblems_ids.csv", EmblemsIDs
        )

        if ids is None:
            return emblems

        for entry in ids:
            emblems.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "hidden": None,
                    "image": None,
                    "background": "ui_loot_bg_emblem",
                }
            )

        return emblems

    def Table(self: Any, emblems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/emblemtable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/emblemtable.csv", EmblemTable
        )

        if table is None:
            return emblems

        for emblem in emblems:
            for entry in table:
                if emblem.get("altId") != entry.get("ref"):
                    continue

                emblem["name"] = self.localize.get(entry.get("name"))
                emblem["hidden"] = bool(entry.get("hideInUI"))
                emblem["image"] = entry.get("image")

        return emblems
