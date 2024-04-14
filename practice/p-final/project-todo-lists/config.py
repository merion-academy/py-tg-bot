import os
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    config.get("bot", "token", fallback=None),
)
if not BOT_TOKEN:
    exit("Please provide BOT_TOKEN env variable")
