# -*- coding: utf-8 -*-
import configparser
import os.path

config = configparser.ConfigParser()

if os.path.exists("configuration.ini"):
    config.read("configuration.ini")
else:
    from uuid import uuid4

    config["ADDRESS"] = {"host": "localhost",
                         "port": "5000"}
    config["PARAMS"] = {"key": uuid4(),
                        "database": "../db/maindatabase.db",
                        "debug": "false"}

    with open(file="configuration.ini", mode="w", encoding="utf-8") as configfile:
        config.write(configfile)

debug: bool = config.getboolean("PARAMS", "debug")
host: str = config.get("ADDRESS", "host")
port: int = config.getint("ADDRESS", "port")
SECRET_KEY: str = config.get("PARAMS", "key")
DATABASE_PATH: str = config.get("PARAMS", "database")
DATABASE_URL = f"sqlite:///{DATABASE_PATH.strip()}?check_same_thread=False"
