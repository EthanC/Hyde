import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class StickerIDs(TypedDict):
    """Structure of loot/sticker_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class WeaponStickerTable(TypedDict):
    """Structure of mp/weaponstickertable.csv"""

    index: int
    ref: str
    netConstID: int
    name: str
    image: str
    category: str
    hideInUI: int  # bool
    unlockType: int
    unlockString: str
    availableOffline: int  # bool


class Stickers:
    """Sticker XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Sticker XAssets."""

        stickers: List[Dict[str, Any]] = []

        stickers = Stickers.IDs(self, stickers)
        stickers = Stickers.Table(self, stickers)

        Utility.WriteFile(self, f"{self.eXAssets}/stickers.json", stickers)

        log.info(f"Compiled {len(stickers):,} Weapon Stickers")

    def IDs(self: Any, stickers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/sticker_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/sticker_ids.csv", StickerIDs
        )

        if ids is None:
            return stickers

        for entry in ids:
            stickers.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "hidden": None,
                    "image": None,
                    "background": "ui_loot_bg_sticker",
                }
            )

        return stickers

    def Table(self: Any, stickers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/weaponstickertable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/weaponstickertable.csv", WeaponStickerTable
        )

        if table is None:
            return stickers

        for sticker in stickers:
            for entry in table:
                if sticker.get("altId") != entry.get("ref"):
                    continue

                sticker["name"] = self.localize.get(entry.get("name"))
                sticker["hidden"] = bool(entry.get("hideInUI"))
                sticker["image"] = entry.get("image")

        return stickers
