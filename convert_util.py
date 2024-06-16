#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project: danmy-scrape
@File: convert_util.py
@IDE: PyCharm
@Author: paidaxing
@Date: 2024/6/16 21:15
"""
import xml.etree.ElementTree as ET


def convert_time(ts: int) -> str:
    hours = ts // 3600
    minutes = (ts % 3600) // 60
    seconds = ts % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.00"


def xml2ass(xml_file: str, ass_file: str, pcs: int) -> None:
    """
    将 xml 文件转换为 ass 文件
    :param xml_file: xml 文件地址
    :param ass_file: ass 文件地址
    :param pcs: xml 文件数量
    :return: None
    """
    # 打开 ass 文件准备写入
    with open(ass_file, 'w', encoding='utf-8') as f:
        f.write("Script Type: v4.00+\n")
        f.write("Collisions: Normal\n")
        f.write("PlayResX: 1920\n")
        f.write("PlayResY: 1080\n\n")
        if pcs > 1:
            for i in range(1, pcs + 1):
                tree = ET.parse(xml_file+'-'+str(i) + '.xml')
                root = tree.getroot()
                for entry in root.findall('data')[0].findall('entry'):
                    bullet = entry.findall('list')[0].findall('bulletInfo')[0]
                    content = bullet.findall('content')[0].text
                    showTime = bullet.findall('showTime')[0].text
                    font = bullet.findall('font')[0].text
                    color = bullet.findall('color')[0].text
                    opacity = bullet.findall('opacity')[0].text
                    position = bullet.findall('position')[0].text
                    layer = 10 - int(opacity)
                    start_ass = convert_time(int(showTime))
                    end_ass = convert_time(int(showTime) + 3)
                    f.write(
                        f"Dialogue: {layer},{start_ass},{end_ass},Default,,0,{position},0,\\fnArial\\c&H{color}\\fad(500,200),{content}")
        else:
            tree = ET.parse(xml_file+'.xml')
            root = tree.getroot()
            for entry in root.findall('data')[0].findall('entry'):
                bullet = entry.findall('list')[0].findall('bulletInfo')[0]
                content = bullet.findall('content')[0].text
                showTime = bullet.findall('showTime')[0].text
                font = bullet.findall('font')[0].text
                color = bullet.findall('color')[0].text
                opacity = bullet.findall('opacity')[0].text
                position = bullet.findall('position')[0].text
                layer = 10 - int(opacity)
                start_ass = convert_time(int(showTime))
                end_ass = convert_time(int(showTime) + 3)
                f.write(
                    f"Dialogue: {layer},{start_ass},{end_ass},Default,,0,{position},0,\\fnArial\\c&H{color}\\fad(500,200),{content}")
