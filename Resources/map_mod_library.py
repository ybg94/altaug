from dataclasses import dataclass
import csv
import os
import re

MAP_MODS_FILE = 'poe_map_mods_to_avoid.csv'

# Strips the "[InternalName|Display Name]" markup the source data uses for keywords
KEYWORD_MARKUP_REGEX = re.compile(r"\[(?:[^\]|]*\|)?([^\]]*)\]")

@dataclass(frozen=True)
class MapMod:
    modifier: str
    affix: str
    nightmare_only: bool
    danger_score: int
    regex: str

    @property
    def display_text(self) -> str:
        return KEYWORD_MARKUP_REGEX.sub(r"\1", self.modifier).replace("|", " / ")

def read() -> list[MapMod]:
    file_path = os.path.join('src', MAP_MODS_FILE)
    with open(file_path, mode='r', encoding='utf-8', newline='') as file:
        mods = [
            MapMod(
                modifier=row['modifier'],
                affix=row['affix'].capitalize(),
                nightmare_only=row['nightmare_only'].strip().lower() == 'true',
                danger_score=int(row['danger_score']),
                regex=row['regex'],
            )
            for row in csv.DictReader(file)
        ]
        pass

    return sorted(mods, key=lambda mod: mod.danger_score, reverse=True)
