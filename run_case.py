#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import subprocess

WIN = sys.platform.startswith('win')
'''
该函数用于判断当前操作系统是否为Windows系统。
使用sys.platform.startswith('win')来检查系统平台是否以'win'开头，
如果是则返回True，否则返回False。这个函数通常用于编写跨平台的Python代码，
根据系统类型执行不同的操作或导入不同的模块。
'''


def main():
    """
    主函数，执行一系列的测试和报告生成步骤。

    该函数不需要参数，并且没有返回值。
    """
    # 定义执行步骤列表，每一步都是一个命令
    steps = [
        # 此处是激活虚拟环境的命令，根据操作系统不同而有差异
        "pytest --alluredir allure-results --clean-alluredir",  # 运行pytest测试，并将结果存储到allure-results目录中
        "allure generate allure-results -c -o allure-report",  # 生成测试报告
        "allure open allure-report"  # 打开生成的测试报告
    ]
    # 遍历步骤列表，并在当前环境下执行每个命令
    for step in steps:
        # 根据操作系统类型，使用不同的命令行调用方式
        subprocess.run("call " + step if WIN else step, shell=True)


if __name__ == "__main__":
    main()
