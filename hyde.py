import logging
from pathlib import Path
from sys import exit
from typing import Any, List

import coloredlogs

from modernwarfare import ModernWarfare

log: logging.Logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="[%(asctime)s] %(message)s", datefmt="%I:%M:%S")


class Hyde:
    """Call of Duty XAsset compiler."""

    def Start(self: Any) -> None:
        """Begin compiling all available XAssets for the supported titles."""

        print("Hyde: Call of Duty XAsset Compiler")
        print("https://github.com/EthanC/Hyde\n")

        directories: List[Path] = [
            Path("import/Modern Warfare/Images"),
            Path("import/Modern Warfare/Videos"),
            Path("export/Modern Warfare/DB/Images"),
            Path("export/Modern Warfare/DB/Videos"),
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        # Call of Duty: Modern Warfare
        log.info("Compiling Call of Duty: Modern Warfare XAssets...")
        ModernWarfare.__init__(self)
        ModernWarfare.CompileAccessories(self)
        ModernWarfare.CompileBattlePasses(self)
        ModernWarfare.CompileBattlePassItems(self)
        ModernWarfare.CompileBundles(self)
        ModernWarfare.CompileCallingCards(self)
        ModernWarfare.CompileCamos(self)
        ModernWarfare.CompileCharms(self)
        ModernWarfare.CompileConsumables(self)
        ModernWarfare.CompileEmblems(self)
        ModernWarfare.CompileExecutions(self)
        ModernWarfare.CompileFeatures(self)
        ModernWarfare.CompileGestures(self)
        ModernWarfare.CompileOfficerChallenges(self)
        ModernWarfare.CompileOperators(self)
        ModernWarfare.CompileQuips(self)
        ModernWarfare.CompileSkins(self)
        ModernWarfare.CompileSpecialItems(self)
        ModernWarfare.CompileSprays(self)
        ModernWarfare.CompileStickers(self)
        ModernWarfare.CompileVehicles(self)
        ModernWarfare.CompileVehicleCamos(self)
        ModernWarfare.CompileWeapons(self)
        ModernWarfare.CompileWeaponUnlockChallenges(self)
        ModernWarfare.CompileWeeklyBRChallenges(self)
        ModernWarfare.CompileWeeklyMPChallenges(self)
        ModernWarfare.CompileDatabase(self, False)


if __name__ == "__main__":
    try:
        Hyde.Start(Hyde)
    except KeyboardInterrupt:
        exit()
