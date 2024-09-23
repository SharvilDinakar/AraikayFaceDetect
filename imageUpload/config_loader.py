import configparser
import logging

def load_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        if 'azure_storage' not in config:
            raise KeyError("The section 'azure_storage' was not found in the config file.")
        section = config['azure_storage']

        # Check for required keys and handle missing ones
        required_keys = ['connection_string', 'container_name', 'local_folder_path']
        for key in required_keys:
            if key not in section:
                raise KeyError(f"Key '{key}' not found in the 'azure_storage' section.")
        return section

    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        raise

config = load_config()

connection_string = config['connection_string']
container_name = config['container_name']
local_folder_path = config['local_folder_path']
