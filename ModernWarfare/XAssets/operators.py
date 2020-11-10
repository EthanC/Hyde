import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class OperatorsTable(TypedDict):
    """Structure of operators.csv"""

    lootIndex: int
    ref: str
    name: str
    superFaction: int
    factionRef: str
    displayOrder: int
    isLaunchOperator: int  # bool
    icon: str
    unlockedInPrivate: int  # bool
    factionIcon: str
    voice: str
    gender: int
    defaultPose: str
    citizenship: str
    firstLanguage: str
    status: str
    background: str
    codeName: str
    weGame: int
    suit: str
    introVideo: str
    lootImage: str
    defaultSkin: str
    defaultQuip: str
    defaultExecution: str
    unlockedInIGR: int  # bool
    bloodType: str
    thumbprint: str
    bioImage: str
    fullName: str
    hiddenWhenLocked: int  # bool


class FactionTable(TypedDict):
    """Structure of mp/factiontable.csv"""

    ref: str
    name: str
    shortName: str
    eliminated: str
    forfeited: str
    iconFriendlySmall: str
    iconEnemySmall: str
    headIcon: str
    factionVoiceInfix: str
    splashSound: str
    customizationInfix: str
    color: str
    iconFriendlyLarge: str
    iconEnemyLarge: str
    superFactionName: str
    iconSuperFactionFriendlyLarge: str
    iconSuperFactionEnemyLarge: str
    iconSuperFactionFriendlySmall: str
    iconSuperFactionEnemySmall: str
    challengeID: int


class IntelBillets(TypedDict):
    """Structure of cp/cp_intel_billets.csv"""

    index: int
    ref: str
    headshotImage: str
    faction: str
    header1: str
    header2: str
    header3: str
    header4: str
    name: str
    codeName: str
    aliases: str
    nationality: str
    dob: str
    gender: str
    laterality: str
    height: str
    weight: str
    vision: str
    blood: str
    eyeColor: str
    hairColor: str
    relatives: str
    languages: str
    maritalStatus: str
    children: str
    specialistFields: str
    history: str
    associations: str
    directive: str
    footerLeft: str
    footerRight: str


class Operators:
    """Operator XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Operator XAssets."""

        operators: List[Dict[str, Any]] = []

        operators = Operators.IDs(self, operators)
        operators = Operators.Table(self, operators)
        operators = Operators.FactionTable(self, operators)
        operators = Operators.IntelBillets(self, operators)

        Utility.WriteFile(self, f"{self.eXAssets}/operators.json", operators)

        log.info(f"Compiled {len(operators):,} Operators")

    def IDs(self: Any, operators: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/operators_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = self.ModernWarfare.operatorIds

        if ids is None:
            return operators

        for entry in ids:
            operators.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "description": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(
                        entry.get("license") * 1000
                    ),
                    "faction": None,
                    "branch": None,
                    "branchIcon": None,
                    "thumbprint": None,
                    "launchOperator": None,
                    "image": None,
                    "video": None,
                    "hidden": None,
                    "billets": [],
                }
            )

        return operators

    def Table(self: Any, operators: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the operators.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/operators.csv", OperatorsTable
        )

        if table is None:
            return operators

        for operator in operators:
            for entry in table:
                if operator.get("altId") != entry.get("ref"):
                    continue

                operator["name"] = self.localize.get(entry.get("name")).title()
                operator["description"] = self.localize.get(entry.get("background"))
                operator["faction"] = entry.get("superFaction")
                operator["branch"] = entry.get("factionRef")
                operator["branchIcon"] = entry.get("factionIcon")
                operator["thumbprint"] = entry.get("thumbprint")
                operator["launchOperator"] = bool(entry.get("isLaunchOperator"))
                operator["image"] = entry.get("icon")
                operator["video"] = (
                    None
                    if ((v := entry.get("introVideo")) is None)
                    or (v.endswith("_placeholder"))
                    else v
                )
                operator["hidden"] = bool(entry.get("hiddenWhenLocked"))
                operator["billets"] = [
                    {
                        "label": self.localize.get("LUA_MENU/CITIZENSHIP"),
                        "value": self.localize.get(entry.get("citizenship")),
                    },
                    {
                        "label": self.localize.get("LUA_MENU/FIRST_LANGUAGE"),
                        "value": self.localize.get(entry.get("firstLanguage")),
                    },
                    {
                        "label": self.localize.get("LUA_MENU/STATUS"),
                        "value": self.localize.get(entry.get("status")),
                    },
                ]

        return operators

    def FactionTable(
        self: Any, operators: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Compile the mp/factiontable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/factiontable.csv", FactionTable
        )

        if table is None:
            return operators

        for operator in operators:
            for entry in table:
                if operator.get("branch") != entry.get("ref"):
                    continue

                operator["branch"] = self.localize.get(entry.get("name"))

                if operator.get("altId").startswith("default_"):
                    # This is a (temporary?) workaround as Infinity Ward does
                    # not distinguish the two Mil-Sim branches in the factiontable,
                    # thus resulting in each incorrectly belonging to Coalition.
                    if (faction := operator.get("faction")) == 0:
                        operator["faction"] = self.localize.get("LUA_MENU/THE_WEST")
                    elif faction == 1:
                        operator["faction"] = self.localize.get("LUA_MENU/THE_EAST")
                    else:
                        operator["faction"] = None
                else:
                    operator["faction"] = self.localize.get(entry.get("superFactionName"))

        return operators

    def IntelBillets(
        self: Any, operators: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Compile the cp/cp_intel_billets.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/cp/cp_intel_billets.csv", IntelBillets
        )

        if table is None:
            return operators

        for operator in operators:
            for entry in table:
                operatorRef: str = operator.get("altId").split("_")[0]
                entryRef: str = entry.get("ref").split("_")[1]

                if operatorRef != entryRef:
                    continue

                operator["billets"].extend(
                    [
                        {
                            "label": self.localize.get("CP_INTEL/BILLET_NAME_TITLE"),
                            "value": self.localize.get(entry.get("name")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_CODENAME_TITLE"
                            ),
                            "value": self.localize.get(entry.get("codeName")),
                        },
                        {
                            "label": self.localize.get("CP_INTEL/BILLET_ALIASES_TITLE"),
                            "value": self.localize.get(entry.get("aliases")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_NATIONALITY_TITLE"
                            ),
                            "value": self.localize.get(entry.get("nationality")),
                        },
                        {
                            "label": self.localize.get("CP_INTEL/BILLET_DOB_TITLE"),
                            "value": self.localize.get(entry.get("dob")),
                        },
                        {
                            "label": self.localize.get("CP_INTEL/BILLET_GENDER_TITLE"),
                            "value": self.localize.get(entry.get("gender")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_LATERALITY_TITLE"
                            ),
                            "value": self.localize.get(entry.get("laterality")),
                        },
                        {
                            "label": self.localize.get("CP_INTEL/BILLET_HEIGHT_TITLE"),
                            "value": self.localize.get(entry.get("height")),
                        },
                        {
                            "label": self.localize.get("CP_INTEL/BILLET_WEIGHT_TITLE"),
                            "value": self.localize.get(entry.get("weight")),
                        },
                        {
                            "label": self.localize.get("CP_INTEL/BILLET_VISION_TITLE"),
                            "value": self.localize.get(entry.get("vision")),
                        },
                        {
                            "label": self.localize.get("CP_INTEL/BILLET_BLOOD_TITLE"),
                            "value": self.localize.get(entry.get("blood")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_EYECOLOR_TITLE"
                            ),
                            "value": self.localize.get(entry.get("eyeColor")),
                        },
                        {
                            "label": self.localize.get("CP_INTEL/BILLET_HAIR_TITLE"),
                            "value": self.localize.get(entry.get("hairColor")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_RELATIVES_TITLE"
                            ),
                            "value": self.localize.get(entry.get("relatives")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_LANGUAGES_TITLE"
                            ),
                            "value": self.localize.get(entry.get("languages")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_MARITALSTATUS_TITLE"
                            ),
                            "value": self.localize.get(entry.get("maritalStatus")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_CHILDERN_TITLE"
                            ),
                            "value": self.localize.get(entry.get("children")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_SPECIALIST_TITLE"
                            ),
                            "value": self.localize.get(entry.get("specialistFields")),
                        },
                        {
                            "label": self.localize.get("CP_INTEL/BILLET_HISTORY_TITLE"),
                            "value": self.localize.get(entry.get("history")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_ASSOCIATIONS_TITLE"
                            ),
                            "value": self.localize.get(entry.get("associations")),
                        },
                        {
                            "label": self.localize.get(
                                "CP_INTEL/BILLET_DIRECTIVE_TITLE"
                            ),
                            "value": self.localize.get(entry.get("directive")),
                        },
                    ]
                )

        return operators
