#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project: danmy-scrape
@File: main.py
@IDE: PyCharm
@Author: paidaxing
@Date: 2024/6/16 15:37
"""
import logging
import colorlog

log_color_config = {
    "DEBUG": "white",
    "INFO": "cyan",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}
console_handler = colorlog.StreamHandler()
consle_formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors=log_color_config
)
console_handler.setFormatter(consle_formatter)
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info("开始爱奇艺弹幕提取".center(80, '='))
    url = input("视频链接：")

