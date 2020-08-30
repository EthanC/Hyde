import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class GameTypesTable(TypedDict):
    """Structure of mp/gametypestable.csv"""

    ref: str
    name: str
    desc: str
    image: str
    teamChoice: int  # bool
    classChoice: int  # bool
    category: str
    defaultMap: str
    wargameName: str
    objectiveHintAttackers: str
    objectiveHintDefenders: str
    MLG: int  # bool
    teamBased: int  # bool
    hardcoreImage: str
    realismImage: str
    wegame: int  # bool
    hideInUI: int  # bool
    xpScalar: float
    isRoundBased: int  # bool
    weaponXPScalar: float
    weaponKillsPerHouse: int
    MLG_ID: int
    CDLImage: str
    CDLName: str
    privateRecipe: str


class GameTypes:
    """Game Type XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Game Type XAssets."""

        types: List[Dict[str, Any]] = []

        types = GameTypes.Table(self, types)

        Utility.WriteFile(self, f"{self.eXAssets}/gameTypes.json", types)

        log.info(f"Compiled {len(types):,} Game Types")

    def Table(self: Any, types: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/gametypestable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/gametypestable.csv", GameTypesTable
        )

        if table is None:
            return types

        for entry in table:
            types.append(
                {
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "description": self.localize.get(entry.get("desc")),
                    "hints": {
                        "global": None
                        if (val := entry.get("objectiveHintAttackers"))
                        != entry.get("objectiveHintDefenders")
                        else self.localize.get(val),
                        "offense": None
                        if (val := entry.get("objectiveHintAttackers"))
                        == entry.get("objectiveHintDefenders")
                        else self.localize.get(val),
                        "defense": None
                        if entry.get("objectiveHintAttackers")
                        == (val := entry.get("objectiveHintDefenders"))
                        else self.localize.get(val),
                    },
                    "category": self.ModernWarfare.GetGameTypeCategory(
                        entry.get("category")
                    ),
                    "teamBased": bool(entry.get("teamBased")),
                    "roundBased": bool(entry.get("isRoundBased")),
                    "teamChoice": bool(entry.get("teamChoice")),
                    "classChoice": bool(entry.get("classChoice")),
                    "scaleXP": entry.get("xpScalar"),
                    "scaleWeaponXP": entry.get("weaponXPScalar"),
                    "icons": {
                        "core": entry.get("image"),
                        "hardcore": entry.get("hardcoreImage"),
                        "realism": entry.get("realismImage"),
                        "cdl": entry.get("CDLImage"),
                    },
                    "hidden": bool(entry.get("hideInUI")),
                }
            )

        return types
