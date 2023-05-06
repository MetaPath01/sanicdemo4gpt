import logging
import os
from logging.handlers import TimedRotatingFileHandler


def get_logger():
    logger = logging.getLogger("LOGGER")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "filename": "%(filename)s", "line": "%(lineno)d", "message": "%(message)s"}')

    # 添加控制台输出处理器
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 添加文件输出处理器
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "gptbot.log")
    handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=365)
    handler.suffix = "%Y%m%d"
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


loger = get_logger()
