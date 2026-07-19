
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("Weather-CLI.log"),
        logging.StreamHandler()  # keeps console output too
    ]
)
logger = logging.getLogger(__name__)