# -*- coding: utf-8 -*
"""Logger 設定."""


def getLogger(logname):
    """Logger を生成します."""
    from os import path
    from sys import stderr
    from logging import (
        getLogger, FileHandler, Formatter, DEBUG
    )

    from rainbow_logging_handler import RainbowLoggingHandler

    from config import PROJECT_ROOT

    logfile = path.join(PROJECT_ROOT, 'log', logname + '.log')
    if not path.exists(logfile):
        from pathlib import Path
        Path(logfile).touch()
    formatter = Formatter('%(asctime)s:%(levelname)s:%(message)s')
    logger = getLogger(logname)
    logger.setLevel(DEBUG)
    handlers = [FileHandler(logfile), RainbowLoggingHandler(stderr)]
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
