from typing import LiteralString
import os
import yaml
from . import decorators

class ConfigurationCoordinates(yaml.YAMLObject):
    yaml_dumper = yaml.SafeDumper
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Coordinates'

    def __init__(self, item_x, item_y, map_top_left_x, map_top_left_y, map_bottom_right_x, map_bottom_right_y, alt_x, alt_y, aug_x, aug_y, alch_x, alch_y, scour_x, scour_y, chaos_x, chaos_y) -> None:
        self.item_x: float = item_x
        self.item_y: float = item_y
        self.map_top_left_x: float = map_top_left_x,
        self.map_top_left_y: float = map_top_left_y,
        self.map_bottom_right_x: float = map_bottom_right_x,
        self.map_bottom_right_y: float = map_bottom_right_y,
        self.alt_x: float = alt_x
        self.alt_y: float = alt_y
        self.aug_x: float = aug_x
        self.aug_y: float = aug_y
        self.alch_x: float = alch_x
        self.alch_y: float = alch_y
        self.scour_x: float = scour_x
        self.scour_y: float = scour_y
        self.chaos_x: float = chaos_x
        self.chaos_y: float = chaos_y
        super().__init__()

class ConfigurationAppSettings(yaml.YAMLObject):
    yaml_dumper = yaml.SafeDumper
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!AppSettings'

    def __init__(self, pyautogui_pause: float, enable_pyautogui_failsafe: bool, enable_performance_logging: bool) -> None:
        self.pyautogui_pause: float = pyautogui_pause
        self.enable_pyautogui_failsafe: bool = enable_pyautogui_failsafe
        self.enable_performance_logging: bool = enable_performance_logging
        super().__init__()

class ConfigurationLastState(yaml.YAMLObject):
    yaml_dumper = yaml.SafeDumper
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!LastState'

    def __init__(self, crafting_target: str, regex_string: str, crafting_attempts: int) -> None:
        self.crafting_target: str = crafting_target
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

    def __init__(self) -> None:
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
