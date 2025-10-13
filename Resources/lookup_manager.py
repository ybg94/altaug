import yaml
import os
from typing import TypeAlias, Dict

REGEX_LOOKUP_FILE = 'regex_store.yaml'
RegexLookup: TypeAlias = Dict[str, Dict[str, Dict[str, str]]]

MASER_LOOKUP: RegexLookup = {
    "Armour": {
        "Warlock Boots": {
            "Regex title One": "Regex string 1",
            "Regex title Two": "Regex string 2",
        },
        "Lich's Circlet": {
            "Regex title Three": "Regex string 3",
        },
    },
    "Weapon": {
        "Spine Bow": {
            "Regex title Four": "Regex string 4",
        },
    },
    "Map": {
        "Tier 17": {
            "Regex title Five": "Regex string 5",
            "Regex title Six": "Regex string 6",
        },
        "Tier 16": {
            "Regex title Seven": "Regex string 7",
        },
    },
}

def read() -> RegexLookup:
    file_path = os.path.join('src', REGEX_LOOKUP_FILE)
    with open(file_path, mode='r', encoding='utf-8') as file:
        lookup: RegexLookup = yaml.safe_load(stream=file)
        pass
    
    return lookup

def update(lookup: RegexLookup = MASER_LOOKUP) -> None:
    file_path = os.path.join('src', REGEX_LOOKUP_FILE)
    with open(file_path, mode='w', encoding='utf-8') as file:
        yaml.safe_dump(data=lookup, stream=file, encoding='utf-8', sort_keys=False)
        pass
