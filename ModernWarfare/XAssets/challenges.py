import logging
from typing import Any, Dict, List, Optional, TypedDict, Union

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class ElderChallenges(TypedDict):
    """Structure of elder_challenges.csv"""

    id: int
    ref: str
    name: str
    desc: str
    amount: int
    loot: int
    xp: int


class GunUnlockChallenges(TypedDict):
    """Structure of gun_unlock_challenges.csv"""

    id: int
    ref: str
    name: str
    desc: str
    amount: int
    unknown1: str  # Not defined in luashared/csvutils.lua
    loot: int


class BRWeeklyChallenges(TypedDict):
    """Structure of br_weekly_challenges.csv"""

    id: int
    ref: str
    name: str
    desc: str
    amount: int
    xp: int
    loot: int
    start: int
    length: int
    season: int
    unknown1: str  # Not defined in luashared/csvutils.lua


class WeeklyChallenges(TypedDict):
    """Structure of weekly_challenges.csv"""

    id: int
    ref: str
    name: str
    desc: str
    amount: int
    xp: int
    loot: int
    start: int
    length: int
    season: int


class StickerBookChallenges(TypedDict):
    """Structure of sticker_book_challenges.csv"""

    id: int
    ref: str
    name: str
    desc: str
    amount: str  # Array of ints
    loot: str  # Array of ints
    XPReward: str  # Array of ints
    categoryType: str
    icon: str
    detailDesc: str


class PetWatchTurboTable(TypedDict):
    """Structure of mp/petwatchturbotable.csv"""

    ref: str
    phaseNum: int
    phaseTime: int
    bonusTimeMax: int
    gameType: str
    charmID: int
    challengeDesc: str


class MiscChallenges(TypedDict):
    """Structure of misc_challenges.csv"""

    id: int
    ref: str
    name: str
    desc: str
    amount: int
    xp: int
    loot: int
    categoryType: str
    icon: str
    detailDesc: str
    conversionType: str
    hideSplash: int  # bool
    hideAARLoot: int  # bool
    showAARPopup: int  # bool
    sound: str


class OfficerChallenges:
    """Officer Challenge XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Officer Challenge XAssets."""

        challenges: List[Dict[str, Any]] = []

        challenges = OfficerChallenges.Table(self, challenges)

        Utility.WriteFile(self, f"{self.eXAssets}/officerChallenges.json", challenges)

        log.info(f"Compiled {len(challenges):,} Officer Challenges")

    def Table(self: Any, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the elder_challenges.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/elder_challenges.csv", ElderChallenges
        )

        if table is None:
            return challenges

        for entry in table:
            if (ref := entry.get("ref")).startswith("ch_elder_s"):
                season: Optional[int] = int(ref.split("ch_elder_s")[1].split("_")[0])
            else:
                season: Optional[int] = None

            if (amount := entry.get("amount")) is not None:
                amount: Optional[Union[str, int]] = f"{amount:,}"

            challenges.append(
                {
                    "altId": ref,
                    "name": self.localize.get(entry.get("name")),
                    "description": self.localize.get(entry.get("desc")).replace(
                        "&&1", amount
                    ),
                    "season": season,
                    "xp": entry.get("xp"),
                }
            )

        return challenges


class WeaponUnlockChallenges:
    """Weapon Unlock Challenge XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Weapon Unlock Challenge XAssets."""

        challenges: List[Dict[str, Any]] = []

        challenges = WeaponUnlockChallenges.Table(self, challenges)

        Utility.WriteFile(
            self, f"{self.eXAssets}/weaponUnlockChallenges.json", challenges
        )

        log.info(f"Compiled {len(challenges):,} Weapon Unlock Challenges")

    def Table(self: Any, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the gun_unlock_challenges.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/gun_unlock_challenges.csv", GunUnlockChallenges
        )

        if table is None:
            return challenges

        for entry in table:
            if (amount := entry.get("amount")) is not None:
                amount: Optional[Union[str, int]] = f"{amount:,}"

            challenges.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "description": self.localize.get(entry.get("desc")).replace(
                        "&&1", amount
                    ),
                    "weaponId": entry.get("loot"),
                }
            )

        return challenges


class WeeklyChallengesBR:
    """Weekly Battle Royale Challenges XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Weekly Battle Royale Challenges XAssets."""

        challenges: List[Dict[str, Any]] = []

        challenges = WeeklyChallengesBR.Table(self, challenges)

        Utility.WriteFile(self, f"{self.eXAssets}/weeklyChallengesBR.json", challenges)

        log.info(f"Compiled {len(challenges):,} Weekly Battle Royale Challenges")

    def Table(self: Any, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the br_weekly_challenges.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/br_weekly_challenges.csv", BRWeeklyChallenges
        )

        if table is None:
            return challenges

        for entry in table:
            altId: str = entry.get("ref")

            season: int = int(altId.split("season_")[1].split("_")[0])
            week: int = int(altId.split("week_")[1].split("_")[0])

            if (amount := entry.get("amount")) is not None:
                amount: Optional[Union[str, int]] = f"{amount:,}"

            challenges.append(
                {
                    "id": entry.get("id"),
                    "altId": altId,
                    "name": self.localize.get(entry.get("name")),
                    "description": self.localize.get(entry.get("desc")).replace(
                        "&&1", amount
                    ),
                    "start": Utility.PrettyTime(self, entry.get("start")),
                    "season": season,
                    "week": week,
                    "xp": entry.get("xp"),
                    "rewards": [],
                }
            )

            if (l := entry.get("loot")) is not None:
                challenges[-1]["rewards"].append(
                    {"id": l, "type": self.ModernWarfare.GetLootType(l)}
                )

        return challenges


class WeeklyChallengesMP:
    """Weekly Multiplayer Challenges XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Weekly Multiplayer Challenges XAssets."""

        challenges: List[Dict[str, Any]] = []

        challenges = WeeklyChallengesMP.Table(self, challenges)

        Utility.WriteFile(self, f"{self.eXAssets}/weeklyChallengesMP.json", challenges)

        log.info(f"Compiled {len(challenges):,} Weekly Multiplayer Challenges")

    def Table(self: Any, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the weekly_challenges.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/weekly_challenges.csv", WeeklyChallenges
        )

        if table is None:
            return challenges

        for entry in table:
            altId: str = entry.get("ref")

            season: int = int(altId.split("season_")[1].split("_")[0])
            week: int = int(altId.split("week_")[1].split("_")[0])

            if (amount := entry.get("amount")) is not None:
                amount: Optional[Union[str, int]] = f"{amount:,}"

            challenges.append(
                {
                    "id": entry.get("id"),
                    "altId": altId,
                    "name": self.localize.get(entry.get("name")),
                    "description": self.localize.get(entry.get("desc")).replace(
                        "&&1", amount
                    ),
                    "start": Utility.PrettyTime(self, entry.get("start")),
                    "season": season,
                    "week": week,
                    "xp": entry.get("xp"),
                    "rewards": [],
                }
            )

            if (l := entry.get("loot")) is not None:
                challenges[-1]["rewards"].append(
                    {"id": l, "type": self.ModernWarfare.GetLootType(l)}
                )

        return challenges


class MasteryChallenges:
    """Mastery Challenges XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Mastery Challenges XAssets."""

        challenges: List[Dict[str, Any]] = []

        challenges = MasteryChallenges.Table(self, challenges)

        Utility.WriteFile(self, f"{self.eXAssets}/masteryChallenges.json", challenges)

        log.info(f"Compiled {len(challenges):,} Mastery Challenges")

    def Table(self: Any, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the sticker_book_challenges.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/sticker_book_challenges.csv", StickerBookChallenges
        )

        if table is None:
            return challenges

        for entry in table:
            challenges.append(
                {
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "description": self.localize.get(entry.get("desc")),
                    "category": entry.get("categoryType"),
                    "rewards": [],
                }
            )

            amounts: List[int] = Utility.GetCSVArray(self, entry.get("amount"), int)
            loot: List[int] = Utility.GetCSVArray(self, entry.get("loot"), int)
            xp: List[int] = Utility.GetCSVArray(self, entry.get("XPReward"), int)

            for a, l, x in zip(amounts, loot, xp):
                challenges[-1]["rewards"].append(
                    {
                        "amount": a,
                        "xp": x,
                        "id": l,
                        "type": self.ModernWarfare.GetLootType(l),
                    }
                )

            if (desc := challenges[-1].get("description")) is not None:
                challenges[-1]["description"] = desc.replace("&&1", str(amounts[-1]))

        return challenges


class TurboChallenges:
    """Tomogunchi Turbo Challenges XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Tomogunchi Turbo Challenges XAssets."""

        challenges: List[Dict[str, Any]] = []

        challenges = TurboChallenges.Table(self, challenges)

        Utility.WriteFile(self, f"{self.eXAssets}/turboChallenges.json", challenges)

        log.info(f"Compiled {len(challenges):,} Tomogunchi Turbo Challenges")

    def Table(self: Any, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/petwatchturbotable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/petwatchturbotable.csv", PetWatchTurboTable
        )

        if table is None:
            return challenges

        for entry in table:
            challenges.append(
                {
                    "altId": entry.get("ref"),
                    "phase": entry.get("phaseNum"),
                    "description": self.localize.get(entry.get("challengeDesc")),
                    "phaseTime": entry.get("phaseTime"),
                    "maxBonusTime": entry.get("bonusTimeMax"),
                    "charmAltId": None
                    if (cid := entry.get("charmID")) is None
                    else f"cos_{cid}",
                }
            )

        return challenges


class MiscellaneousChallenges:
    """Miscellaneous Challenges XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Miscellaneous Challenges XAssets."""

        challenges: List[Dict[str, Any]] = []

        challenges = MiscellaneousChallenges.Table(self, challenges)

        Utility.WriteFile(self, f"{self.eXAssets}/miscChallenges.json", challenges)

        log.info(f"Compiled {len(challenges):,} Miscellaneous Challenges")

    def Table(self: Any, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the misc_challenges.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/misc_challenges.csv", MiscChallenges
        )

        if table is None:
            return challenges

        for entry in table:
            if (d := self.localize.get(entry.get("desc"))) is not None:
                desc: Optional[str] = d
            elif (d := self.localize.get(entry.get("detailDesc"))) is not None:
                desc = d
            else:
                desc = None

            challenges.append(
                {
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "description": desc,
                    "rewards": [
                        {
                            "id": entry.get("loot"),
                            "type": self.ModernWarfare.GetLootType(entry.get("loot")),
                        }
                    ],
                }
            )

        return challenges
