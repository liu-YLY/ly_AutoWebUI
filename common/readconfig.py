#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import configparser
from config.conf import settings

HOST = 'HOST'


class ReadConfig:
    """配置文件"""

    def __init__(self):
        self.config = configparser.RawConfigParser()  # 当有%的符号时请使用Raw读取
        # 不会对配置文件中的值进行任何转换，即它不会解析百分比符号 % 或变量替换，这使得它在处理原始配置数据时非常有用。
        self.config.read(settings.ini_file, encoding='utf-8')

    def _get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """更新"""
        self.config.set(section, option, value)
        with open(settings.ini_file, 'w') as f:
            self.config.write(f)

    @property
    def url(self):
        return self._get(HOST, HOST)


ini = ReadConfig()

if __name__ == '__main__':
    print(ini.url)
