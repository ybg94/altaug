from collections import namedtuple
from enum import StrEnum, auto
import logging
import re
from .GuiModules.constants import CraftingTarget, MapModifier, MapStat

class ItemRarity(StrEnum):
    NONE = auto()
    NORMAL = 'Normal'
    MAGIC = 'Magic'
    RARE = 'Rare'
    UNIQUE = 'Unique'

ITEM_BASE_REGEX = re.compile(r"^Item Class: (?P<class>[\w ]*)$\s*^Rarity:\s(?P<rarity>\w*)$.*^(?P<corrupted>Corrupted)?$", re.MULTILINE | re.DOTALL)
AFFIX_REGEX = re.compile(
    r"^{ (?:Master Crafted )?(?P<affix_type>Prefix|Suffix) Modifier \"(?P<affix_name>[^\"]+)\" (?:\((?P<tier>(?:Rank|Tier): \d+)\))?.*$\n(?P<description>.+?)(?=\n{|$)",
    re.MULTILINE
)
MAP_STAT_REGEX = re.compile(
    r"^(?P<stat>" + "|".join(re.escape(stat) for stat in MapStat) + r"): \+(?P<value>\d+)%",
    re.MULTILINE
)
# The game may use a typographic apostrophe (e.g. K'Tash), accept both
MAP_MODIFIER_REGEXES: dict[MapModifier, re.Pattern] = {
    modifier: re.compile(re.escape(modifier).replace("'", "['’]"), re.IGNORECASE)
    for modifier in MapModifier
}

AffixInfo = namedtuple('AffixInfo', ['type', 'name', 'tier', 'description'])
class ItemInfo:
    def __init__(self, advanced_description: str):
        self.description = advanced_description.replace('\r\n', '\n').replace('\r', '\n')
        self.item_class: CraftingTarget = CraftingTarget.GEAR
        self.rarity: ItemRarity = ItemRarity.NONE
        self.prefixes: list[AffixInfo] = []
        self.suffixes: list[AffixInfo] = []
        self.is_corrupted: bool = False
        self.map_stats: dict[MapStat, int] = {}
        self.map_modifiers: set[MapModifier] = set()

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

        for match in MAP_STAT_REGEX.finditer(self.description):
            self.map_stats[MapStat(match.group("stat"))] = int(match.group("value"))

        self.map_modifiers = {modifier for modifier, regex in MAP_MODIFIER_REGEXES.items() if regex.search(self.description)}
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
    
    def meets_map_stats(self, minimum_stats: dict[MapStat, int]) -> bool:
        # Stats missing from the description are treated as 0%
        return all(self.map_stats.get(stat, 0) >= minimum for stat, minimum in minimum_stats.items())

    def meets_map_modifiers(self, wanted_modifiers: set[MapModifier]) -> bool:
        # Any one of the wanted modifiers is enough, no filter when none are wanted
        return not wanted_modifiers or not self.map_modifiers.isdisjoint(wanted_modifiers)

    def is_affixes_full(self) -> bool:
        affix_count = len(self.prefixes) + len(self.suffixes)
        match self.rarity:
            case ItemRarity.MAGIC:
                return affix_count >= 2
            case ItemRarity.RARE:
                return affix_count >= 6
            case _:
                return True
