import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class AccessoryIDs(TypedDict):
    """Structure of loot/accessory_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class AccessoryTable(TypedDict):
    """Structure of mp/accessorytable.csv"""

    ref: str
    asset: str
    weaponRef: str
    attachmentRef: str
    name: str
    description: str
    image: str
    hideInUI: int  # bool
    gimmeGesture: str
    rttDirtyCheck: int
    index: int
    unknown1: str
    unlockType: str
    unlock: str
    lootImage: str
    gscLogic: str
    face: str
    faceLarge: str
    faceFemale: str


class Accessories:
    """Accessory XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Accessory XAssets."""

        accessories: List[Dict[str, Any]] = []

        accessories = Accessories.IDs(self, accessories)
        accessories = Accessories.Table(self, accessories)

        Utility.WriteFile(self, f"{self.eXAssets}/accessories.json", accessories)

        log.info(f"Compiled {len(accessories):,} Accessories")

    def IDs(self: Any, accessories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/accessory_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/accessory_ids.csv", AccessoryIDs
        )

        if ids is None:
            return accessories

        for entry in ids:
            accessories.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "description": None,
                    "flavor": self.localize.get(
                        "STORE_FLAVOR/" + entry.get("ref").upper() + "_FLAVOR"
                    ),
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "hidden": None,
                    "image": None,
                }
            )

        return accessories

    def Table(self: Any, accessories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/accessorytable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/accessorytable.csv", AccessoryTable
        )

        if table is None:
            return accessories

        for accessory in accessories:
            for entry in table:
                if accessory.get("altId") != entry.get("ref"):
                    continue

                accessory["name"] = self.localize.get(entry.get("name"))
                accessory["description"] = self.localize.get(entry.get("description"))
                accessory["image"] = entry.get("lootImage")
                accessory["hidden"] = bool(entry.get("hideInUI"))

        return accessories
