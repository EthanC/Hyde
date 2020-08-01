import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class ConsumableIDs(TypedDict):
    """Structure of loot/consumable_ids.csv"""

    id: int
    ref: str
    quality: int
    cost: int
    salvage: int
    license: int
    AEID: int
    AEEvent: str
    name: str
    image: str
    unknown1: str
    duration: str


class Consumables:
    """Consumable XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Consumable XAssets."""

        consumables: List[Dict[str, Any]] = []

        consumables = Consumables.IDs(self, consumables)

        Utility.WriteFile(self, f"{self.eXAssets}/consumables.json", consumables)

        log.info(f"Compiled {len(consumables):,} Consumables")

    def IDs(self: Any, consumables: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/consumable_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/consumable_ids.csv", ConsumableIDs
        )

        if ids is None:
            return consumables

        for entry in ids:
            consumables.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "description": self.localize.get(entry.get("duration")),
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("quality")),
                    "image": None
                    if ((i := entry.get("image")) == "placeholder_x") or (i == "white")
                    else i,
                    "background": "ui_loot_bg_generic",
                }
            )

        return consumables
