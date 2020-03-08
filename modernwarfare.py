import logging
from typing import Any, Dict, List, Optional, Union

from util import Utility

log: logging.Logger = logging.getLogger(__name__)


class ModernWarfare:
    """Call of Duty: Modern Warfare (2019)"""

    def __init__(self: Any):
        # Types
        self.csv = Optional[List[List[str]]]
        self.json = Optional[Dict[str, str]]

        # Global / Reused XAssets
        self.localize: self.json = Utility.ReadFile(
            self, "import/Modern Warfare/", "localize", "json"
        )
        self.lootMaster: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "loot_master", "csv"
        )

    def GetLootType(self: Any, value: int) -> Optional[Union[str, int]]:
        """
        Return the loot type for the given id.

        Requires loot_master.csv
        """

        # Skip the first row of loot_master.csv
        for row in self.lootMaster[1:]:
            if (value >= Utility.GetColumn(self, row[0])) and (
                value <= Utility.GetColumn(self, row[1])
            ):
                return ModernWarfare.GetLocalize(self, row[5])

    def GetLootRarity(self: Any, value: int) -> Optional[str]:
        """
        Return the loot rarity for the given value.
        
        Requires localize.json
        """

        return ModernWarfare.GetLocalize(self, f"LOOT_MP/QUALITY_{value}")

    def GetLocalize(self: Any, key: str) -> Optional[str]:
        """
        Return the localized string for the requested key.
        
        Requires localize.json
        """

        value: Optional[str] = self.localize.get(key)

        if value is None:
            return None
        elif value == "":
            return None
        else:
            return Utility.StripColors(self, value)

    def CompileAccessories(self: Any) -> None:
        """
        Compile the Accessory XAssets.
        
        Requires accessory_ids.csv and accessorytable.csv
        """

        accessoryIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "accessory_ids", "csv"
        )
        accessoryTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "accessorytable", "csv"
        )

        if (accessoryIds is None) or (accessoryTable is None):
            return

        accessories: List[dict] = []

        # Skip the first row of accessory_ids.csv and accessorytable.csv
        for idRow, tableRow in zip(accessoryIds[1:], accessoryTable[1:]):
            if (idColumn := Utility.GetColumn(self, idRow[1])) != Utility.GetColumn(
                self, tableRow[0]
            ):
                tableRow: Optional[List[str]] = Utility.GetRow(
                    self, str(idColumn), accessoryTable, 0
                )

                if tableRow is None:
                    log.warning(
                        f"Mismatch in accessory_ids.csv, {idColumn} does not exist in accessorytable.csv"
                    )

                    continue

            accessories.append(
                {
                    "id": Utility.GetColumn(self, idRow[0]),
                    "name": ModernWarfare.GetLocalize(self, tableRow[4]),
                    "description": ModernWarfare.GetLocalize(self, tableRow[5]),
                    "flavor": ModernWarfare.GetLocalize(
                        self, f"STORE_FLAVOR/{idRow[1].upper()}_FLAVOR"
                    ),
                    "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                    "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                    "image": Utility.GetColumn(self, tableRow[14]),
                }
            )

        search: str = ""
        for accessory in accessories:
            if (image := accessory["image"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "accessories", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "accessories", "json", accessories
        )

        if status is True:
            log.info(f"Compiled {len(accessories)} Accessories")

    def CompileBundles(self: Any) -> None:
        """
        Compile the Bundle XAssets.
        
        Requires bundle_ids.csv
        """

        bundleIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "bundle_ids", "csv"
        )

        if bundleIds is None:
            return

        bundles: List[dict] = []

        for row in bundleIds:
            items: List[dict] = []
            for i in range(14, 24):
                if Utility.GetColumn(self, row[i]) is not None:
                    items.append(
                        {
                            "id": Utility.GetColumn(self, row[i]),
                            "type": ModernWarfare.GetLootType(self, int(row[i])),
                        }
                    )

            bundles.append(
                {
                    "id": Utility.GetColumn(self, row[0]),
                    "name": ModernWarfare.GetLocalize(self, row[1]),
                    "description": ModernWarfare.GetLocalize(self, row[2]),
                    "flavor": ModernWarfare.GetLocalize(self, row[3]),
                    "type": ModernWarfare.GetLocalize(self, row[5]),
                    "billboard": Utility.GetColumn(self, row[6]),
                    "logo": Utility.GetColumn(self, row[8]),
                    "price": Utility.GetColumn(self, row[10]),
                    "items": items,
                }
            )

        search: str = ""
        for bundle in bundles:
            if (image := bundle["billboard"]) is not None:
                search += f"{image},"
            if (image := bundle["logo"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "bundles", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "bundles", "json", bundles
        )

        if status is True:
            log.info(f"Compiled {len(bundles)} Bundles")

    def CompileCallingCards(self: Any) -> None:
        """
        Compile the Calling Card XAssets.
        
        Requires playercards_ids.csv and callingcards.csv
        """

        cardIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "playercards_ids", "csv"
        )
        cardTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "callingcards", "csv"
        )

        if (cardIds is None) or (cardTable is None):
            return

        cards: List[dict] = []

        # Skip the first row of callingcards.csv
        for idRow, tableRow in zip(cardIds, cardTable[1:]):
            if (idColumn := Utility.GetColumn(self, idRow[1])) != Utility.GetColumn(
                self, tableRow[1]
            ):
                tableRow: Optional[List[str]] = Utility.GetRow(
                    self, str(idColumn), cardTable, 1
                )

                if tableRow is None:
                    log.warning(
                        f"Mismatch in playercards_ids.csv, {idColumn} does not exist in callingcards.csv"
                    )

                    continue

            cards.append(
                {
                    "id": Utility.GetColumn(self, idRow[0]),
                    "name": ModernWarfare.GetLocalize(self, tableRow[3]),
                    "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                    "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                    "image": Utility.GetColumn(self, idRow[1]),
                }
            )

        search: str = ""
        for card in cards:
            if (image := card["image"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "callingCards", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "callingCards", "json", cards
        )

        if status is True:
            log.info(f"Compiled {len(cards)} Calling Cards")

    def CompileCamos(self: Any) -> None:
        """
        Compile the Camo XAssets.
        
        Requires camo_ids.csv and camotable.csv
        """

        camoIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "camo_ids", "csv"
        )
        camoTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "camotable", "csv"
        )

        if (camoIds is None) or (camoTable is None):
            return

        camos: List[dict] = []

        # Skip the first row of camotable.csv
        for idRow, tableRow in zip(camoIds, camoTable[1:]):
            if (idColumn := Utility.GetColumn(self, idRow[1])) != Utility.GetColumn(
                self, tableRow[1]
            ):
                tableRow: Optional[List[str]] = Utility.GetRow(
                    self, str(idColumn), camoTable, 1
                )

                if tableRow is None:
                    log.warning(
                        f"Mismatch in camo_ids.csv, {idColumn} does not exist in camotable.csv"
                    )

                    continue

            camos.append(
                {
                    "id": Utility.GetColumn(self, idRow[0]),
                    "name": ModernWarfare.GetLocalize(self, tableRow[7]),
                    "category": Utility.GetColumn(self, tableRow[3]),
                    "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                    "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                    "unlock": Utility.GetColumn(self, tableRow[4]),
                    "image": Utility.GetColumn(self, tableRow[8]),
                }
            )

        for camo in camos:
            if camo["category"] is not None:
                camo["category"] = camo["category"].capitalize()

            if camo["unlock"] is not None:
                camo["unlock"] = camo["unlock"].capitalize()

        search: str = ""
        for camo in camos:
            if (image := camo["image"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "camos", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "camos", "json", camos
        )

        if status is True:
            log.info(f"Compiled {len(camos)} Camos")

    def CompileCharms(self: Any) -> None:
        """
        Compile the Charm XAssets.
        
        Requires weapon_charm_ids.csv and weaponcharmtable.csv
        """

        charmIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "weapon_charm_ids", "csv"
        )
        charmTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "weaponcharmtable", "csv"
        )

        if (charmIds is None) or (charmTable is None):
            return

        charms: List[dict] = []

        # Skip the first row of weaponcharmtable.csv
        for idRow, tableRow in zip(charmIds, charmTable[1:]):
            if (idColumn := Utility.GetColumn(self, idRow[1])) != Utility.GetColumn(
                self, tableRow[1]
            ):
                tableRow: Optional[List[str]] = Utility.GetRow(
                    self, str(idColumn), charmTable, 1
                )

                if tableRow is None:
                    log.warning(
                        f"Mismatch in weapon_charm_ids.csv, {idColumn} does not exist in weaponcharmtable.csv"
                    )

                    continue

            charms.append(
                {
                    "id": Utility.GetColumn(self, idRow[0]),
                    "name": ModernWarfare.GetLocalize(self, tableRow[2]),
                    "flavor": ModernWarfare.GetLocalize(
                        self, f"STORE_FLAVOR/{idRow[1].upper()}_FLAVOR"
                    ),
                    "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                    "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                    "image": Utility.GetColumn(self, tableRow[3]),
                }
            )

        search: str = ""
        for charm in charms:
            if (image := charm["image"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "charms", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "charms", "json", charms
        )

        if status is True:
            log.info(f"Compiled {len(charms)} Charms")

    def CompileEmblems(self: Any) -> None:
        """
        Compile the Emblem XAssets.
        
        Requires emblems_ids.csv and emblemtable.csv
        """

        emblemIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "emblems_ids", "csv"
        )
        emblemTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "emblemtable", "csv"
        )

        if (emblemIds is None) or (emblemTable is None):
            return

        emblems: List[dict] = []

        # Skip the first row of emblemtable.csv
        for idRow, tableRow in zip(emblemIds, emblemTable[1:]):
            if (idColumn := Utility.GetColumn(self, idRow[1])) != Utility.GetColumn(
                self, tableRow[1]
            ):
                tableRow: Optional[List[str]] = Utility.GetRow(
                    self, str(idColumn), emblemTable, 1
                )

                if tableRow is None:
                    log.warning(
                        f"Mismatch in emblems_ids.csv, {idColumn} does not exist in emblemtable.csv"
                    )

                    continue

            emblems.append(
                {
                    "id": Utility.GetColumn(self, idRow[0]),
                    "name": ModernWarfare.GetLocalize(self, tableRow[3]),
                    "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                    "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                    "image": Utility.GetColumn(self, tableRow[1]),
                }
            )

        search: str = ""
        for emblem in emblems:
            if (image := emblem["image"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "emblems", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "emblems", "json", emblems
        )

        if status is True:
            log.info(f"Compiled {len(emblems)} Emblems")

    def CompileExecutions(self: Any) -> None:
        """
        Compile the Finishing Move XAssets.
        
        Requires executions_ids.csv, executiontable.csv, and operators.csv
        """

        executionIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "executions_ids", "csv"
        )
        executionTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "executiontable", "csv"
        )

        if (executionIds is None) or (executionTable is None):
            return

        executions: List[dict] = []

        # Skip the first 3 rows of executiontable.csv
        for idRow, tableRow in zip(executionIds, executionTable[3:]):
            if (idColumn := Utility.GetColumn(self, idRow[1])) != Utility.GetColumn(
                self, tableRow[1]
            ):
                tableRow: Optional[List[str]] = Utility.GetRow(
                    self, str(idColumn), executionTable, 1
                )

                if tableRow is None:
                    # Set to debug because there are typically many missing executions
                    log.debug(
                        f"Mismatch in executions_ids.csv, {idColumn} does not exist in executiontable.csv"
                    )

                    continue

            executions.append(
                {
                    "id": Utility.GetColumn(self, idRow[0]),
                    "name": ModernWarfare.GetLocalize(self, tableRow[3]),
                    "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                    "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                    "operatorId": None,  # This is determined later
                    "operator": Utility.GetColumn(self, tableRow[2]),
                    "image": Utility.GetColumn(self, tableRow[17]),
                    "video": Utility.GetColumn(self, tableRow[11]),
                }
            )

        opsTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "operators", "csv"
        )

        if opsTable is not None:
            for execution in executions:
                if execution["operator"] is None:
                    continue

                if execution["operator"] == "universal_ref":
                    execution["operator"] = "Universal"

                    continue

                for opRow in opsTable:
                    if Utility.GetColumn(self, opRow[1]) == execution["operator"]:
                        execution["operatorId"] = Utility.GetColumn(self, opRow[0])

                        if (
                            name := ModernWarfare.GetLocalize(self, opRow[2])
                        ) is not None:
                            execution["operator"] = name.capitalize()

        search: str = ""
        for execution in executions:
            if (image := execution["image"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "executions", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "executions", "json", executions
        )

        if status is True:
            log.info(f"Compiled {len(executions)} Executions")

    def CompileQuips(self: Any) -> None:
        """
        Compile the Operator Quip XAssets.
        
        Requires operator_quip_ids.csv and operatorquips.csv
        """

        quipIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "operator_quip_ids", "csv"
        )
        quipTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "operatorquips", "csv"
        )

        if (quipIds is None) or (quipTable is None):
            return

        quips: List[dict] = []

        # Skip the first row of operatorquips.csv
        for idRow, tableRow in zip(quipIds, quipTable[1:]):
            if (idColumn := Utility.GetColumn(self, idRow[1])) != Utility.GetColumn(
                self, tableRow[1]
            ):
                tableRow: Optional[List[str]] = Utility.GetRow(
                    self, str(idColumn), quipTable, 1
                )

                if tableRow is None:
                    log.warning(
                        f"Mismatch in operator_quip_ids.csv, {idColumn} does not exist in operatorquips.csv"
                    )

                    continue

            quips.append(
                {
                    "id": Utility.GetColumn(self, idRow[0]),
                    "name": ModernWarfare.GetLocalize(self, tableRow[3]),
                    "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                    "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                    "image": Utility.GetColumn(self, tableRow[4]),
                }
            )

        search: str = ""
        for quip in quips:
            if (image := quip["image"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "quips", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "quips", "json", quips
        )

        if status is True:
            log.info(f"Compiled {len(quips)} Quips")

    def CompileSkins(self: Any) -> None:
        """
        Compile the Operator Skin XAssets.
        
        Requires operator_skin_ids.csv, operatorskins.csv, and operators.csv
        """

        skinIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "operator_skin_ids", "csv"
        )
        skinTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "operatorskins", "csv"
        )

        if (skinIds is None) or (skinTable is None):
            return

        skins: List[dict] = []

        for idRow, tableRow in zip(skinIds, skinTable):
            if (idColumn := Utility.GetColumn(self, idRow[1])) != Utility.GetColumn(
                self, tableRow[1]
            ):
                tableRow: Optional[List[str]] = Utility.GetRow(
                    self, str(idColumn), skinTable, 1
                )

                if tableRow is None:
                    log.warning(
                        f"Mismatch in operator_skin_ids.csv, {idColumn} does not exist in operatorskins.csv"
                    )

                    continue

            skins.append(
                {
                    "id": Utility.GetColumn(self, idRow[0]),
                    "name": ModernWarfare.GetLocalize(self, tableRow[3]),
                    "description": ModernWarfare.GetLocalize(self, tableRow[15]),
                    "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                    "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                    "operatorId": None,  # This is determined later
                    "operator": Utility.GetColumn(self, tableRow[2]),
                    "image": Utility.GetColumn(self, tableRow[18]),
                }
            )

        opsTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "operators", "csv"
        )

        if opsTable is not None:
            for skin in skins:
                if skin["operator"] is None:
                    continue

                for opRow in opsTable:
                    if Utility.GetColumn(self, opRow[1]) == skin["operator"]:
                        skin["operatorId"] = Utility.GetColumn(self, opRow[0])

                        if (
                            name := ModernWarfare.GetLocalize(self, opRow[2])
                        ) is not None:
                            skin["operator"] = name.capitalize()

        search: str = ""
        for skin in skins:
            if (image := skin["image"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "skins", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "skins", "json", skins
        )

        if status is True:
            log.info(f"Compiled {len(skins)} Skins")

    def CompileSprays(self: Any) -> None:
        """
        Compile the Spray XAssets.
        
        Requires sprays_ids.csv and spraytable.csv
        """

        sprayIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "sprays_ids", "csv"
        )
        sprayTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "spraytable", "csv"
        )

        if (sprayIds is None) or (sprayTable is None):
            return

        sprays: List[dict] = []

        for idRow, tableRow in zip(sprayIds, sprayTable):
            if (idColumn := Utility.GetColumn(self, idRow[1])) != Utility.GetColumn(
                self, tableRow[1]
            ):
                tableRow: Optional[List[str]] = Utility.GetRow(
                    self, str(idColumn), sprayTable, 1
                )

                if tableRow is None:
                    log.warning(
                        f"Mismatch in sprays_ids.csv, {idColumn} does not exist in spraytable.csv"
                    )

                    continue

            sprays.append(
                {
                    "id": Utility.GetColumn(self, idRow[0]),
                    "name": ModernWarfare.GetLocalize(self, tableRow[2]),
                    "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                    "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                    "image": Utility.GetColumn(self, tableRow[3]),
                }
            )

        search: str = ""
        for spray in sprays:
            if (image := spray["image"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "sprays", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "sprays", "json", sprays
        )

        if status is True:
            log.info(f"Compiled {len(sprays)} Sprays")

    def CompileStickers(self: Any) -> None:
        """
        Compile the Sticker XAssets.
        
        Requires sticker_ids.csv and weaponstickertable.csv
        """

        stickerIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "sticker_ids", "csv"
        )
        stickerTable: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "weaponstickertable", "csv"
        )

        if (stickerIds is None) or (stickerTable is None):
            return

        stickers: List[dict] = []

        # Skip the first 5 rows of weaponstickertable.csv
        for idRow, tableRow in zip(stickerIds, stickerTable[5:]):
            if (idColumn := Utility.GetColumn(self, idRow[1])) != Utility.GetColumn(
                self, tableRow[1]
            ):
                tableRow: Optional[List[str]] = Utility.GetRow(
                    self, str(idColumn), stickerTable, 1
                )

                if tableRow is None:
                    log.warning(
                        f"Mismatch in sticker_ids.csv, {idColumn} does not exist in weaponstickertable.csv"
                    )

                    continue

            stickers.append(
                {
                    "id": Utility.GetColumn(self, idRow[0]),
                    "name": ModernWarfare.GetLocalize(self, tableRow[3]),
                    "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                    "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                    "image": Utility.GetColumn(self, tableRow[4]),
                }
            )

        search: str = ""
        for sticker in stickers:
            if (image := sticker["image"]) is not None:
                search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "stickers", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "stickers", "json", stickers
        )

        if status is True:
            log.info(f"Compiled {len(stickers)} Stickers")

    def CompileWeapons(self: Any) -> None:
        """
        Compile the Weapon and Weapon Variant XAssets.
        
        Requires weapon_ids.csv and X_Y_variants.csv (for each weapon)
        """

        weaponIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "weapon_ids", "csv"
        )

        if weaponIds is None:
            return

        weapons = {}
        count: int = 0

        for idRow in weaponIds:
            if weapons.get((w := Utility.GetColumn(self, idRow[1]))) is None:
                weapons[w] = {}
                weapons[w]["id"] = Utility.GetColumn(self, idRow[0])
                weapons[w]["name"] = Utility.GetColumn(self, idRow[6])
                weapons[w]["description"] = None  # This is determined later
                weapons[w]["flavor"] = None  # This is determined later
                weapons[w]["type"] = ModernWarfare.GetLootType(self, int(idRow[0]))
                weapons[w]["rarity"] = ModernWarfare.GetLootRarity(self, int(idRow[2]))
                weapons[w]["image"] = None  # This is determined later
                weapons[w]["icon"] = f"icon_cac_weapon_{str(w)[4:]}"
                # weapons[w]["attachments"] = [] # TODO
                weapons[w]["variants"] = []

                if w is not None:
                    weapons[w]["description"] = ModernWarfare.GetLocalize(
                        self, f"PERKS/{str(w)[4:].upper()}"
                    )

                if Utility.GetColumn(self, idRow[6]) is not None:
                    n = (
                        str(Utility.GetColumn(self, idRow[6]))[4:]
                        .upper()
                        .replace("VARIANT_", "")
                    )
                    weapons[w]["flavor"] = ModernWarfare.GetLocalize(
                        self, f"WEAPON_FLAVOR/{n}_FLAVOR"
                    )
            else:
                weapons[w]["variants"].append(
                    {
                        "id": Utility.GetColumn(self, idRow[0]),
                        "name": Utility.GetColumn(self, idRow[6]),
                        "description": None,  # This is determined later
                        "flavor": None,  # This is determined later
                        "type": ModernWarfare.GetLootType(self, int(idRow[0])),
                        "rarity": ModernWarfare.GetLootRarity(self, int(idRow[2])),
                        "baseId": weapons[w]["id"],
                        "base": Utility.GetColumn(self, idRow[1]),
                        "image": None,
                        # "attachments": [], # TODO
                    }
                )

            count += 1

        for weapon in weapons:
            if (n := weapons[weapon]["name"]) is None:
                continue

            filename: str = Utility.FindBetween(self, n, "iw8_", "_variant")
            variants: self.csv = Utility.ReadFile(
                self, "import/Modern Warfare/Weapons/", f"{filename}_variants", "csv"
            )

            if variants is None:
                continue

            for varRow in variants:
                if Utility.GetColumn(self, varRow[1]) == n:
                    weapons[weapon]["name"] = ModernWarfare.GetLocalize(
                        self, varRow[17]
                    )
                    weapons[weapon]["image"] = Utility.GetColumn(self, varRow[18])

                    continue

                for variant in weapons[weapon]["variants"]:
                    if Utility.GetColumn(self, varRow[1]) is None:
                        continue

                    n: str = str(Utility.GetColumn(self, varRow[1]))
                    if n == variant["name"]:
                        variant["name"] = ModernWarfare.GetLocalize(self, varRow[17])
                        variant["image"] = Utility.GetColumn(self, varRow[18])

                        n: str = n[4:].replace("variant_", "").upper()
                        variant["flavor"] = ModernWarfare.GetLocalize(
                            self, f"WEAPON_FLAVOR/{n}_FLAVOR"
                        )

        search: str = ""
        for weapon in weapons:
            if (image := weapons[weapon]["image"]) is not None:
                search += f"{image},"

            if (image := weapons[weapon]["icon"]) is not None:
                search += f"{image},"

            for variant in weapons[weapon]["variants"]:
                if (image := variant["image"]) is not None:
                    search += f"{image},"

        Utility.WriteFile(
            self, "export/Modern Warfare/Search Strings/", "weapons", "txt", search
        )

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "weapons", "json", weapons
        )

        if status is True:
            log.info(f"Compiled {count} Weapons")

    def CompileWeeklyChallenges(self: Any) -> None:
        """
        Compile the Weekly Challenge XAssets.
        
        Requires weekly_challenges.csv
        """

        challengeIds: self.csv = Utility.ReadFile(
            self, "import/Modern Warfare/", "weekly_challenges", "csv"
        )

        if challengeIds is None:
            return

        count: int = 0
        challenges = {}

        for challenge in challengeIds:
            s: str = str(Utility.GetColumn(self, challenge[1])).split("_")[2]
            if challenges.get(f"season{s}") is None:
                challenges[f"season{s}"] = {}

            w: str = str(Utility.GetColumn(self, challenge[1])).split("_")[4]
            if challenges[f"season{s}"].get(f"week{w}") is None:
                challenges[f"season{s}"][f"week{w}"] = []

            challenges[f"season{s}"][f"week{w}"].append(
                {
                    "id": Utility.GetColumn(self, challenge[0]),
                    "name": ModernWarfare.GetLocalize(self, challenge[2]),
                    "description": ModernWarfare.GetLocalize(
                        self, challenge[3]
                    ).replace("&&1", challenge[4]),
                    "amount": Utility.GetColumn(self, challenge[4]),
                    "reward": Utility.GetColumn(self, challenge[5]),
                    "start": Utility.GetColumn(self, challenge[7]),
                    "end": Utility.GetColumn(self, challenge[8]),
                }
            )

            count += 1

        status: bool = Utility.WriteFile(
            self, "export/Modern Warfare/", "weeklyChallenges", "json", challenges
        )

        if status is True:
            log.info(f"Compiled {count} Weekly Challenges")
