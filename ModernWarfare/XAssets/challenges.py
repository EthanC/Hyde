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
