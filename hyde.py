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
            Path("import/Modern Warfare"),
            Path("export/Modern Warfare/Search Strings"),
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        # Call of Duty: Modern Warfare
        log.info("Compiling Call of Duty: Modern Warfare XAssets...")
        ModernWarfare.__init__(self)
        ModernWarfare.CompileAccessories(self)
        ModernWarfare.CompileBundles(self)
        ModernWarfare.CompileCallingCards(self)
        ModernWarfare.CompileCamos(self)
        ModernWarfare.CompileCharms(self)
        ModernWarfare.CompileEmblems(self)
        ModernWarfare.CompileExecutions(self)
        ModernWarfare.CompileQuips(self)
        ModernWarfare.CompileSkins(self)
        ModernWarfare.CompileSprays(self)
        ModernWarfare.CompileStickers(self)
        ModernWarfare.CompileWeapons(self)
        ModernWarfare.CompileWeeklyChallenges(self)


if __name__ == "__main__":
    try:
        Hyde.Start(Hyde)
    except KeyboardInterrupt:
        exit()
