from enum import StrEnum

class CraftingTarget(StrEnum):
    GEAR = 'Gear'
    MAPS = 'Maps'

CRAFTING_TARGETS: list[str] = [CraftingTarget.GEAR, CraftingTarget.MAPS]

ITEM_TYPE_TO_CRAFTING_TARGET_LOOKUP: dict[str, str] = {
    "Armour": CRAFTING_TARGETS[0],
    "Weapon": CRAFTING_TARGETS[0],
    "Jewelry": CRAFTING_TARGETS[0],
    "Map": CRAFTING_TARGETS[1],
}

ITEM_TYPE_COMBO_DEFAULT = "Select item type..."
ITEM_BASE_COMBO_DEFAULT = "Select item base..."
REGEX_TITLE_COMBO_DEFAULT = "Select RegEx preset..."

EDITOR_ADD_NEW_ITEM = "Add new..."
