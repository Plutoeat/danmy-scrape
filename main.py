#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project: danmy-scrape
@File: main.py
@IDE: PyCharm
@Author: paidaxing
@Date: 2024/6/16 15:37
"""
import json
import logging
import os.path
import zlib
from math import ceil
from typing import Dict, Union, Optional

import bs4
import colorlog
import requests

from convert_util import xml2ass

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
logging.basicConfig(level=logging.INFO, handlers=[console_handler])
logger = logging.getLogger(__name__)


def get_html_content(url: str) -> Union[bytes, None]:
    """
    获取网址内容，获取失败返回 None
    :param url: 网址
    :return: 网站二进制内容或者 None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logger.exception(e)
        return None


def get_vid_duration_title(url: str) -> Dict[str, Union[str, int]]:
    """
    解析视频链接，获取弹幕链接必要参数
    :param url: 视频链接
    :return: 页面关键参数
    """
    logger.info(f"[开始解析链接 - {url}]".center(80, '='))
    content = get_html_content(url)
    soup = bs4.BeautifulSoup(content, 'html.parser')
    scripts = soup.findAll('script')
    target_script = list(filter(lambda script: "window.QiyiPlayerProphetData" in script.text, scripts))[0]
    target_dict = json.loads(target_script.text.split("window.QiyiPlayerProphetData=")[1])
    tvid = str(target_dict['tvid'])
    duration = target_dict['a']['data']['showResponse']['videoInfo']['videoDuration']
    tl = target_dict['a']['data']['originRes']['vdi']['tl']
    logger.info(f"已成功获取视频 tvid: {tvid}, duration: {duration}, title: {tl}".center(80, '='))
    return {"tvid": tvid, "duration": duration, "title": tl}


def get_danmu_urls(params: dict) -> tuple[list[str], int]:
    """
    获取弹幕链接
    :param params: 关键参数
    :return: 弹幕链接列表和列表长度
    """
    logger.info(f"正在拼接弹幕链接".center(80, '='))
    # 每 5 分钟一个文件, 向下取整
    pcs = ceil(params['duration'] / 300)
    danmu_url_list = []
    for i in range(1, pcs + 1):
        danmu_url = f"https://cmts.iqiyi.com/bullet/{params['tvid'][-4:-2]}/{params['tvid'][-2:]}/{params['tvid']}_300_{i}.z"
        danmu_url_list.append(danmu_url)
    return danmu_url_list, pcs


def download_danmu(url: str, filename: str, seq: int) -> None:
    """
    下载弹幕文件
    :param url: 弹幕链接
    :param filename: 文件名
    :param seq: 顺序
    :return: None
    """
    logger.info(f"开始下载文件{filename}-{seq}".center(80, '+'))
    res = get_html_content(url)
    # 解码
    decode = zlib.decompress(res).decode('utf-8')
    with open(f'./danmu/{filename}-{seq}.xml', 'a+', encoding='utf-8') as f:
        f.write(decode)


def remove_xml(filename: str, pcs: int) -> None:
    """
    删除 xml 文件
    :param filename: 文件名
    :param pcs: 切片
    :return: None
    """
    for i in range(1, pcs + 1):
        logger.info(f"正在删除文件{filename}-{i}".center(80, '-'))
        os.remove(f'./danmu/{filename}-{i}.xml')


if __name__ == '__main__':
    logger.info("开始爱奇艺弹幕提取".center(80, '#'))
    video_url = input("视频链接：")
    kwargs = get_vid_duration_title(video_url)
    danmu_urls, num = get_danmu_urls(kwargs)
    if not os.path.exists('danmu/'):
        os.mkdir('./danmu/')
        logger.info("没有存储路径，创建文件夹 ./danmu/".center(80, '+'))
    for i in range(1, num + 1):
        download_danmu(danmu_urls[i - 1], kwargs['title'], i)
    xml2ass(f"./danmu/{kwargs['title']}", f"./danmu/{kwargs['title'].split('.')[0]}.ass", num)
    remove_xml(kwargs['title'], num)
    logger.info("爱奇艺弹幕下载结束".center(80, '#'))
