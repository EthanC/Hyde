import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class ItemSourceTable(TypedDict):
    """Structure of mp/itemsourcetable.csv"""

    marketPlaceID: int
    refType: str
    refName: str
    gameSourceID: str
    equippableBy: str


class ItemSources:
    """Item Source XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Item Source XAssets."""

        sources: List[Dict[str, Any]] = []

        sources = ItemSources.Table(self, sources)

        Utility.WriteFile(self, f"{self.eXAssets}/itemSources.json", sources)

        log.info(f"Compiled {len(sources):,} Item Sources")

    def Table(self: Any, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/itemsourcetable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/itemsourcetable.csv", ItemSourceTable
        )

        if table is None:
            return sources

        for entry in table:
            sources.append(
                {
                    "id": entry.get("marketPlaceID"),
                    "altId": entry.get("refName"),
                    "type": self.ModernWarfare.GetLootType(entry.get("marketPlaceID")),
                    "source": entry.get("gameSourceID"),
                    "equippable": None
                    if (e := entry.get("equippableBy")) is None
                    else e.split(" "),
                }
            )

        return sources
