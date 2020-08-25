import logging
from typing import Any, Dict, List, Optional, TypedDict

from utility import Utility

from .database import Database
from .XAssets import (
    Accessories,
    BattlePasses,
    BattlePassItems,
    Bundles,
    CallingCards,
    Camos,
    Charms,
    Consumables,
    Emblems,
    Equipment,
    Executions,
    Features,
    Gestures,
    Killstreaks,
    MasteryChallenges,
    MissionItems,
    Missions,
    OfficerChallenges,
    Operators,
    Quips,
    Skins,
    SpecialItems,
    Splashes,
    Sprays,
    Stickers,
    TurboChallenges,
    VehicleCamos,
    VehicleHorns,
    Vehicles,
    VehicleTracks,
    Weapons,
    WeaponUnlockChallenges,
    WeeklyChallengesBR,
    WeeklyChallengesMP,
)

log: logging.Logger = logging.getLogger(__name__)


class LootMaster(TypedDict):
    """Structure of loot/loot_master.csv"""

    rangeStart: int
    rangeEnd: int
    typeName: str
    typeValue: str
    hidden: int
    typeNameLoc: str
    typeDesc: str
    typeImg: str
    breadcrumb: str
    baseWeaponRef: str


class OperatorIDs(TypedDict):
    """Structure of loot/operator_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class WeaponClassTable(TypedDict):
    """Structure of mp/weaponClassTable.csv"""

    index: int
    ref: str
    slot: int
    name: str
    pluralName: str
    showInMenus: int  # bool
    unlockTablePrefix: str
    showInCP: int  # bool
    image: str
    showInArmory: int  # bool
    previewScene: str
    attachScenePrefix: str
    unknown1: str  # Not defined in luashared/csvutils.csv
    unknown2: str  # Not defined in luashared/csvutils.csv
    classImage: str
    canBeGunsmithed: int  # bool
    attachCategoryWhitelist: str  # Array of strings
    hasVariants: int  # bool


class AttachmentCategoryTable(TypedDict):
    """Structure of mp/attachmentcategorytable.csv"""

    index: int
    ref: str
    name: str
    buttonIndex: int
    displayOrder: int
    categoryScene: str
    smallCategoryScene: str
    largeCategoryScene: str
    bone: str
    defaultLineOffsetX: int
    defaultLineOffsetY: int
    defaultLineOffsetZ: int
    enableBigGunPreviewCamera: int  # bool
    enableSmallGunPreviewCamera: int  # bool
    enableBigShotgunPreviewCamera: int  # bool


class CamoCategoryTable(TypedDict):
    """Structure of mp/camocategorytable.csv"""

    index: int
    ref: str
    name: str


class ModernWarfare:
    """Call of Duty: Modern Warfare (IW8)"""

    def __init__(self: Any, config: dict) -> None:
        self.ModernWarfare = self

        self.config: Dict[str, Any] = config.get("ModernWarfare")
        self.iXAssets: str = self.config["import"]["xassets"]
        self.iImages: str = self.config["import"]["images"]
        self.iVideos: str = self.config["import"]["videos"]
        self.eXAssets: str = self.config["export"]["xassets"]
        self.eImages: str = self.config["export"]["images"]
        self.eVideos: str = self.config["export"]["videos"]
        self.eDatabase: str = self.config["export"]["database"]

    def Compile(self: Any) -> None:
        """Compile and export all supported XAsset types for Modern Warfare."""

        log.info("Compiling XAssets for Call of Duty: Modern Warfare...")

        # Global and reused XAssets
        self.localize: Dict[str, Optional[str]] = ModernWarfare.LoadLocalize(self)
        self.lootTypes: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/loot_master.csv", LootMaster, 1
        )
        self.operatorIds: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/operator_ids.csv", OperatorIDs
        )
        self.weaponClasses: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/weaponClassTable.csv", WeaponClassTable
        )
        self.attachCategories: List[Dict[str, Any]] = Utility.ReadCSV(
            self,
            f"{self.iXAssets}/mp/attachmentcategorytable.csv",
            AttachmentCategoryTable,
        )
        self.camoCategories: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/camocategorytable.csv", CamoCategoryTable
        )

        Accessories.Compile(self)
        BattlePasses.Compile(self)
        BattlePassItems.Compile(self)
        Bundles.Compile(self)
        CallingCards.Compile(self)
        Camos.Compile(self)
        Charms.Compile(self)
        Consumables.Compile(self)
        Emblems.Compile(self)
        Equipment.Compile(self)
        Executions.Compile(self)
        Features.Compile(self)
        Gestures.Compile(self)
        Killstreaks.Compile(self)
        MasteryChallenges.Compile(self)
        MissionItems.Compile(self)
        Missions.Compile(self)
        OfficerChallenges.Compile(self)
        Operators.Compile(self)
        Quips.Compile(self)
        Skins.Compile(self)
        SpecialItems.Compile(self)
        Splashes.Compile(self)
        Sprays.Compile(self)
        Stickers.Compile(self)
        TurboChallenges.Compile(self)
        VehicleCamos.Compile(self)
        VehicleHorns.Compile(self)
        Vehicles.Compile(self)
        VehicleTracks.Compile(self)
        Weapons.Compile(self)
        WeaponUnlockChallenges.Compile(self)
        WeeklyChallengesBR.Compile(self)
        WeeklyChallengesMP.Compile(self)

        if self.config.get("compileDatabase") is True:
            Database.Compile(self)

    def LoadLocalize(self: Any) -> Dict[str, Optional[str]]:
        """Load and filter the localized string entries for Modern Warfare."""

        localize: dict = Utility.ReadFile(self, f"{self.iXAssets}/localize.json")
        placeholders: List[str] = Utility.ReadFile(
            self, "ModernWarfare/placeholders.json"
        )

        for key in localize:
            value: Optional[str] = localize.get(key)

            if value is None:
                continue
            elif value == "":
                localize[key] = None
                continue

            for placeholder in placeholders:
                if value.lower().startswith(placeholder.lower()):
                    localize[key] = None
                elif value.lower().endswith(placeholder.lower()):
                    localize[key] = None

            if (value := localize.get(key)) is not None:
                localize[key] = Utility.StripColorCodes(self, value)

        return localize

    def GetLootRarity(self: Any, value: int) -> Optional[str]:
        """Get the loot rarity for the provided value."""

        return self.localize.get(f"LOOT_MP/QUALITY_{value}")

    def GetLootType(self: Any, id: int) -> Optional[str]:
        """Get the loot type for the provided id."""

        if id is None:
            return

        for loot in self.lootTypes:
            start: int = loot.get("rangeStart")
            end: int = loot.get("rangeEnd")

            if (id >= start) and (id <= end):
                return self.localize.get(loot.get("typeNameLoc"))

    def GetLootSeason(self: Any, license: int) -> Optional[str]:
        """Get the loot season for the provided value."""

        # TODO: This can be improved. Need to research non-seasonal values,
        # such as 99, to handle the other license types.

        if license == 0:
            # Does not necessarily mean that the item is a part of Season 0.
            return
        elif ((license - 1) % 1000) == 0:
            # For instances such as the Season 4: Reloaded update.
            license -= 1
        elif (license % 1000) != 0:
            # Seasonal licenses are multiples of 1,000.
            return

        return self.localize.get(f"SEASONS/SEASON_{round(license / 1000)}")

    def GetOperatorID(self: Any, reference: str) -> Optional[int]:
        """Get the ID for the specified Operator."""

        if reference == "universal_ref":
            # Universal Operator items do not have an ID, so we'll just
            # set one ourselves.
            return 29999
        elif reference == "universal_base_ref":
            # Same reason as universal_ref, however, this is only intended
            # for use with Operators where isLaunchOperator is True.
            return 29998

        for operator in self.operatorIds:
            if reference == operator.get("ref"):
                return operator.get("id")

    def GetWeaponClass(self: Any, reference: str) -> Optional[str]:
        """Get the name of the specified Weapon Class."""

        for weaponClass in self.weaponClasses:
            if reference == weaponClass.get("ref"):
                return self.localize.get(weaponClass.get("name"))

    def GetAttachmentCategory(self: Any, reference: str) -> Optional[str]:
        """Get the name of the specified attachment category."""

        for category in self.attachCategories:
            if category.get("ref") == reference:
                return self.localize.get(category.get("name"))

    def GetCamoCategory(self: Any, reference: str) -> Optional[str]:
        """Get the name of the specified camo category."""

        for category in self.camoCategories:
            if category.get("ref") == reference:
                return self.localize.get(category.get("name"))

    def GetWeaponAttribute(self: Any, reference: str) -> Optional[str]:
        """
        Get the name of the specified weapon attribute.
        
        Defined in ui/utils/weaponutils.lua
        """

        attributes: Dict[str, str] = {
            "red": "WEAPON/TRACER_RED",
            "blue": "WEAPON/TRACER_BLUE",
            "pink": "WEAPON/TRACER_PINK",
            "green": "WEAPON/TRACER_GREEN",
            "purple": "WEAPON/TRACER_PURPLE",
            "freedom": "WEAPON/TRACER_FREEDOM",
            "shadow": "WEAPON/TRACER_SHADOW",
            "gold": "WEAPON/TRACER_GOLD",
            "morte": "WEAPON/TRACER_MORTE",
            "standardDis": "WEAPON/DISMEMBERMENT",
            "cryoDis": "WEAPON/CRYO_DISMEMBERMENT",
            "goldDis": "WEAPON/DISMEMBERMENT_GOLD",
        }

        return self.localize.get(attributes.get(reference))
