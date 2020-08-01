import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class WeaponCharmIDs(TypedDict):
    """Structure of loot/weapon_charm_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class WeaponCharmTable(TypedDict):
    """Structure of mp/weaponcharmtable.csv"""

    index: int
    ref: str
    name: str
    image: str
    category: str
    hideInUI: int  # bool
    unlockType: str
    unlockString: str
    availableOffline: int  # bool


class Charms:
    """Charm XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Charm XAssets."""

        charms: List[Dict[str, Any]] = []

        charms = Charms.IDs(self, charms)
        charms = Charms.Table(self, charms)

        Utility.WriteFile(self, f"{self.eXAssets}/charms.json", charms)

        log.info(f"Compiled {len(charms):,} Charms")

    def IDs(self: Any, charms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/weapon_charm_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/weapon_charm_ids.csv", WeaponCharmIDs
        )

        if ids is None:
            return charms

        for entry in ids:
            charms.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "flavor": self.localize.get(
                        "STORE_FLAVOR/" + entry.get("ref").upper() + "_FLAVOR"
                    ),
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "hidden": None,
                    "image": None,
                    "background": "ui_loot_bg_charm",
                }
            )

        return charms

    def Table(self: Any, charms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/weaponcharmtable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/weaponcharmtable.csv", WeaponCharmTable
        )

        if table is None:
            return charms

        for charm in charms:
            for entry in table:
                if charm.get("altId") != entry.get("ref"):
                    continue

                charm["name"] = self.localize.get(entry.get("name"))
                charm["hidden"] = bool(entry.get("hideInUI"))
                charm["image"] = entry.get("image")

        return charms
