import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class VehicleTable(TypedDict):
    """Structure of mp_cp/vehicletable.csv"""

    id: int
    ref: str
    name: str
    image: str
    scrRef: str
    desc: str
    icon: str  # Not defined in luashared/csvutils.lua
    unknown1: int  # Not defined in luashared/csvutils.lua


class Vehicles:
    """Vehicle XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Vehicle XAssets."""

        vehicles: List[Dict[str, Any]] = []

        vehicles = Vehicles.Table(self, vehicles)

        Utility.WriteFile(self, f"{self.eXAssets}/vehicles.json", vehicles)

        log.info(f"Compiled {len(vehicles):,} Vehicles")

    def Table(self: Any, vehicles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp_cp/vehicletable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp_cp/vehicletable.csv", VehicleTable
        )

        if table is None:
            return vehicles

        for entry in table:
            vehicles.append(
                {
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "description": self.localize.get(entry.get("desc")),
                    "image": entry.get("image"),
                    "icon": entry.get("icon"),
                }
            )

        return vehicles
