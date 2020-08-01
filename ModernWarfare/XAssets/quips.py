import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class OperatorQuipIDs(TypedDict):
    """Structure of loot/operator_quip_ids.csv"""

    id: int
    ref: str
    quality: int
    cost: int
    salvage: int
    license: int
    name: str
    icon: str
    lootImage: str


class OperatorQuips(TypedDict):
    """Structure of operatorquips.csv"""

    lootIndex: int
    ref: str
    operatorRef: str
    name: str
    lootImage: str
    icon: str
    alias: str
    unlockType: int
    transcript: str


class Quips:
    """Quip XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Quip XAssets."""

        quips: List[Dict[str, Any]] = []

        quips = Quips.IDs(self, quips)
        quips = Quips.Table(self, quips)

        Utility.WriteFile(self, f"{self.eXAssets}/operatorQuips.json", quips)

        log.info(f"Compiled {len(quips):,} Operator Quips")

    def IDs(self: Any, quips: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/operator_quip_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/operator_quip_ids.csv", OperatorQuipIDs
        )

        if ids is None:
            return quips

        for entry in ids:
            quips.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "description": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("quality")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "operatorId": None,
                    "operatorAltId": None,
                    "image": None,
                    "background": "ui_loot_bg_operator",
                }
            )

        return quips

    def Table(self: Any, quips: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the operatorquips.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/operatorquips.csv", OperatorQuips
        )

        if table is None:
            return quips

        for quip in quips:
            for entry in table:
                if quip.get("altId") != entry.get("ref"):
                    continue

                quip["name"] = self.localize.get(entry.get("name"))
                quip["description"] = self.localize.get(entry.get("transcript"))
                quip["operatorId"] = self.ModernWarfare.GetOperatorID(
                    entry.get("operatorRef")
                )
                quip["operatorAltId"] = entry.get("operatorRef")
                quip["image"] = entry.get("lootImage")

        return quips
