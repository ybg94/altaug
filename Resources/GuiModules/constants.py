item_base_combo_items: dict[str, list[str]] = {
    "Armour": ["Warlock Boots", "Lich's Circlet"],
    "Weapon": ["Spine Bow"],
    "Map": ["Tier 17", "Tier 16"],
}
regex_combo_items: dict[str, list[str]] = {
    "Warlock Boots": ["One", "Two"],
    "Lich's Circlet": ["Three"],
    "Spine Bow": ["Four"],
    "Tier 17": ["Five", "Six"],
    "Tier 16": ["Seven"],
}

ITEM_TYPE_COMBO_DEFAULT = "Select item type..."
ITEM_BASE_COMBO_DEFAULT = "Select item base..."
REGEX_COMBO_DEFAULT = "Select RegEx preset..."