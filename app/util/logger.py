import logging


def set_logger(_logger, level: int = logging.INFO):
    formatter = logging.Formatter("%(asctime)s %(name)10s %(levelname)8s %(process)6d %(thread)11d --- %(filename)-22s : %(message)s")
    handler = logging.StreamHandler()

    handler.setLevel(level)
    handler.setFormatter(formatter)
    _logger.addHandler(handler)


logger = logging.getLogger("MRT")
logger.setLevel(logging.INFO)
set_logger(logger)

