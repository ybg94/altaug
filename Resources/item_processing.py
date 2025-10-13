from collections import namedtuple
from enum import StrEnum, auto
import logging
import re
from . import autogui

class ItemRarity(StrEnum):
    NONE = auto()
    NORMAL = 'Normal'
    MAGIC = 'Magic'
    RARE = 'Rare'
    UNIQUE = 'Unique'

RARITY_REGEX = re.compile(r"^Rarity:\s(?P<rarity>\w*)$", re.MULTILINE)
AFFIX_REGEX = re.compile(
    r"^{ (?:Master Crafted )?(?P<affix_type>Prefix|Suffix) Modifier \"(?P<affix_name>[\w\s'-]*)\" (?:\((?P<tier>(?:Rank|Tier): \d*)\))?[^(?:\r\n|\n|\r)]*$(?:\r\n|\n|\r)(?P<description>[^{]*)(?={?)",
    re.MULTILINE
)

AffixInfo = namedtuple('AffixInfo', ['type', 'name', 'tier', 'description'])
class ItemInfo:
    def __init__(self, advanced_description: str | None = None):
        if not advanced_description:
            advanced_description = autogui.get_item_advanced_description()

        self.description = advanced_description.replace('\r\n', '\n').replace('\r', '\n')
        self.rarity: ItemRarity = ItemRarity.NONE
        self.prefixes: list[AffixInfo] = []
        self.suffixes: list[AffixInfo] = []

        logging.debug(f"Normalized item description: {self.description}")

        rarity_match = RARITY_REGEX.search(self.description)
        if rarity_match:
            self.rarity = ItemRarity(rarity_match.group("rarity"))

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

    def get_logs(self) -> list[str]:
        logs: list[str] = ["Found item affixes:\n"]

        for affix in [*self.prefixes, *self.suffixes]:
            logs.append(f"\t{affix.type} | {affix.name} | {affix.tier} | {affix.description}\n")
        return logs

    def match(self, regex: re.Pattern) -> bool:
        match = regex.search(self.description)
        if (match):
            return True

        return False
    
    def is_affixes_full(self) -> bool:
        affix_count = len(self.prefixes) + len(self.suffixes)
        match self.rarity:
            case ItemRarity.MAGIC:
                return affix_count >= 2
            case ItemRarity.RARE:
                return affix_count >= 6
            case _:
                return True
