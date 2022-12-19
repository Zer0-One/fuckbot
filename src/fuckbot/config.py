import configparser
import logging
import os
import sys

class Config:
    __CONFIG_ENV="FUCKBOT_CONFIG"
    __CONFIG_DEFAULT_PATH="/etc/fuckbot/fuckbot.ini"

    DEFAULT_CONFIG = {
        "ADMIN": -1,
        "AUTOMOD_DB": "automod.json",
        "API_KEY_PATH": "/etc/fuckbot/api.key",
        "BLACKLIST_DB": "blacklist.json",
        "DEBUG": False,
        "FEED_DB": "feed.json",
        "LOGFILE": False,
        "SQLITE_DB": "fuckbot.db",
        "SYSLOG": False,
        "TRIGGER_DB": "trigger.json",
        "WORKING_DIR": "/var/lib/fuckbot",
    }

    config = {}

    def __getitem__(self, key):
        return Config.config.get(key)

    def __setitem__(self, key, value):
        Config.config[key] = value

    def items(self):
        return Config.config.items()

    @classmethod
    def config_init(cls, path=""):
        config = configparser.ConfigParser()

        # The user supplied a config path, but it's invalid
        if path and not os.path.isfile(path):
            logging.error("Configuration file " + path + " does not exist or is not a file")
            sys.exit(-1)

        # If the user didn't give us a path, use the default
        if not path:
            path = cls.__CONFIG_DEFAULT_PATH
            logging.warning("No configuration file path supplied, attempting to load config at " + path)

        # If the path (whether user-supplied or default) isn't valid, use the default config
        if not os.path.isfile(path):
            logging.warning("No configuration file present at " + path)
            logging.warning("Loading default config")
            
            # Instantiate empty config
            config = {"fuckbot": {}}
        else:
            try:
                config.read(path)
                if not "fuckbot" in config:
                    raise Exception("Missing 'fuckbot' section in configuration")
            except Exception as e:
                logging.error("Unable to parse fuckbot configuration file: " + str(e))
                sys.exit(-1)

        # Set config from env, config file, and defaults, in that order of precedence
        for key in cls.DEFAULT_CONFIG:
            if os.environ.get(key):
                cls.config[key.upper()] = os.environ.get(key)
            elif key in config["fuckbot"]:
                cls.config[key.upper()] = config["fuckbot"][key]
            else:
                cls.config[key.upper()] = cls.DEFAULT_CONFIG[key]

        # Load API key
        apikey_path = cls.config["API_KEY_PATH"]
        if not os.path.isfile(apikey_path):
            logging.warning("No API key present at " + apikey_path)
            sys.exit(-1)

        with open(apikey_path, "r") as apikey:
            cls.config["API_KEY"] = apikey.readline()

        # Convert config values into proper python representations
        for key,val in cls.config.items():
            if isinstance(val, str):
                if val.lower() == "on" or val.lower() == "true" or val.lower() == "yes":
                    cls.config[key] = True
                elif val.lower() == "off" or val.lower() == "false" or val.lower() == "no":
                    cls.config[key] = False

                # Admin ID should be an integer
                if key.upper() == "ADMIN":
                    cls.config[key] = int(val)
