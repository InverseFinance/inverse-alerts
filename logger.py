import logging
import sys

# Logger config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
# Mute warning when pool is full
logging.getLogger("urllib3").setLevel(logging.ERROR)