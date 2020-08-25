import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class BundleIDs(TypedDict):
    """Structure of loot/bundle_ids.csv"""

    id: int
    name: str
    description: str
    flavorText: str
    license: int
    bundleType: str
    image: str
    previewImage: str
    titleImage: str
    currencyID: int
    currencyAmount: int
    saleCurrencyAmount: int
    firstPartyProductID: str
    numItems: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int
    item7: int
    item8: int
    item9: int
    item10: int
    numHiddenItems: int
    hiddenItem1: int
    hiddenItem2: int
    hiddenItem3: int
    hiddenItem4: int
    hiddenItem5: int
    hiddenItem6: int
    hiddenItem7: int
    hiddenItem8: int
    hiddenItem9: int
    hiddenItem10: int
    smartID: int
    smartCost: int
    isBattlePassBundle: int  # bool
    purchaseEnd: str
    dlcRef: str
    oldBundleOwnershipID: int
    isCollection: int  # bool
    ref: str
    minTierInclude: int
    maxTierInclude: int
    battlePassID: int
    collectionName: str
    collectionImage: str
    collectionPreviewImage: str
    featureText: str


class Bundles:
    """Bundle XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Bundle XAssets."""

        bundles: List[Dict[str, Any]] = []

        bundles = Bundles.IDs(self, bundles)

        Utility.WriteFile(self, f"{self.eXAssets}/bundles.json", bundles)

        log.info(f"Compiled {len(bundles):,} Bundles")

    def IDs(self: Any, bundles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/bundle_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/bundle_ids.csv", BundleIDs
        )

        if ids is None:
            return bundles

        for entry in ids:
            if bool(entry.get("isCollection")) is False:
                bundles.append(
                    {
                        "id": entry.get("id"),
                        "altId": entry.get("ref"),
                        "name": self.localize.get(entry.get("name")),
                        "description": self.localize.get(entry.get("description")),
                        "flavor": self.localize.get(entry.get("flavorText")),
                        "feature": self.localize.get(entry.get("featureText")),
                        "type": self.localize.get(entry.get("bundleType")),
                        "season": self.ModernWarfare.GetLootSeason(
                            entry.get("license")
                        ),
                        "billboard": None
                        if (i := entry.get("image")) == "placeholder_x"
                        else i,
                        "logo": None
                        if (i := entry.get("titleImage")) == "placeholder_x"
                        else i,
                        "price": None
                        if ((p := entry.get("currencyAmount")) == 99) or (p == 10000)
                        else p,
                        "items": [],
                        "hiddenItems": [],
                    }
                )

            for i in range(1, entry.get("numItems") + 1):
                if (item := entry.get(f"item{i}")) is None:
                    continue

                bundles[-1]["items"].append(
                    {"id": item, "type": self.ModernWarfare.GetLootType(item),}
                )

            for i in range(1, entry.get("numHiddenItems") + 1):
                if (item := entry.get(f"hiddenItem{i}")) is None:
                    continue

                bundles[-1]["hiddenItems"].append(
                    {"id": item, "type": self.ModernWarfare.GetLootType(item),}
                )

        return bundles
