from enum import StrEnum
from typing import LiteralString
import os
import pyautogui
import yaml
from . import decorators
from .GuiModules.constants import CraftingTarget

def __point_representer(dumper: yaml.SafeDumper, data: pyautogui.Point) -> yaml.MappingNode:
    return dumper.represent_mapping(u'!Point', data._asdict())

def __point_constructor(loader: yaml.SafeLoader, node: yaml.MappingNode) -> pyautogui.Point:
    values = loader.construct_mapping(node)
    return pyautogui.Point(**values)

yaml.SafeDumper.add_representer(pyautogui.Point, __point_representer)
yaml.SafeDumper.add_multi_representer(StrEnum, yaml.representer.SafeRepresenter.represent_str)
yaml.SafeLoader.add_constructor(u'!Point', __point_constructor)

class ConfigurationCoordinates(yaml.YAMLObject):
    yaml_dumper = yaml.SafeDumper
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Coordinates'

    def __init__(self,
                 item: pyautogui.Point,
                 map_top_left: pyautogui.Point,
                 map_bottom_right: pyautogui.Point,
                 alt: pyautogui.Point,
                 aug: pyautogui.Point,
                 alch: pyautogui.Point,
                 scour: pyautogui.Point,
                 chaos: pyautogui.Point) -> None:
        self.item: pyautogui.Point = item
        self.map_top_left: pyautogui.Point = map_top_left
        self.map_bottom_right: pyautogui.Point = map_bottom_right
        self.alt: pyautogui.Point = alt
        self.aug: pyautogui.Point = aug
        self.alch: pyautogui.Point = alch
        self.scour: pyautogui.Point = scour
        self.chaos: pyautogui.Point = chaos
        super().__init__()

class ConfigurationAppSettings(yaml.YAMLObject):
    yaml_dumper = yaml.SafeDumper
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!AppSettings'

    def __init__(self, pyautogui_pause: float, enable_performance_logging: bool) -> None:
        self.pyautogui_pause: float = pyautogui_pause
        self.enable_performance_logging: bool = enable_performance_logging
        super().__init__()

class ConfigurationLastState(yaml.YAMLObject):
    yaml_dumper = yaml.SafeDumper
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!LastState'

    def __init__(self, crafting_target: CraftingTarget, map_craft_amount: int, is_t17: bool, regex_string: str, crafting_attempts: int) -> None:
        self.crafting_target: CraftingTarget = crafting_target
        self.map_craft_amount: int = map_craft_amount
        self.is_t17: bool = is_t17
        self.regex_string: str = regex_string
        self.crafting_attempts: int = crafting_attempts
        super().__init__()

class Configuration(yaml.YAMLObject):
    yaml_dumper = yaml.SafeDumper
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Config'

    def __init__(self, coordinates: ConfigurationCoordinates, app_settings: ConfigurationAppSettings, last_state: ConfigurationLastState) -> None:
        self.coordinates: ConfigurationCoordinates = coordinates
        self.app_settings: ConfigurationAppSettings = app_settings
        self.last_state: ConfigurationLastState = last_state
        super().__init__()

@decorators.singleton
class ConfigManager:
    CONFIG_PATH: LiteralString = os.path.join('src', 'config.yaml')
    DEFAULT_CONFIG: Configuration = Configuration(
        ConfigurationCoordinates(pyautogui.Point(0, 0), pyautogui.Point(0, 0), pyautogui.Point(0, 0), pyautogui.Point(0, 0), pyautogui.Point(0, 0), pyautogui.Point(0, 0), pyautogui.Point(0, 0), pyautogui.Point(0, 0)),
        ConfigurationAppSettings(0.03, False),
        ConfigurationLastState(CraftingTarget.GEAR, 15, False, "", 10))

    def __init__(self) -> None:
        if not os.path.isfile(self.CONFIG_PATH):
            self.save_config(self.DEFAULT_CONFIG)

        self._cfg = self.__parse_config()

    def __parse_config(self) -> Configuration:
        with open(self.CONFIG_PATH, mode='r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def save_config(self, new_config: Configuration) -> None:
        with open(self.CONFIG_PATH, mode='w', encoding='utf-8') as file:
            yaml.safe_dump(data=new_config, stream=file, encoding='utf-8', sort_keys=False)

        self.cfg = new_config
        pass

    @property
    def cfg(self) -> Configuration:
        return self._cfg
    
    @cfg.setter
    def cfg(self, value: Configuration) -> None:
        self._cfg = value
        pass

manager = ConfigManager()
