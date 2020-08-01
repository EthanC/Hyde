import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class SpraysIDs(TypedDict):
    """Structure of loot/sprays_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class SprayTable(TypedDict):
    """Structure of mp/spraytable.csv"""

    index: int
    ref: str
    name: str
    image: str
    hideInUI: int  # bool
    unlockType: int
    unlockString: str
    availableOffline: int  # bool


class Sprays:
    """Spray XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Spray XAssets."""

        sprays: List[Dict[str, Any]] = []

        sprays = Sprays.IDs(self, sprays)
        sprays = Sprays.Table(self, sprays)

        Utility.WriteFile(self, f"{self.eXAssets}/sprays.json", sprays)

        log.info(f"Compiled {len(sprays):,} Sprays")

    def IDs(self: Any, sprays: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/sprays_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/sprays_ids.csv", SpraysIDs
        )

        if ids is None:
            return sprays

        for entry in ids:
            sprays.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "hidden": None,
                    "image": None,
                    "background": "ui_loot_bg_spray",
                }
            )

        return sprays

    def Table(self: Any, sprays: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/spraytable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/spraytable.csv", SprayTable
        )

        if table is None:
            return sprays

        for spray in sprays:
            for entry in table:
                if spray.get("altId") != entry.get("ref"):
                    continue

                spray["name"] = self.localize.get(entry.get("name"))
                spray["hidden"] = bool(entry.get("hideInUI"))
                spray["image"] = entry.get("image")

        return sprays
