from enum import StrEnum

class CraftingTarget(StrEnum):
    GEAR = 'Gear'
    MAPS = 'Maps'

CRAFTING_TARGETS: list[str] = [CraftingTarget.GEAR, CraftingTarget.MAPS]

class AffixCategory(StrEnum):
    ITEM = 'Item'
    MAP = 'Map'

AFFIX_CATEGORIES: list[str] = [AffixCategory.ITEM, AffixCategory.MAP]

CATEGORY_TO_CRAFTING_TARGET_LOOKUP: dict[str, str] = {
    AffixCategory.ITEM: CraftingTarget.GEAR,
    AffixCategory.MAP: CraftingTarget.MAPS,
}

NIGHTMARE_MAP_TYPE = "Nightmare"

CATEGORY_COMBO_DEFAULT = "Select category..."
TYPE_COMBO_DEFAULT = "Select item type..."
