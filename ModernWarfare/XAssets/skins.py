import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class OperatorSkinIDs(TypedDict):
    """Structure of loot/operator_skin_ids.csv"""

    id: int
    ref: str
    quality: int
    cost: int
    salvage: int
    unlockMethod: int
    altMethod: int
    overrideString: str
    unknown1: str
    lootImage: str


class OperatorSkins(TypedDict):
    """Structure of operatorskins.csv"""

    lootIndex: int
    ref: str
    operatorRef: str
    name: str
    bodyModel: str
    headModel: str
    icon: str
    uiPriority: int
    smallIcon: str
    value: int
    bodyModelHighRes: str
    headeModelHighRes: str
    devUnlocked: int  # bool
    isGlobal: int  # bool
    unlockType: int
    desc: str
    unknown1: str
    unknown2: str
    lootImage: str
    unknown3: str
    unknown4: str
    bannerImage: str
    unknown5: str


class Skins:
    """Skin XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Skin XAssets."""

        skins: List[Dict[str, Any]] = []

        skins = Skins.IDs(self, skins)
        skins = Skins.Table(self, skins)

        Utility.WriteFile(self, f"{self.eXAssets}/operatorSkins.json", skins)

        log.info(f"Compiled {len(skins):,} Operator Skins")

    def IDs(self: Any, skins: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/operator_skin_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/operator_skin_ids.csv", OperatorSkinIDs
        )

        if ids is None:
            return skins

        for entry in ids:
            skins.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "description": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("quality")),
                    "season": self.ModernWarfare.GetLootSeason(
                        entry.get("unlockMethod")
                    ),
                    "operatorId": None,
                    "operatorAltId": None,
                    "image": None,
                    "background": "ui_loot_bg_operator",
                }
            )

        return skins

    def Table(self: Any, skins: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the operatorskins.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/operatorskins.csv", OperatorSkins
        )

        if table is None:
            return skins

        for skin in skins:
            for entry in table:
                if skin.get("altId") != entry.get("ref"):
                    continue

                skin["name"] = self.localize.get(entry.get("name"))
                skin["description"] = self.localize.get(entry.get("desc"))
                skin["image"] = entry.get("lootImage")

                if bool(entry.get("isGlobal")) is True:
                    skin["operatorId"] = self.ModernWarfare.GetOperatorID(
                        "universal_base_ref"
                    )
                    skin["operatorAltId"] = "universal_base_ref"
                else:
                    ref: str = entry.get("operatorRef")
                    skin["operatorId"] = self.ModernWarfare.GetOperatorID(ref)
                    skin["operatorAltId"] = ref

        return skins
