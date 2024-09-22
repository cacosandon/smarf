import logging

from rich.console import Console
from rich.logging import RichHandler

console = Console(force_terminal=True)


def setup_logging():
    handler = RichHandler(console=console, rich_tracebacks=True)
    handler.setFormatter(logging.Formatter("%(message)s"))

    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[handler],
    )

    logger = logging.getLogger("rich")

    return logger


log = setup_logging()
