import logging
import configparser

def setup_logging(config_file='config.ini'):
    """
    Setup logging configuration based on the configuration file.
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    
    log_file = config['logging']['log_file']
    log_level = config['logging'].get('log_level', 'INFO').upper()

    logging.basicConfig(
        filename=log_file,
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
