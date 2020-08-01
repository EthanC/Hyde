import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class PlayercardsIDs(TypedDict):
    """Structure of loot/playercards_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class CallingCardsTable(TypedDict):
    """Structure of mp/callingcards.csv"""

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


class CallingCards:
    """Calling Card XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Calling Card XAssets."""

        cards: List[Dict[str, Any]] = []

        cards = CallingCards.IDs(self, cards)
        cards = CallingCards.Table(self, cards)

        Utility.WriteFile(self, f"{self.eXAssets}/callingCards.json", cards)

        log.info(f"Compiled {len(cards):,} Calling Cards")

    def IDs(self: Any, cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/playercards_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/playercards_ids.csv", PlayercardsIDs
        )

        if ids is None:
            return cards

        for entry in ids:
            cards.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "hidden": None,
                    "image": None,
                }
            )

        return cards

    def Table(self: Any, cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/callingcards.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/callingcards.csv", CallingCardsTable
        )

        if table is None:
            return cards

        for card in cards:
            for entry in table:
                if card.get("altId") != entry.get("ref"):
                    continue

                card["name"] = self.localize.get(entry.get("name"))
                card["hidden"] = bool(entry.get("hideInUI"))
                card["image"] = entry.get("image")

        return cards
