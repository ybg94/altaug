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
        ALT_X_COORDINATE_PERCENT = float(config.get('Coordinates', 'alt_x'))
        ALT_Y_COORDINATE_PERCENT = float(config.get('Coordinates', 'alt_y'))
        AUG_X_COORDINATE_PERCENT = float(config.get('Coordinates', 'aug_x'))
        AUG_Y_COORDINATE_PERCENT = float(config.get('Coordinates', 'aug_y'))

        CONFIG_VALUES = {
            'item_x_coordinate_percent': ITEM_X_COORDINATE_PERCENT,
            'item_y_coordinate_percent': ITEM_Y_COORDINATE_PERCENT,
            'alt_x_coordinate_percent': ALT_X_COORDINATE_PERCENT,
            'alt_y_coordinate_percent': ALT_Y_COORDINATE_PERCENT,
            'aug_x_coordinate_percent': AUG_X_COORDINATE_PERCENT,
            'aug_y_coordinate_percent': AUG_Y_COORDINATE_PERCENT
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