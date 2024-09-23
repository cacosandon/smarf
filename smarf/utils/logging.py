import logging
import sys


def setup_logging():
    class GreenFormatter(logging.Formatter):
        GREEN = "\033[32m"
        RESET = "\033[0m"

        def format(self, record):
            message = super().format(record)

            return f"{self.GREEN}{message}{self.RESET}"

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        GreenFormatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="[%X]")
    )

    logging.basicConfig(
        level="INFO",
        handlers=[handler],
    )

    logger = logging.getLogger(__name__)

    return logger


log = setup_logging()
