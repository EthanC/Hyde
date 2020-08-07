import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class FeatureIDs(TypedDict):
    """Structure of loot/feature_ids.csv"""

    index: int
    ref: str
    quality: int
    cost: int
    salvage: int
    license: int
    name: str
    desc: str
    image: str
    hudImage: str
    operatorSkinRef: str


class Features:
    """Feature XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Feature XAssets."""

        features: List[Dict[str, Any]] = []

        features = Features.IDs(self, features)

        Utility.WriteFile(self, f"{self.eXAssets}/features.json", features)

        log.info(f"Compiled {len(features):,} Features")

    def IDs(self: Any, features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/feature_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/feature_ids.csv", FeatureIDs
        )

        if ids is None:
            return features

        for entry in ids:
            features.append(
                {
                    "id": entry.get("index"),
                    "altId": entry.get("ref"),
                    "name": None
                    if (n := self.localize.get(entry.get("name"))) is None
                    else n.replace("&&1 ", ""),
                    "description": self.localize.get(entry.get("desc")),
                    "type": self.ModernWarfare.GetLootType(entry.get("index")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("quality")),
                    "image": None if (i := entry.get("hudImage")) == "white" else i,
                    "background": "ui_loot_bg_generic",
                }
            )

        return features
