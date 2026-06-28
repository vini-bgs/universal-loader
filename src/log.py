from loguru import logger
from sys import stderr

logger.remove()  # remove o handler padrão do loguru

logger.add(
    sink=stderr, format="{time} <r>{level}</r> <g>{message}</g> {file}", level="INFO"
)

logger.add(
    sink="logs/universal_loader.log",
    format="{time} {level} {message} {file}",
    level="INFO",
)
