#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import yaml
from config.conf import settings


class Element:
    """获取元素"""

    def __init__(self, name: str):
        """
        初始化元素管理器实例。

        该构造函数用于创建一个元素管理器的实例，它会根据给定的名称加载对应的yaml文件。
        如果文件不存在，则会抛出一个FileNotFoundError。

        :param name: 元素的名称，用于构造yaml文件的名称。
        """
        # 根据名称生成yaml文件名
        self.file_name = f'{name}.yaml'
        # 构建元素文件的完整路径
        self.element_path = os.path.join(settings.ELEMENT_PATH, self.file_name)
        # 检查元素文件是否存在，如果不存在则抛出异常
        if not os.path.exists(self.element_path):
            raise FileNotFoundError(f"{self.element_path} 文件不存在！")
        # 打开元素文件，并使用yaml安全加载器加载文件内容到self.data
        with open(self.element_path, encoding='utf-8') as f:
            self.data = yaml.safe_load(f)


    """
    获取属性的值。

    参数:
    - item: str，要获取的属性名称。

    返回值:
    - tuple，包含属性名称和属性值的元组。

    异常:
    - KeyError: 如果传入的属性名称为空。
    - ArithmeticError: 如果属性在文件中不存在。
    - ValueError: 如果属性数据格式不正确（不包含'=='）。
    """
    def __getitem__(self, item: str):
        """获取属性"""
        if not item:
            raise KeyError("关键字不正确")
        data: str = self.data.get(item)
        if not data:
            raise ArithmeticError(f"{self.file_name}中不存在关键字：{item}")
        if '==' not in data:
            raise ValueError(f"{self.file_name}中{item}关键字数据不正确")
        name, value = data.split('==')
        return name, value


if __name__ == '__main__':
    search = Element('search')
    print(search['搜索框'])
