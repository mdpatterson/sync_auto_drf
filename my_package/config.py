import os
import json
import sys
import logging

def load_config():
    config_path = os.path.join(os.getcwd(), "config.json")
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            logging.info(f"Configuration loaded from {config_path}")
            return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from configuration file: {config_path}")
        sys.exit(1)
