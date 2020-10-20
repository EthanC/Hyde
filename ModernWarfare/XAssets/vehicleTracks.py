import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class VehicleTrackIDs(TypedDict):
    """Structure of loot/vehicle_track_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class VehicleTracksTable(TypedDict):
    """Structure of mp_cp/vehicletracks.csv"""

    index: int
    ref: str
    vehicleRef: str
    name: str
    alias: str
    lootImage: str
    hideInUI: int  # bool
    inGameSFXAlias: str
    inGameMusicState: str
    battlePassAlias: str
    battlePassName: str
    unlockText: str
    packRef: str


class VehicleTracks:
    """Vehicle Tracks XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Vehicle Track XAssets."""

        tracks: List[Dict[str, Any]] = []

        tracks = VehicleTracks.IDs(self, tracks)
        tracks = VehicleTracks.Table(self, tracks)

        Utility.WriteFile(self, f"{self.eXAssets}/vehicleTracks.json", tracks)

        log.info(f"Compiled {len(tracks):,} Vehicle Tracks")

    def IDs(self: Any, tracks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/vehicle_track_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/vehicle_track_ids.csv", VehicleTrackIDs
        )

        if ids is None:
            return tracks

        for entry in ids:
            tracks.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "unlock": None,
                    "hidden": None,
                    "image": "ui_vehicle_battle_track",
                    "background": "ui_loot_bg_vehicle_horn",
                }
            )

        return tracks

    def Table(self: Any, tracks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp_cp/vehicletracks.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp_cp/vehicletracks.csv", VehicleTracksTable
        )

        if table is None:
            return tracks

        for track in tracks:
            for entry in table:
                if track.get("altId") != entry.get("ref"):
                    continue

                track["name"] = self.localize.get(entry.get("name"))
                track["unlock"] = self.localize.get(entry.get("unlockText"))
                track["hidden"] = bool(entry.get("hideInUI"))

        return tracks
