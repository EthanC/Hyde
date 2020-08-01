import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class BattlePassSeason(TypedDict):
    """Structure of loot/battlepass_season*.csv"""

    level: int
    xp: int
    lootId: str  # array of ints
    isFree: int  # bool
    xpToNext: int
    challengeId: str
    codPoints: int
    numVisibleLoot: int  # bool
    billboardImage: str
    isShowcased: str  # array of ints (bools)
    isPromoted: str  # array of ints (bools)


class BattlePassIDs(TypedDict):
    """Structure of loot/battlepass_ids.csv"""

    id: int
    ref: str
    type: int
    rarity: int
    skips: int
    event: str
    challengeID: int
    currencyID: int
    currencyAmount: int
    saleAmount: int
    numItems: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    season: int
    previewImage: str
    name: str
    imageLarge: str
    unknown1: str
    unknown2: str
    seasonFile: str


class BattlePasses:
    """Battle Pass XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Battle Pass XAssets."""

        battlePasses: List[Dict[str, Any]] = []

        battlePasses = BattlePasses.Table(self, battlePasses)

        Utility.WriteFile(self, f"{self.eXAssets}/battlePasses.json", battlePasses)

        log.info(f"Compiled {len(battlePasses):,} Battle Passes")

    def Table(self: Any, battlePasses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/battlepass_season*.csv XAssets."""

        for path in Utility.GetMatchingFiles(
            self, f"{self.iXAssets}/loot/", "csv", "battlepass_season", None
        ):
            table: List[Dict[str, Any]] = Utility.ReadCSV(self, path, BattlePassSeason)

            if table is None:
                continue

            season: int = int(path.split("season")[1].split(".")[0])

            battlePasses.append({"name": f"Season {season}", "items": []})

            for entry in table:
                items: List[int] = Utility.GetCSVArray(self, entry.get("lootId"), int)
                billboards: List[str] = Utility.GetCSVArray(
                    self, entry.get("billboardImage"), str
                )

                for item, billboard in zip(items, billboards):
                    battlePasses[-1]["items"].append(
                        {
                            "id": item,
                            "type": self.ModernWarfare.GetLootType(item),
                            "tier": entry.get("level"),
                            "free": bool(entry.get("isFree")),
                            "codPoints": None
                            if (c := entry.get("codPoints")) == 0
                            else c,
                            "billboard": billboard,
                        }
                    )

        return battlePasses


class BattlePassItems:
    """Battle Pass Item XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Battle Pass Item XAssets."""

        items: List[Dict[str, Any]] = []

        items = BattlePassItems.Table(self, items)

        Utility.WriteFile(self, f"{self.eXAssets}/battlePassItems.json", items)

        log.info(f"Compiled {len(items):,} Battle Pass Items")

    def Table(self: Any, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/battlepass_ids.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/battlepass_ids.csv", BattlePassIDs
        )

        if table is None:
            return items

        for entry in table:
            items.append(
                {
                    "id": entry.get("id"),
                    "name": self.localize.get(entry.get("name")),
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "image": "battlepass_emblem",
                    "background": "ui_loot_bg_battlepass",
                }
            )

        return items
