import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class CamoIDs(TypedDict):
    """Structure of loot/camo_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class CamoTable(TypedDict):
    """Structure of mp/camotable.csv"""

    index: int
    ref: str
    botValid: int  # bool
    category: str
    unlockType: str
    unlockString: str
    hideInUI: int  # bool
    name: str
    image: str
    availableOffline: int  # bool


class Camos:
    """Camo XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Camo XAssets."""

        camos: List[Dict[str, Any]] = []

        camos = Camos.IDs(self, camos)
        camos = Camos.Table(self, camos)

        Utility.WriteFile(self, f"{self.eXAssets}/camos.json", camos)

        log.info(f"Compiled {len(camos):,} Camos")

    def IDs(self: Any, camos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/camo_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/camo_ids.csv", CamoIDs
        )

        if ids is None:
            return camos

        for entry in ids:
            camos.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "category": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "hidden": None,
                    "image": None,
                }
            )

        return camos

    def Table(self: Any, camos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/camotable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/camotable.csv", CamoTable
        )

        if table is None:
            return camos

        for camo in camos:
            for entry in table:
                if camo.get("altId") != entry.get("ref"):
                    continue

                camo["name"] = self.localize.get(entry.get("name"))
                camo["category"] = self.ModernWarfare.GetCamoCategory(
                    entry.get("category")
                )
                camo["hidden"] = bool(entry.get("hidden"))
                camo["image"] = entry.get("image")

        return camos
