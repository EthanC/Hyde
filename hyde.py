import logging
from sys import exit
from typing import Any, Dict, Optional

import coloredlogs

from ModernWarfare import ModernWarfare
from utility import Utility

log: logging.Logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="[%(asctime)s] %(message)s", datefmt="%I:%M:%S")


class Hyde:
    """
    Call of Duty XAsset compiler that transforms raw assets into
    digestible data.
    """

    def Initialize(self: Any) -> None:
        """Configure the application and begin its main functionality."""

        print("Hyde: Call of Duty XAsset Compiler")
        print("https://github.com/EthanC/Hyde\n")

        self.config: Dict[str, Any] = Hyde.LoadConfiguration(self)

        if self.config is None:
            return

        log.info("Loaded configuration")

        if self.config["ModernWarfare"]["enabled"] is True:
            self.ModernWarfare = ModernWarfare(self.config)
            self.ModernWarfare.Compile()

    def LoadConfiguration(self: Any) -> Dict[str, Any]:
        """Load the configurable values from config.json"""

        config: Optional[Dict[str, Any]] = Utility.ReadFile(self, "config.json")

        if config is not None:
            return dict(config)


if __name__ == "__main__":
    try:
        Hyde.Initialize(Hyde)
    except KeyboardInterrupt:
        exit()
