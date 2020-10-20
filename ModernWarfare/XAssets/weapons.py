import logging
from typing import Any, Dict, List, TypedDict, Union

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class StatsTable(TypedDict):
    """Structure of mp/statstable.csv"""

    index: int
    classRef: str
    menuClass: str
    name: str
    ref: str
    asset: str
    image: str
    desc: str
    unknown1: int  # Not defined in luashared/csvutils.lua
    defaultAttachments: str
    attachFirst: str
    stickerSlots: int
    attachCategoryBlacklist: str
    gunTableOverrideAsset: str
    operatorOverrideAsset: str
    attachVariantCategoryBlacklist: str
    hiddenWhenLocked: int  # bool
    unknown3: str  # Not defined in luashared/csvutils.lua
    unknown4: str  # Not defined in luashared/csvutils.lua
    unknown5: str  # Not defined in luashared/csvutils.lua
    unknown6: str  # Not defined in luashared/csvutils.lua
    unknown7: str  # Not defined in luashared/csvutils.lua
    unknown8: str  # Not defined in luashared/csvutils.lua
    unknown9: str  # Not defined in luashared/csvutils.lua
    unknown10: str  # Not defined in luashared/csvutils.lua
    unknown11: str  # Not defined in luashared/csvutils.lua
    brPickupString: str
    unknown12: str  # Not defined in luashared/csvutils.lua
    brRarity: str
    brAmmoType: str
    statAccuracy: float
    statDamage: float
    statRange: float
    statFireRate: float
    statMobility: float
    statControl: float
    BWImage: str
    profileImage: str
    unknown13: str  # Not defined in luashared/csvutils.lua
    unknown14: str  # Not defined in luashared/csvutils.lua
    unknown15: str  # Not defined in luashared/csvutils.lua
    displayOrder: int
    maxRank: int
    showInCP: int  # bool
    unknown16: str  # Not defined in luashared/csvutils.lua
    fireMode1: str
    fireMode2: str
    cpDisplayOrder: int
    canUseCosmetic: int  # bool
    defaultOpticRef: str
    unknown17: str  # Not defined in luashared/csvutils.lua
    postLaunch: str
    isGunsmithDisabled: int  # bool
    isCustomizationDisabled: int  # bool
    canUseOptics: int  # bool
    subclassID: str
    category: str
    progressionImage: str
    survivalCost: int
    lobbyShouldSwapWithSecondary: int  # bool
    lobbyShouldSwapWithPrimary: int  # bool


class WeaponIDs(TypedDict):
    """Structure of loot/weapon_ids.csv"""

    index: int
    baseRef: str
    quality: int
    cost: int
    salvage: int
    license: int
    variantRef: str


class WeaponVariants(TypedDict):
    """Structure of mp/gunsmith/*_*_variants.csv"""

    variantID: int
    ref: str
    baseRef: str
    assetOverride: str
    defaultAttachmentOverrides: str  # Array of strings and ints
    muzzle: str  # Array containing a string and an int
    barrel: str  # Array containing a string and an int
    extra: str  # Array containing a string and an int
    underBarrel: str  # Array containing a string and an int
    optic: str  # Array containing a string and an int
    mag: str  # Array containing a string and an int
    rearGrip: str  # Array containing a string and an int
    stock: str  # Array containing a string and an int
    perk: str  # Array containing a string and an int
    trigger: str  # Array containing a string and an int
    other: str  # Array containing a string and an int
    extraToID: str
    name: str
    image: str
    overrideImage: str  # Not present in all *_*_variants.csv's
    tracerColor: str  # Not present in all *_*_variants.csv's
    dismembermentEnabled: str  # Not present in all *_*_variants.csv's
    gunTableOverrideAsset: str  # Not present in all *_*_variants.csv's
    operatorOverrideAsset: str  # Not present in all *_*_variants.csv's


class WeaponProgression(TypedDict):
    """Structure of mp/gunsmith/*_*_progression.csv"""

    level: int
    lootID: int
    challengeID: int
    challengeRef: str
    bucketID: int
    unlockID: str  # Array of ints
    # +10 columns which are not defined in luashared/csvutils.lua


class AttachmentIDs(TypedDict):
    """Structure of loot/iw8_*_*_attachment_ids.csv"""

    index: int
    ref: str
    quality: int
    cost: int
    salvage: int
    license: int
    variantLootID: int
    variantID: int
    # +10 columns which are not defined in luashared/csvutils.lua and
    # are not present in all iw8_*_*_attachment_ids.csv's


class AttachmentTable(TypedDict):
    """Structure of mp/attachmenttable.csv"""

    index: int
    unknown1: str  # Not defined in luashared/csvutils.lua
    category: str
    name: str
    ref: str
    baseRef: str
    image: str
    desc: str
    unknown2: str  # Not defined in luashared/csvutils.lua
    blockedCategory: str
    unknown3: str  # Not defined in luashared/csvutils.lua
    reticles: str
    perk: str
    slot: str
    acc: float
    dam: float
    rng: float
    rof: float
    mob: float
    ctl: float
    botDifficulty: str  # Array of strings
    modifier1: str  # Array containing a string and an int (modifierStart in luashared/csvutils.lua)
    modifier2: str  # Array containing a string and an int
    modifier3: str  # Array containing a string and an int
    modifier4: str  # Array containing a string and an int
    modifier5: str  # Array containing a string and an int
    modifier6: str  # Array containing a string and an int
    modifier7: str  # Array containing a string and an int
    modifier8: str  # Array containing a string and an int (modifierEnd in luashared/csvutils.lua)
    isWeapon: int  # bool
    reticlePreviewImage: str
    dismembermentEnabled: str
    unknown4: int  # bool, not defined in luashared/csvutils.lua


class Weapons:
    """Weapon XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Weapon XAssets."""

        weapons: List[Dict[str, Any]] = []

        weapons = Weapons.Table(self, weapons)
        weapons = Weapons.IDs(self, weapons)
        weapons = Weapons.Variants(self, weapons)
        weapons = Weapons.Progression(self, weapons)
        weapons = Weapons.Attachments(self, weapons)
        weapons = Weapons.AttachmentTable(self, weapons)

        Utility.WriteFile(self, f"{self.eXAssets}/weapons.json", weapons)

        log.info(f"Compiled {len(weapons):,} Weapons")

    def Table(self: Any, weapons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/statstable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/statstable.csv", StatsTable
        )

        for entry in table:
            if entry.get("ref") is None:
                continue

            weapons.append(
                {
                    "id": None,
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "altName": self.localize.get(entry.get("subclassID")),
                    "description": self.localize.get(entry.get("desc")),
                    "type": None,
                    "rarity": None,
                    "season": None,
                    "class": self.ModernWarfare.GetWeaponClass(entry.get("classRef")),
                    "image": None,
                    "icon": None
                    if (i := entry.get("progressionImage")) == "placeholder_x"
                    else i,
                    "statBars": [
                        {
                            "label": self.localize.get("LUA_MENU/WEAPSTATS_ACCURACY"),
                            "value": entry.get("statAccuracy"),
                        },
                        {
                            "label": self.localize.get("LUA_MENU/WEAPSTATS_DAMAGE"),
                            "value": entry.get("statDamage"),
                        },
                        {
                            "label": self.localize.get("LUA_MENU/WEAPSTATS_RANGE"),
                            "value": entry.get("statRange"),
                        },
                        {
                            "label": self.localize.get("LUA_MENU/WEAPSTATS_ROF"),
                            "value": entry.get("statFireRate"),
                        },
                        {
                            "label": self.localize.get("LUA_MENU/WEAPSTATS_MOBILITY"),
                            "value": entry.get("statMobility"),
                        },
                        {
                            "label": self.localize.get("LUA_MENU/WEAPSTATS_CONTROL"),
                            "value": entry.get("statControl"),
                        },
                    ],
                    "attachments": [],
                    "variants": [],
                }
            )

        if table is None:
            return weapons

        return weapons

    def IDs(self: Any, weapons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/weapon_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/weapon_ids.csv", WeaponIDs
        )

        if ids is None:
            return weapons

        for weapon in weapons:
            for entry in ids:
                if weapon.get("altId") != entry.get("baseRef"):
                    continue

                if entry.get("quality") == 0:
                    weapon["id"] = entry.get("index")
                    weapon["type"] = self.ModernWarfare.GetLootType(entry.get("index"))
                    weapon["rarity"] = self.ModernWarfare.GetLootRarity(
                        entry.get("quality")
                    )
                    weapon["season"] = self.ModernWarfare.GetLootSeason(
                        entry.get("license")
                    )
                else:
                    weapon["variants"].append(
                        {
                            "id": entry.get("index"),
                            "altId": entry.get("variantRef"),
                            "name": None,
                            "flavor": None,
                            "type": self.ModernWarfare.GetLootType(entry.get("index")),
                            "rarity": self.ModernWarfare.GetLootRarity(
                                entry.get("quality")
                            ),
                            "season": self.ModernWarfare.GetLootSeason(
                                entry.get("license")
                            ),
                            "tracers": None,
                            "dismemberment": None,
                            "image": None,
                        }
                    )

        return weapons

    def Variants(self: Any, weapons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/gunsmith/*_*_variants.csv XAssets."""

        files: List[str] = Utility.GetMatchingFiles(
            self, f"{self.iXAssets}/mp/gunsmith/", "csv", None, "_variants"
        )

        for weapon in weapons:
            if (altId := weapon.get("altId")) is None:
                continue

            for file in files:
                refPartial: str = altId.replace("iw8_", "") + "_"
                filePartial: str = file.split("\\")[-1].split(".")[0]

                if filePartial.startswith(refPartial) is False:
                    continue

                table: List[Dict[str, Any]] = Utility.ReadCSV(
                    self, file, WeaponVariants
                )

                if table is None:
                    continue

                for entry in table:
                    if entry.get("variantID") == 0:
                        weapon["image"] = entry.get("image")

                    for variant in weapon.get("variants", []):
                        if variant.get("altId") != entry.get("ref"):
                            continue

                        flavor: str = variant.get("altId").replace("iw8_", "").replace(
                            "variant_", ""
                        )

                        variant["name"] = self.localize.get(entry.get("name"))
                        variant["flavor"] = self.localize.get(
                            f"WEAPON_FLAVOR/{flavor.upper()}_FLAVOR"
                        )
                        variant["tracers"] = self.ModernWarfare.GetAttribute(
                            entry.get("tracerColor")
                        )
                        variant["dismemberment"] = self.ModernWarfare.GetAttribute(
                            entry.get("dismembermentEnabled")
                        )
                        variant["image"] = entry.get("image")

        return weapons

    def Progression(self, weapons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/gunsmith/*_*_progression.csv XAssets."""

        files: List[str] = Utility.GetMatchingFiles(
            self, f"{self.iXAssets}/mp/gunsmith/", "csv", None, "_progression"
        )

        for weapon in weapons:
            if (wAltId := weapon.get("altId")) is None:
                continue

            for file in files:
                refPartial: str = wAltId.replace("iw8_", "") + "_"
                filePartial: str = file.split("\\")[-1].split(".")[0]

                if filePartial.startswith(refPartial) is False:
                    continue

                table: List[Dict[str, Any]] = Utility.ReadCSV(
                    self, file, WeaponProgression
                )

                if table is None:
                    continue

                for entry in table:
                    if entry.get("lootID") is None:
                        continue
                    elif entry.get("level") < 0:
                        continue

                    weapon["attachments"].append(
                        {
                            "id": entry.get("lootID"),
                            "altId": None,
                            "name": None,
                            "description": None,
                            "type": None,
                            "unlock": entry.get("level"),
                            "image": None,
                            "background": "ui_loot_bg_generic",
                            "attributes": [],
                            "statBars": [],
                        }
                    )

        return weapons

    def Attachments(self: Any, weapons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/iw8_*_*_attachment_ids.csv XAssets."""

        files: List[str] = Utility.GetMatchingFiles(
            self, f"{self.iXAssets}/loot/", "csv", None, "_attachment_ids"
        )

        for weapon in weapons:
            if (wAltId := weapon.get("altId")) is None:
                continue

            for file in files:
                filePartial: str = file.split("\\")[-1].split(".")[0]

                if filePartial.startswith(wAltId + "_") is False:
                    continue

                table: List[Dict[str, Any]] = Utility.ReadCSV(self, file, AttachmentIDs)

                if table is None:
                    continue

                for attachment in weapon.get("attachments"):
                    for entry in table:
                        if entry.get("ref") is None:
                            continue
                        elif attachment.get("id") != entry.get("index"):
                            continue

                        attachment["altId"] = entry.get("ref")

        return weapons

    def AttachmentTable(
        self: Any, weapons: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Compile the mp/attachmenttable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/attachmenttable.csv", AttachmentTable
        )

        if table is None:
            return weapons

        for weapon in weapons:
            for attachment in weapon.get("attachments"):
                if attachment.get("altId") is None:
                    continue

                for entry in table:
                    weaponPartial: str = weapon.get("altId").split("_")[-1]

                    if attachment.get("altId") + "_" + weaponPartial == entry.get(
                        "ref"
                    ):
                        pass
                    elif attachment.get("altId") == entry.get("ref"):
                        pass
                    else:
                        continue

                    attachment["name"] = self.localize.get(entry.get("name"))
                    attachment["description"] = self.localize.get(entry.get("desc"))
                    attachment["type"] = self.ModernWarfare.GetAttachmentCategory(
                        entry.get("category")
                    )
                    attachment["image"] = entry.get("image")

                    for i in range(1, 9):
                        if (mod := entry.get(f"modifier{i}")) is None:
                            continue

                        mod: List[str] = mod.split("|")
                        modVal: Union[int, str] = int(mod[1])

                        if modVal == 1:
                            modVal = "+"
                        elif modVal == -1:
                            modVal = "-"

                        attachment["attributes"].append(
                            {"label": self.localize.get(mod[0]), "value": modVal}
                        )

                    statLabels: List[str] = [
                        "LUA_MENU/WEAPSTATS_ACCURACY",
                        "LUA_MENU/WEAPSTATS_DAMAGE",
                        "LUA_MENU/WEAPSTATS_RANGE",
                        "LUA_MENU/WEAPSTATS_ROF",
                        "LUA_MENU/WEAPSTATS_MOBILITY",
                        "LUA_MENU/WEAPSTATS_CONTROL",
                    ]
                    statValues: List[str] = ["acc", "dam", "rng", "rof", "mob", "ctl"]

                    for label, value in zip(statLabels, statValues):
                        if (value := entry.get(value)) is None:
                            continue
                        elif value == 0.0:
                            continue

                        attachment["statBars"].append(
                            {"label": self.localize.get(label), "value": value}
                        )

        return weapons
