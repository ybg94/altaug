from dataclasses import asdict, dataclass
import logging
import os
import yaml
from .GuiModules.constants import CraftingTarget

FAVORITES_PATH = os.path.join('src', 'regex_favorites.yaml')

@dataclass
class RegexFavorite:
    name: str
    target: CraftingTarget
    regex: str

def read() -> list[RegexFavorite]:
    if not os.path.isfile(FAVORITES_PATH):
        return []

    try:
        with open(FAVORITES_PATH, mode='r', encoding='utf-8') as file:
            entries = yaml.safe_load(file) or []

        return [
            RegexFavorite(name=str(entry['name']), target=CraftingTarget(entry['target']), regex=str(entry['regex']))
            for entry in entries
        ]
    except Exception:
        logging.error('Unable to read RegEx favorites, starting with an empty list.', exc_info=True)
        return []

def save(favorites: list[RegexFavorite]) -> None:
    entries = [asdict(favorite) | {'target': str(favorite.target)} for favorite in favorites]
    with open(FAVORITES_PATH, mode='w', encoding='utf-8') as file:
        yaml.safe_dump(data=entries, stream=file, allow_unicode=True, sort_keys=False)
    pass
