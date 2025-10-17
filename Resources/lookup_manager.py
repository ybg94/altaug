from typing import TypeAlias, Dict
import os
import yaml

REGEX_LOOKUP_FILE = 'regex_store.yaml'
RegexLookup: TypeAlias = Dict[str, Dict[str, Dict[str, str]]]

DEFAULT_REGEX_LOOKUP: RegexLookup = {
    'Armour': {
        "Lich's Circlet": {
            'T1 ES/Int': "^Blazing|^Unassailable|^Seraphim's|of the Polymath$"
        },
        'Warlock Boots': {
            'T1 ES/MS/Int': "^Seething|^Unassailable|^Cheetah's|^Hellion's|of the Genius$"
        }
    },
    'Map': {
        'Tier 16': {
            'No ele/leech/regen': '!efl|old$|gen|r at|o al'
        },
        'Tier 17': {
            'No reflect/crit/-max': '!o al|ra c|wak|r li|f ph|lier'
        }
    },
    'Jewelry': {
        'Amulet': {
            '+1 Skill': "^Exalter's"
        }
    },
    'Weapon': {
        'Spine Bow': {
            'PH': 'Placeholder'
        }
    }
}

def read() -> RegexLookup:
    file_path = os.path.join('src', REGEX_LOOKUP_FILE)
    with open(file_path, mode='r', encoding='utf-8') as file:
        lookup: RegexLookup = yaml.safe_load(stream=file)
        pass
    
    return lookup

def update(lookup: RegexLookup) -> None:
    file_path = os.path.join('src', REGEX_LOOKUP_FILE)
    with open(file_path, mode='w', encoding='utf-8') as file:
        yaml.safe_dump(data=lookup, stream=file, encoding='utf-8', sort_keys=False)
        pass
