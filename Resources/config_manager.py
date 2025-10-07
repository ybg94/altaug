import configparser
import os

def update_config(items: list[tuple[str, str, str]]) -> None:
    print(f"Updating config with: {items}")

    config = configparser.ConfigParser()
    config_path = os.path.join('src', 'config.ini')

    try:
        config.read(config_path)
        for section, option, value in items:
            config.set(section, option, value)

        with open(config_path, 'w+') as config_file:
            config.write(config_file)

    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}")
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