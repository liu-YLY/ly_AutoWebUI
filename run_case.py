#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import subprocess

WIN = sys.platform.startswith('win')


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
