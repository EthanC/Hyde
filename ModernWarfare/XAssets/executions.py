import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class ExecutionsIDs(TypedDict):
    """Structure of loot/executions_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class ExecutionTable(TypedDict):
    """Structure of mp_cp/executiontable.csv"""

    lootIndex: int
    ref: str
    operatorRef: str
    name: str
    unknown1: str
    value: int
    devUnlocked: int  # bool
    unknown2: str
    icon: str
    unlockType: int
    desc: str
    videoPreview: str
    asset: str
    propWeapon: str
    inGameName: str
    image: str
    unknown3: str
    lootImage: str
    pet: str


class Executions:
    """Execution XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Execution XAssets."""

        executions: List[Dict[str, Any]] = []

        executions = Executions.IDs(self, executions)
        executions = Executions.Table(self, executions)

        Utility.WriteFile(self, f"{self.eXAssets}/executions.json", executions)

        log.info(f"Compiled {len(executions):,} Executions")

    def IDs(self: Any, executions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/executions_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/executions_ids.csv", ExecutionsIDs
        )

        if ids is None:
            return executions

        for entry in ids:
            executions.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "operatorId": None,
                    "operatorAltId": None,
                    "pet": None,
                    "image": None,
                    "background": "ui_loot_bg_execution",
                    "video": None,
                }
            )

        return executions

    def Table(self: Any, executions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp_cp/executiontable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp_cp/executiontable.csv", ExecutionTable
        )

        if table is None:
            return executions

        for execution in executions:
            for entry in table:
                if execution.get("altId") != entry.get("ref"):
                    continue

                execution["name"] = self.localize.get(entry.get("name"))
                execution["operatorId"] = self.ModernWarfare.GetOperatorID(
                    entry.get("operatorRef")
                )
                execution["operatorAltId"] = entry.get("operatorRef")
                execution["pet"] = entry.get("pet")
                execution["image"] = entry.get("lootImage")
                execution["video"] = entry.get("videoPreview")

        return executions
