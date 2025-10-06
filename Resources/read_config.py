import configparser
import os

def read_config():
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
        print(f"Error: Config file not found at {config_file_path}")
        return None  
    except configparser.NoSectionError as e:
        print(f"Error: Missing section in config file: {e}")
        return None
    except configparser.NoOptionError as e:
        print(f"Error: Missing option in config file: {e}")
        return None
    except ValueError as e:
        print(f"Error: Could not convert value to float: {e}") 
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None