#!/usr/bin/env python3
"""
config_loader.py

This module loads configuration data for LLMCoder. On startup it does the following:
  - If a JSON configuration file (config.json) exists, load and return it.
  - Otherwise, load the configuration from the .env file (using python-dotenv),
    write it to config.json (with proper formatting) and delete the original .env file.
  - The returned configuration is a Python dictionary.

Usage (in any service/module):
    from config_loader import load_config
    config = load_config()
    # Now access config['OPENAI_API_KEY'], config['PLAID_SECRET'], etc.
"""

import json
import logging
import sys
from pathlib import Path

from dotenv import dotenv_values

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define filenames
CONFIG_JSON_FILE = "config.json"
ENV_FILE = ".env"


def load_config() -> dict:
    """
    Loads the configuration from config.json if it exists; otherwise, converts the .env file into JSON.
    Returns:
        A dictionary containing the configuration key–value pairs.
    Exits the process with an error message if neither file is available or if a conversion fails.
    """
    env_path = Path(ENV_FILE)
    config_json_path = Path(CONFIG_JSON_FILE)

    # If JSON config already exists, load and return it.
    if config_json_path.exists():
        try:
            with config_json_path.open("r", encoding="utf-8") as f:
                config = json.load(f)
            logging.info(f"Loaded configuration from {CONFIG_JSON_FILE}")
            return config
        except Exception as e:
            logging.error(f"Failed to load {CONFIG_JSON_FILE}: {e}")
            sys.exit(1)
    # Otherwise, if the .env file exists, convert it.
    elif env_path.exists():
        try:
            config = dotenv_values(ENV_FILE)
            if not config:
                logging.error(f"No valid configuration found in {ENV_FILE}")
                sys.exit(1)
            # Write out as JSON
            with config_json_path.open("w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            logging.info(f"Converted {ENV_FILE} to {CONFIG_JSON_FILE}")
            # Delete the .env file after successful conversion
            env_path.unlink()
            logging.info(f"Deleted original {ENV_FILE} file")
            return config
        except Exception as e:
            logging.error(f"Failed to convert {ENV_FILE} to JSON: {e}")
            sys.exit(1)
    else:
        logging.error("No configuration file found. Expected .env or config.json.")
        sys.exit(1)


if __name__ == "__main__":
    # For testing: print the configuration
    configuration = load_config()
    print("Configuration loaded successfully:")
    print(json.dumps(configuration, indent=4))
