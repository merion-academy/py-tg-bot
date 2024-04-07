import os
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

# BOT_TOKEN = os.getenv("BOT_TOKEN")
# BOT_TOKEN = config.get("bot", "token", fallback=os.getenv("BOT_TOKEN"))
BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    config.get("bot", "token", fallback=None),
)
if not BOT_TOKEN:
    exit("Please provide BOT_TOKEN env variable")

DOGS_PIC_URL = "https://masterpiecer-images.s3.yandex.net/9586e0deb07711ee8f9e5e02d8de8a56:upscaled"
DOG_PIC_FILE_ID = "AgACAgQAAxkDAAPtZfiuhOe_NegUBDkWg8Vk1dncUGgAAs7DMRuMXMhTm_qnL1YeP78BAAMCAAN5AAM0BA"

CAT_PIC_URL = "https://png.pngtree.com/png-clipart/20230511/ourmid/pngtree-isolated-cat-on-white-background-png-image_7094927.png"


def get_admin_ids():
    admin_ids = config.get("admin", "admin_ids", fallback="")
    admin_ids = [admin_id.strip() for admin_id in admin_ids.split(",")]
    admin_ids = [
        int(admin_id)
        for admin_id in admin_ids
        if admin_id
    ]
    return admin_ids


BOT_ADMIN_USER_IDS = get_admin_ids()
