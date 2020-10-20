import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class VehicleCamoIDs(TypedDict):
    """Structure of loot/vehicle_camo_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class VehicleCamosTable(TypedDict):
    """Structure of mp_cp/vehiclecamos.csv"""

    ref: str
    vehicleRef: str
    name: str
    icon: str
    camoAsset: str
    turretAsset: str
    lootID: int
    showcaseImage: str
    hideInUI: int  # bool
    flavorText: str
    trailVFX: str
    specialAttribute: str
    unlockText: str


class VehicleCamos:
    """Vehicle Camo XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Vehicle Camo XAssets."""

        camos: List[Dict[str, Any]] = []

        camos = VehicleCamos.IDs(self, camos)
        camos = VehicleCamos.Table(self, camos)

        Utility.WriteFile(self, f"{self.eXAssets}/vehicleCamos.json", camos)

        log.info(f"Compiled {len(camos):,} Vehicle Camos")

    def IDs(self: Any, camos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/vehicle_camo_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/vehicle_camo_ids.csv", VehicleCamoIDs
        )

        if ids is None:
            return camos

        for entry in ids:
            camos.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "flavor": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "unlock": None,
                    "attribute": None,
                    "hidden": None,
                    "image": None,
                    "background": "ui_loot_bg_vehicle",
                }
            )

        return camos

    def Table(self: Any, camos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp_cp/vehiclecamos.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp_cp/vehiclecamos.csv", VehicleCamosTable
        )

        if table is None:
            return camos

        for camo in camos:
            for entry in table:
                if camo.get("altId") != entry.get("ref"):
                    continue

                camo["name"] = self.localize.get(entry.get("name"))
                camo["flavor"] = self.localize.get(entry.get("flavorText"))
                camo["unlock"] = self.localize.get(entry.get("unlockText"))
                camo["attribute"] = self.ModernWarfare.GetAttribute(
                    entry.get("specialAttribute")
                )
                camo["hidden"] = bool(entry.get("hideInUI"))
                camo["image"] = (
                    None
                    if (i := entry.get("showcaseImage")) == "ui_default_white"
                    else i
                )

        return camos
