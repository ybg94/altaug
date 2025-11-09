from collections import namedtuple
from enum import StrEnum, auto
import logging
import re
from .GuiModules.constants import CraftingTarget

class ItemRarity(StrEnum):
    NONE = auto()
    NORMAL = 'Normal'
    MAGIC = 'Magic'
    RARE = 'Rare'
    UNIQUE = 'Unique'

ITEM_BASE_REGEX = re.compile(r"^Item Class: (?P<class>[\w ]*)$\s*^Rarity:\s(?P<rarity>\w*)$.*^(?P<corrupted>Corrupted)?$", re.MULTILINE | re.DOTALL)
AFFIX_REGEX = re.compile(
    r"^{ (?:Master Crafted )?(?P<affix_type>Prefix|Suffix) Modifier \"(?P<affix_name>[\w\s'-]*)\" (?:\((?P<tier>(?:Rank|Tier): \d*)\))?[^(?:\r\n|\n|\r)]*$(?:\r\n|\n|\r)(?P<description>[^{]*?)(?=(?:\n\n))",
    re.MULTILINE
)

AffixInfo = namedtuple('AffixInfo', ['type', 'name', 'tier', 'description'])
class ItemInfo:
    def __init__(self, advanced_description: str):
        self.description = advanced_description.replace('\r\n', '\n').replace('\r', '\n')
        self.item_class: CraftingTarget = CraftingTarget.GEAR
        self.rarity: ItemRarity = ItemRarity.NONE
        self.prefixes: list[AffixInfo] = []
        self.suffixes: list[AffixInfo] = []
        self.is_corrupted: bool = False

        logging.debug(f"Normalized item description: {self.description}")

        item_base_match = ITEM_BASE_REGEX.search(self.description)
        if item_base_match:
            if item_base_match.group("class") == CraftingTarget.MAPS:
                self.item_class = CraftingTarget.MAPS
            self.rarity = ItemRarity(item_base_match.group("rarity"))
            # TODO: This doesn't actually work, not sure why but the group is None 
            if item_base_match.group("corrupted"):
                self.is_corrupted = True

        matches = AFFIX_REGEX.finditer(self.description)
        for match in matches:
            affix_type = match.group("affix_type")
            affix_name = match.group("affix_name")
            affix_tier = match.group("tier")
            affix_desc = match.group("description").replace("\n", " / ")

            self.add_affix(type=affix_type, name=affix_name, tier=affix_tier, description=affix_desc)
        pass

    def add_affix(self, type: str, name: str, tier: str, description: str) -> None:
        if type.lower() == "prefix":
            self.prefixes.append(AffixInfo(type=type, name=name, tier=tier, description=description))
        else:
            self.suffixes.append(AffixInfo(type=type, name=name, tier=tier, description=description))
        pass

    def get_affix_logs(self, dump_all: bool = False) -> list[str]:
        if dump_all:
            return ["Item description:\n", self.description]
        
        logs: list[str] = ["Found item affixes:\n"]

        for affix in [*self.prefixes, *self.suffixes]:
            logs.append(f"\t{affix.type} | {affix.name} | {affix.tier} | {affix.description}\n")
        return logs

    def match(self, regex: re.Pattern, is_regex_inverted: bool = False) -> bool:
        if (self.rarity == ItemRarity.NORMAL):
            return False

        match = regex.search(self.description)
        if (match):
            return not is_regex_inverted

        return is_regex_inverted
    
    def is_affixes_full(self) -> bool:
        affix_count = len(self.prefixes) + len(self.suffixes)
        match self.rarity:
            case ItemRarity.MAGIC:
                return affix_count >= 2
            case ItemRarity.RARE:
                return affix_count >= 6
            case _:
                return True
