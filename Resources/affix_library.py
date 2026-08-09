from typing import TypeAlias, Dict
import os
import yaml

AFFIX_LIBRARY_FILE = 'affix_library.yaml'
AffixLibrary: TypeAlias = Dict[str, Dict[str, Dict[str, list[str]]]]

def read() -> AffixLibrary:
    file_path = os.path.join('src', AFFIX_LIBRARY_FILE)
    with open(file_path, mode='r', encoding='utf-8') as file:
        library: AffixLibrary = yaml.safe_load(stream=file)
        pass

    return library
