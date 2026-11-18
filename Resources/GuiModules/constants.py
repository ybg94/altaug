from enum import StrEnum

class CraftingTarget(StrEnum):
    GEAR = 'Gear'
    MAPS = 'Maps'

CRAFTING_TARGETS: list[str] = [CraftingTarget.GEAR, CraftingTarget.MAPS]

class AffixMode(StrEnum):
    ANY = 'Any'
    PREFIX = 'Prefix'
    SUFFIX = 'Suffix'

AFFIX_MODES: list[str] = [AffixMode.ANY, AffixMode.PREFIX, AffixMode.SUFFIX]

class MapStat(StrEnum):
    """Value is the stat's line label in the copied map description."""
    QUANTITY = 'Item Quantity'
    PACK_SIZE = 'Monster Pack Size'
    MORE_MAPS = 'More Maps'
    MORE_CURRENCY = 'More Currency'
    MORE_SCARABS = 'More Scarabs'

MAP_STAT_LABELS: dict[MapStat, str] = {
    MapStat.QUANTITY: 'Quantity',
    MapStat.PACK_SIZE: 'Pack Size',
    MapStat.MORE_MAPS: 'More Maps',
    MapStat.MORE_CURRENCY: 'More Currency',
    MapStat.MORE_SCARABS: 'More Scarabs',
}

class MapModifier(StrEnum):
    """Value is the modifier line as it appears in the copied map description."""
    EVOCATOR_KTASH = "Area contains an Evocator of K'Tash"
    EVOCATOR_BEIDAT = "Area contains an Evocator of Beidat"
    EVOCATOR_GHORR = "Area contains an Evocator of Ghorr"
    PANDEMONIUM_SENTINEL = "Area contains a buried Pandemonium Sentinel"
    STALKER_SENTINEL = "Area contains a buried Stalker Sentinel"
    APEX_SENTINEL = "Area contains a buried Apex Sentinel"
    MIRROR_OF_DELIRIUM = "Area contains a Mirror of Delirium"
    MIRAGE = "Area contains a Mirage"
    VIRIDIAN_WILDWOOD = "Area contains the Viridian Wildwood"

MAP_MODIFIER_LABELS: dict[MapModifier, str] = {
    MapModifier.EVOCATOR_KTASH: "Evocator of K'Tash",
    MapModifier.EVOCATOR_BEIDAT: 'Evocator of Beidat',
    MapModifier.EVOCATOR_GHORR: 'Evocator of Ghorr',
    MapModifier.PANDEMONIUM_SENTINEL: 'Pandemonium Sentinel',
    MapModifier.STALKER_SENTINEL: 'Stalker Sentinel',
    MapModifier.APEX_SENTINEL: 'Apex Sentinel',
    MapModifier.MIRROR_OF_DELIRIUM: 'Mirror of Delirium',
    MapModifier.MIRAGE: 'Mirage',
    MapModifier.VIRIDIAN_WILDWOOD: 'Viridian Wildwood',
}

HINT_TEXT_COLOR = (150, 150, 150)
