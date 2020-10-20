import logging
from typing import Any, Dict, List

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class Database:
    """
    XAssets used in the COD Tracker Database.
    https://cod.tracker.gg/warzone/db
    """

    def Compile(self: Any) -> None:
        """Compile the XAssets for the COD Tracker Database."""

        self.dbImages: List[str] = []
        self.count: int = 0

        DBBattlePasses.Compile(self)
        DBBundles.Compile(self)
        DBLoot.Compile(self)
        DBOperators.Compile(self)
        DBWeapons.Compile(self)

        Utility.WriteFile(
            self, f"{self.eDatabase}/_images.txt", ",".join(list(set(self.dbImages)))
        )

        log.info(f"Compiled {self.count:,} Database Items")


class DBBattlePasses:
    """Battle Pass XAssets for the COD Tracker Database."""

    def Compile(self: Any) -> None:
        """Compile the Battle Pass XAssets for the COD Tracker Database."""

        dbPasses: List[Dict[str, Any]] = []
        passes: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/battlePasses.json"
        )

        for battlePass in passes:
            if battlePass.get("name") is None:
                continue

            items: List[Dict[str, Any]] = []

            for item in battlePass.get("items"):
                item.pop("type")
                item.pop("billboard")

                items.append(item)

            dbPasses.append(battlePass)
            self.count += 1

        Utility.WriteFile(
            self,
            f"{self.eDatabase}/battlePasses.json",
            dbPasses,
            compress=True,
        )
        Utility.WriteFile(self, f"{self.eDatabase}/_battlePasses.json", dbPasses)


class DBBundles:
    """Bundle XAssets for the COD Tracker Database."""

    def Compile(self: Any) -> None:
        """Compile the Bundle XAssets for the COD Tracker Database."""

        dbBundles: List[Dict[str, Any]] = []
        bundles: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/bundles.json"
        )

        for bundle in bundles:
            if bundle.get("id") is None:
                continue
            elif bundle.get("name") is None:
                continue
            elif (b := bundle.get("billboard")) is None:
                continue
            elif (l := bundle.get("logo")) is None:
                continue

            self.dbImages.append(b)
            self.dbImages.append(l)

            if Utility.FileExists(self, f"{self.iImages}/{b}.png") is False:
                continue
            elif Utility.FileExists(self, f"{self.iImages}/{l}.png") is False:
                continue

            items: List[int] = []

            for item in bundle.get("items"):
                items.append(item.get("id"))

            bundle["items"] = items

            bundle.pop("altId")
            bundle.pop("hiddenItems")

            if bundle.get("description") is None:
                bundle.pop("description")
            if bundle.get("flavor") is None:
                bundle.pop("flavor")
            if bundle.get("feature") is None:
                bundle.pop("feature")
            if bundle.get("season") is None:
                bundle.pop("season")
            if bundle.get("name") == bundle.get("flavor"):
                bundle.pop("flavor")

            bundle["slug"] = Utility.Sluggify(self, bundle.get("name"))

            dbBundles.append(bundle)
            self.count += 1

        Utility.WriteFile(
            self,
            f"{self.eDatabase}/bundles.json",
            Utility.SortList(self, dbBundles, "name", key2="type"),
            compress=True,
        )
        Utility.WriteFile(
            self,
            f"{self.eDatabase}/_bundles.json",
            Utility.SortList(self, dbBundles, "name", key2="type"),
        )


class DBLoot:
    """Loot XAssets for the COD Tracker Database."""

    def Compile(self: Any) -> None:
        """Compile the Loot XAssets for the COD Tracker Database."""

        dbLoot: List[Dict[str, Any]] = []
        loot: List[str] = [
            "accessories",
            "battlePassItems",
            "callingCards",
            "camos",
            "charms",
            "consumables",
            "emblems",
            "executions",
            "features",
            "gestures",
            "missionItems",
            "operatorQuips",
            "operatorSkins",
            "specialItems",
            "sprays",
            "stickers",
            "vehicleCamos",
            "vehicleHorns",
            "vehicleTracks",
        ]

        for file in loot:
            items: List[Dict[str, Any]] = Utility.ReadFile(
                self, f"{self.eXAssets}/{file}.json"
            )

            for item in items:
                if item.get("id") is None:
                    continue
                elif item.get("name") is None:
                    continue
                elif (i := item.get("image")) is None:
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                item.pop("altId", None)
                item.pop("hidden", None)
                item.pop("category", None)
                item.pop("operatorAltId", None)
                item.pop("pet", None)
                item.pop("video", None)
                item.pop("unlock", None)

                if item.get("description") is None:
                    item.pop("description", None)
                if item.get("flavor") is None:
                    item.pop("flavor", None)
                if item.get("season") is None:
                    item.pop("season", None)
                if item.get("attribute") is None:
                    item.pop("attribute", None)

                if (iType := item.get("type")) == "Calling Card":
                    item["animated"] = Utility.AnimateSprite(
                        self, i, [(512, 128), (512, 136), (960, 240)]
                    )
                elif iType == "Emblem":
                    item["animated"] = Utility.AnimateSprite(self, i, [(256, 256)])

                item["slug"] = Utility.Sluggify(self, item.get("name"))

                dbLoot.append(item)
                self.count += 1

        weapons: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/weapons.json"
        )

        for weapon in weapons:
            for variant in weapon.get("variants"):
                if variant.get("id") is None:
                    continue
                elif variant.get("name") is None:
                    continue
                elif (i := variant.get("image")) is None:
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                variant.pop("altId")

                if variant.get("flavor") is None:
                    variant.pop("flavor")
                if variant.get("season") is None:
                    variant.pop("season")
                if variant.get("tracers") is None:
                    variant.pop("tracers")
                if variant.get("dismemberment") is None:
                    variant.pop("dismemberment")

                variant["class"] = weapon.get("class")
                variant["baseId"] = weapon.get("id")
                variant["slug"] = Utility.Sluggify(self, variant.get("name"))

                dbLoot.append(variant)
                self.count += 1

        Utility.WriteFile(
            self,
            f"{self.eDatabase}/loot.json",
            Utility.SortList(self, dbLoot, "name", key2="rarity"),
            compress=True,
        )
        Utility.WriteFile(
            self,
            f"{self.eDatabase}/_loot.json",
            Utility.SortList(self, dbLoot, "name", key2="rarity"),
        )


class DBOperators:
    """Operator XAssets for the COD Tracker Database."""

    def Compile(self: Any) -> None:
        """Compile the Operator XAssets for the COD Tracker Database."""

        dbOperators: List[Dict[str, Any]] = []
        operators: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/operators.json"
        )
        skins: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/operatorSkins.json"
        )
        executions: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/executions.json"
        )
        quips: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/operatorQuips.json"
        )

        for operator in operators:
            if operator.get("id") is None:
                continue
            elif operator.get("name") is None:
                continue
            elif (i := operator.get("image")) is None:
                continue
            elif operator.get("name") == "Griggs":  # Temporary
                continue

            self.dbImages.append(i)

            if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                continue

            operator.pop("altId")
            operator.pop("type")
            operator.pop("rarity")
            operator.pop("branchIcon")
            operator.pop("thumbprint")
            operator.pop("launchOperator")
            operator.pop("video")
            operator.pop("hidden")
            operator.pop("billets")

            if operator.get("season") is None:
                operator.pop("season")
            if operator.get("description") is None:
                operator.pop("description")

            operator["skins"] = []
            operator["executions"] = []
            operator["quips"] = []
            operator["slug"] = Utility.Sluggify(self, operator.get("name"))

            for skin in Utility.SortList(self, skins, "name", key2="rarity"):
                if (skinId := skin.get("id")) is None:
                    continue
                elif skin.get("name") is None:
                    continue
                elif (i := skin.get("image")) is None:
                    continue
                elif (skinOpId := skin.get("operatorId")) is None:
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                if skinOpId == operator.get("id"):
                    operator["skins"].append(skinId)
                elif skinOpId == 29999:
                    operator["skins"].append(skinId)
                elif skinOpId == 29998:
                    if operator.get("launchOperator") is True:
                        operator["skins"].append(skinId)

            for execution in Utility.SortList(self, executions, "name", key2="rarity"):
                if (exId := execution.get("id")) is None:
                    continue
                elif execution.get("name") is None:
                    continue
                elif (i := execution.get("image")) is None:
                    continue
                elif (exOpId := execution.get("operatorId")) is None:
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                if exOpId == operator.get("id"):
                    operator["executions"].append(exId)
                elif exOpId == 29999:
                    operator["executions"].append(exId)

            for quip in Utility.SortList(self, quips, "name", key2="rarity"):
                if (quipId := quip.get("id")) is None:
                    continue
                elif quip.get("name") is None:
                    continue
                elif (i := quip.get("image")) is None:
                    continue
                elif (quipOpId := quip.get("operatorId")) is None:
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                if quipOpId == operator.get("id"):
                    operator["quips"].append(quipId)
                elif quipOpId == 29999:
                    operator["quips"].append(quipId)

            dbOperators.append(operator)
            self.count += 1

        Utility.WriteFile(
            self,
            f"{self.eDatabase}/operators.json",
            Utility.SortList(self, dbOperators, "name", key2="faction"),
            compress=True,
        )
        Utility.WriteFile(
            self,
            f"{self.eDatabase}/_operators.json",
            Utility.SortList(self, dbOperators, "name", key2="faction"),
        )


class DBWeapons:
    """Weapon XAssets for the COD Tracker Database."""

    def Compile(self: Any) -> None:
        """Compile the Weapon XAssets for the COD Tracker Database."""

        dbWeapons: List[Dict[str, Any]] = []
        weapons: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/weapons.json"
        )

        for weapon in weapons:
            if weapon.get("id") is None:
                continue
            if weapon.get("name") is None:
                continue
            if (i := weapon.get("image")) is None:
                continue
            if (ico := weapon.get("icon")) is None:
                continue

            self.dbImages.append(i)
            self.dbImages.append(ico)

            if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                continue
            elif Utility.FileExists(self, f"{self.iImages}/{ico}.png") is False:
                continue

            variants: List[int] = []

            for variant in Utility.SortList(
                self, weapon.get("variants"), "name", key2="rarity"
            ):
                if variant.get("id") is None:
                    continue
                elif variant.get("name") is None:
                    continue
                elif variant.get("image") is None:
                    continue

                variants.append(variant.get("id"))

            weapon["variants"] = variants

            attachments: List[int] = []

            for attachment in weapon.get("attachments"):
                if attachment.get("id") is None:
                    continue
                elif attachment.get("name") is None:
                    continue
                elif (i := attachment.get("image")) is None:
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                attachment.pop("altId")
                attachment.pop("unlock")

                if attachment.get("description") is None:
                    attachment.pop("description")

                attachments.append(attachment)

            weapon["attachments"] = Utility.SortList(
                self, attachments, "type", key2="name"
            )

            if weapon.get("description") is None:
                weapon.pop("description")
            if weapon.get("season") is None:
                weapon.pop("season")

            weapon["slug"] = Utility.Sluggify(self, weapon.get("name"))

            dbWeapons.append(weapon)
            self.count += 1

        Utility.WriteFile(
            self,
            f"{self.eDatabase}/weapons.json",
            Utility.SortList(self, dbWeapons, "name", key2="altName"),
            compress=True,
        )
        Utility.WriteFile(
            self,
            f"{self.eDatabase}/_weapons.json",
            Utility.SortList(self, dbWeapons, "name", key2="altName"),
        )
