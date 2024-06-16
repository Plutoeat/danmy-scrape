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
    return f"{hours}:{minutes}:{seconds}.00"


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
        f.write("[Script Info]\n")
        f.write("Title: {}\n".format(xml_file.split('/')[-1]))
        f.write("Original Script: 自用 danmu-scrape 下载生成 ASS 字幕\n")
        f.write("ScriptType: v4.00+\n")
        f.write("Collisions: Normal\n")
        f.write("PlayResX: 1920\n")
        f.write("PlayResY: 1080\n")
        f.write("WrapStyle: 0\n\n")
        f.write("[V4+ Styles]\n")
        f.write(
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write(
            "Style: RightMode1,Microsoft YaHei UI,14,&H80FFFFFF,&H80FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,1,0,2,20,20,2,0\n")
        f.write(
            "Style: TopMode1,Microsoft YaHei UI,14,&H80FFFFFF,&H80FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,1,0,2,20,20,2,0\n\n")
        f.write("[Events]\n")
        f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Tex\n")
        if pcs > 1:
            for i in range(1, pcs + 1):
                tree = ET.parse(xml_file + '-' + str(i) + '.xml')
                root = tree.getroot()
                for entry in root.findall('data')[0].findall('entry'):
                    bullet = entry.findall('list')[0].findall('bulletInfo')[0]
                    content = bullet.findall('content')[0].text
                    showTime = bullet.findall('showTime')[0].text
                    font = int(bullet.findall('font')[0].text)
                    color = bullet.findall('color')[0].text
                    opacity = int(bullet.findall('opacity')[0].text)
                    position = int(bullet.findall('position')[0].text)
                    start_ass = convert_time(int(showTime))
                    end_ass = convert_time(int(showTime) + 38)
                    f.write(
                        "Dialogue: %s,%s,%s,RightMode1,,20,20,2,,{\move(%s,%s,%s,%s)\c&H%s}%s\n" % (
                            str(10 - opacity),
                            start_ass,
                            end_ass,
                            str(1940 + font),
                            str(position + 3 * font + 20),
                            str(-20 - font),
                            str(position + 3 * font + 20),
                            color,
                            content
                        ))
        else:
            tree = ET.parse(xml_file + '.xml')
            root = tree.getroot()
            for entry in root.findall('data')[0].findall('entry'):
                bullet = entry.findall('list')[0].findall('bulletInfo')[0]
                content = bullet.findall('content')[0].text
                showTime = bullet.findall('showTime')[0].text
                font = int(bullet.findall('font')[0].text)
                color = bullet.findall('color')[0].text
                opacity = bullet.findall('opacity')[0].text
                position = int(bullet.findall('position')[0].text)
                start_ass = convert_time(int(showTime))
                end_ass = convert_time(int(showTime) + 38)
                f.write(
                    "Dialogue: %s,%s,%s,RightMode1,,20,20,2,,{\move(%s,%s,%s,%s)\c&H%s}%s\n"%(
                        str(10 - opacity),
                        start_ass,
                        end_ass,
                        str(1940 + font),
                        str(position + 3 * font + 20),
                        str(-20 - font),
                        str(position + 3 * font + 20),
                        color,
                        content
                    ))
