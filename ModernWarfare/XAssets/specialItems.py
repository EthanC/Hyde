import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class SpecialIDs(TypedDict):
    """Structure of loot/special_ids.csv"""

    id: int
    ref: str
    name: str
    image: str
    rarity: int
    license: int  # Not defined in luashared/csvutils.lua


class SpecialItems:
    """Special Item XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Special Item XAssets."""

        items: List[Dict[str, Any]] = []

        items = SpecialItems.IDs(self, items)

        Utility.WriteFile(self, f"{self.eXAssets}/specialItems.json", items)

        log.info(f"Compiled {len(items):,} Special Items")

    def IDs(self: Any, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/special_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/special_ids.csv", SpecialIDs
        )

        if ids is None:
            return items

        for entry in ids:
            items.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "image": entry.get("image"),
                    "background": "ui_loot_bg_generic",
                }
            )

        return items
