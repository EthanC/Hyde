import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class GesturesIDs(TypedDict):
    """Structure of loot/gestures_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class GestureTable(TypedDict):
    """Structure of mp/gesturetable.csv"""

    ref: str
    gestureData: str
    name: str
    desc: str
    image: str
    hideInUI: int  # bool
    unknown1: str
    unknown2: str
    index: int
    unlockType: str
    unlockString: str
    fullImage: str
    lootImage: str
    availableOffline: int  # bool


class Gestures:
    """Gesture XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Gesture XAssets."""

        gestures: List[Dict[str, Any]] = []

        gestures = Gestures.IDs(self, gestures)
        gestures = Gestures.Table(self, gestures)

        Utility.WriteFile(self, f"{self.eXAssets}/gestures.json", gestures)

        log.info(f"Compiled {len(gestures):,} Gestures")

    def IDs(self: Any, gestures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/gestures_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/gestures_ids.csv", GesturesIDs
        )

        if ids is None:
            return gestures

        for entry in ids:
            gestures.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "hidden": None,
                    "image": None,
                    "background": "ui_loot_bg_gesture",
                }
            )

        return gestures

    def Table(self: Any, gestures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/gesturetable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/gesturetable.csv", GestureTable
        )

        if table is None:
            return gestures

        for gesture in gestures:
            for entry in table:
                if gesture.get("altId") != entry.get("ref"):
                    continue

                gesture["name"] = self.localize.get(entry.get("name"))
                gesture["hidden"] = bool(entry.get("hideInUI"))
                gesture["image"] = entry.get("lootImage")

        return gestures
