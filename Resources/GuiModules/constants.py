CRAFTING_TARGETS: list[str] = ["Gear", "Maps"]

ITEM_TYPES = ["Armour", "Weapon", "Map"]
ITEM_BASES_LOOKUP: dict[str, list[str]] = {
    "Armour": ["Warlock Boots", "Lich's Circlet"],
    "Weapon": ["Spine Bow"],
    "Map": ["Tier 17", "Tier 16"],
}
REGEX_PRESETS_LOOKUP: dict[str, list[str]] = {
    "Warlock Boots": ["One", "Two"],
    "Lich's Circlet": ["Three"],
    "Spine Bow": ["Four"],
    "Tier 17": ["Five", "Six"],
    "Tier 16": ["Seven"],
}
REGEX_LOOKUP: dict[str, str] = {
    "One": "1st regex",
    "Two": "2nd regex",
    "Three": "3rd regex",
    "Four": "4th regex",
    "Five": "5th regex",
    "Six": "6th regex",
    "Seven": "7th regex",
}
CRAFTING_TARGET_LOOKUP: dict[str, str] = {
    "Armour": CRAFTING_TARGETS[0],
    "Weapon": CRAFTING_TARGETS[0],
    "Map": CRAFTING_TARGETS[1],
}

ITEM_TYPE_COMBO_DEFAULT = "Select item type..."
ITEM_BASE_COMBO_DEFAULT = "Select item base..."
REGEX_COMBO_DEFAULT = "Select RegEx preset..."
