import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class EquipmentIDs(TypedDict):
    """Structure of loot/equipment_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class EquipmentTable(TypedDict):
    """Structure of mp/equipment.csv"""

    index: int
    ref: str
    nameRef: str
    desc: str
    image: str
    iconLarge: str
    weapon: str
    uiSlot: int
    uiOrder: int
    unknown1: str  # Not defined in luashared/csvutils.lua
    unknown2: str  # Not defined in luashared/csvutils.lua
    unknown3: str  # Not defined in luashared/csvutils.lua
    unknown4: str  # Not defined in luashared/csvutils.lua
    model: str
    tutorialVideo: str
    extraRecordType: str
    progressionImage: str
    survivalCost: int
    disableAutoUnlockPrivate: int  # bool
    unknown5: str  # Not defined in luashared/csvutils.lua


class Equipment:
    """Equipment XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Equipment XAssets."""

        equipment: List[Dict[str, Any]] = []

        equipment = Equipment.IDs(self, equipment)
        equipment = Equipment.Table(self, equipment)

        Utility.WriteFile(self, f"{self.eXAssets}/equipment.json", equipment)

        log.info(f"Compiled {len(equipment):,} Equipment")

    def IDs(self: Any, equipment: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/equipment_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/equipment_ids.csv", EquipmentIDs
        )

        if ids is None:
            return equipment

        for entry in ids:
            equipment.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "description": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "image": None,
                    "icon": None,
                    "video": None,
                }
            )

        return equipment

    def Table(self: Any, equipment: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/equipment.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/equipment.csv", EquipmentTable
        )

        if table is None:
            return equipment

        for item in equipment:
            for entry in table:
                if item.get("altId") != entry.get("ref"):
                    continue

                item["name"] = self.localize.get(entry.get("nameRef"))
                item["description"] = self.localize.get(entry.get("desc"))
                item["image"] = entry.get("progressionImage")
                item["icon"] = entry.get("image")
                item["video"] = entry.get("tutorialVideo")

        return equipment
