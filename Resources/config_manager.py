import configparser
import logging
import os

def read_config() -> dict[str, float] | None:
    config = configparser.ConfigParser()
    config_file_path = os.path.join('src', 'config.ini')

    try:
        config.read(config_file_path)

        ITEM_X_COORDINATE_PERCENT = float(config.get('Coordinates', 'item_x'))
        ITEM_Y_COORDINATE_PERCENT = float(config.get('Coordinates', 'item_y'))
        MAP_TOP_LEFT_X_COORDINATE_PERCENT = float(config.get('Coordinates', 'map_top_left_x'))
        MAP_TOP_LEFT_Y_COORDINATE_PERCENT = float(config.get('Coordinates', 'map_top_left_y'))
        MAP_BOTTOM_RIGHT_X_COORDINATE_PERCENT = float(config.get('Coordinates', 'map_bottom_right_x'))
        MAP_BOTTOM_RIGHT_Y_COORDINATE_PERCENT = float(config.get('Coordinates', 'map_bottom_right_y'))
        ALT_X_COORDINATE_PERCENT = float(config.get('Coordinates', 'alt_x'))
        ALT_Y_COORDINATE_PERCENT = float(config.get('Coordinates', 'alt_y'))
        AUG_X_COORDINATE_PERCENT = float(config.get('Coordinates', 'aug_x'))
        AUG_Y_COORDINATE_PERCENT = float(config.get('Coordinates', 'aug_y'))
        ALCH_X_COORDINATE_PERCENT = float(config.get('Coordinates', 'alch_x'))
        ALCH_Y_COORDINATE_PERCENT = float(config.get('Coordinates', 'alch_y'))
        SCOUR_X_COORDINATE_PERCENT = float(config.get('Coordinates', 'scour_x'))
        SCOUR_Y_COORDINATES_PERCENT = float(config.get('Coordinates', 'scour_y'))
        CHAOS_X_COORDINATES_PERCENT = float(config.get('Coordinates', 'chaos_x'))
        CHAOS_Y_COORDINATES_PERCENT = float(config.get('Coordinates', 'chaos_y'))

        CONFIG_VALUES = {
            'item_x_coordinate_percent': ITEM_X_COORDINATE_PERCENT,
            'item_y_coordinate_percent': ITEM_Y_COORDINATE_PERCENT,
            'map_top_left_x_coordinate_percent': MAP_TOP_LEFT_X_COORDINATE_PERCENT,
            'map_top_left_y_coordinate_percent': MAP_TOP_LEFT_Y_COORDINATE_PERCENT,
            'map_bottom_right_x_coordinate_percent': MAP_BOTTOM_RIGHT_X_COORDINATE_PERCENT,
            'map_bottom_right_y_coordinate_percent': MAP_BOTTOM_RIGHT_Y_COORDINATE_PERCENT,
            'alt_x_coordinate_percent': ALT_X_COORDINATE_PERCENT,
            'alt_y_coordinate_percent': ALT_Y_COORDINATE_PERCENT,
            'aug_x_coordinate_percent': AUG_X_COORDINATE_PERCENT,
            'aug_y_coordinate_percent': AUG_Y_COORDINATE_PERCENT,
            'alch_x_coordinate_percent': ALCH_X_COORDINATE_PERCENT,
            'alch_y_coordinate_percent': ALCH_Y_COORDINATE_PERCENT,
            'scour_x_coordinate_percent': SCOUR_X_COORDINATE_PERCENT,
            'scour_y_coordinate_percent': SCOUR_Y_COORDINATES_PERCENT,
            'chaos_x_coordinate_percent': CHAOS_X_COORDINATES_PERCENT,
            'chaos_y_coordinate_percent': CHAOS_Y_COORDINATES_PERCENT
        }

        return CONFIG_VALUES

    except FileNotFoundError:
        logging.error(f"Error: Config file not found at {config_file_path}.", exc_info=True)
        return None  
    except configparser.NoSectionError:
        logging.error(f"Error: Missing section in config file.", exc_info=True)
        return None
    except configparser.NoOptionError:
        logging.error(f"Error: Missing option in config file.", exc_info=True)
        return None
    except ValueError:
        logging.error(f"Error: Could not convert value to float.", exc_info=True) 
        return None
    except Exception:
        logging.error(f"An unexpected error occurred.", exc_info=True)
        return None

def update_config(items: list[tuple[str, str, str]]) -> None:
    logging.info(f"Updating config with: {items}.")

    config = configparser.ConfigParser()
    config_path = os.path.join('src', 'config.ini')

    try:
        config.read(config_path)
        for section, option, value in items:
            config.set(section, option, value)

        with open(config_path, 'w+') as config_file:
            config.write(config_file)

    except FileNotFoundError:
        logging.error(f"Config file not found at {config_path}.", exc_info=True)
        return None
    except configparser.NoSectionError:
        logging.error(f"Missing section in config file.", exc_info=True)
        return None
    except configparser.NoOptionError:
        logging.error(f"Missing option in config file.", exc_info=True)
        return None
    except ValueError:
        logging.error(f"Could not convert value to float.", exc_info=True) 
        return None
    except Exception:
        logging.error(f"An unexpected error occurred.", exc_info=True)
        return None