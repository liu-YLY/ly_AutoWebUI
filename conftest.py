#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import base64
import pytest
import allure
from py.xml import html
from selenium import webdriver

from config.conf import settings
from common.readconfig import ini
from utils.times import timestamp
from utils.send_mail import send_report
#from chromedriver_py import binary_path
#from selenium.webdriver.chrome.service import Service

driver = None

# 定义一个测试夹具，用于会话级别的Selenium WebDriver管理
@pytest.fixture(scope='session', autouse=True)
def drivers(request):
    """
    初始化并提供一个会话级别的Chrome驱动实例。
    该fixture自动激活，用于所有测试会话中的Chrome浏览器实例初始化和销毁。
    """

    # 全局变量，用于存储Selenium WebDriver实例
    global driver

    # 检查driver是否已初始化，如果没有，则进行初始化
    if driver is None:
        # 初始化Chrome驱动服务
        driver = webdriver.Chrome()
        driver.maximize_window()

    # 定义一个函数，用于在测试结束后关闭驱动
    def fn():
        driver.quit()

    # 将关闭驱动的函数注册为测试的最终执行函数，确保测试结束后驱动能被正确关闭
    # 添加一个函数fn，在request对象被销毁时调用
    request.addfinalizer(fn)

    # 返回驱动实例，供测试使用
    return driver
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """
#     当测试失败的时候，自动截图，展示到html报告中
#     :param item:
#     """
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     report.description = str(item.function.__doc__)
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             screen_img = _capture_screenshot()
#             if screen_img:
#                 html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % screen_img
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra
#
#
# def pytest_html_results_table_header(cells):
#     cells.insert(1, html.th('用例名称'))
#     cells.insert(2, html.th('Test_nodeid'))
#     cells.pop(2)
#
#
# def pytest_html_results_table_row(report, cells):
#     cells.insert(1, html.td(report.description))
#     cells.insert(2, html.td(report.nodeid))
#     cells.pop(2)
#
#
# def pytest_html_results_table_html(report, data):
#     if report.passed:
#         del data[:]
#         data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))
#
#
# def pytest_html_report_title(report):
#     report.title = "pytest示例项目测试报告"
#
#
# """
# def pytest_configure(config): # QA FAIL
#     config._metadata.clear()
#     config._metadata['测试项目'] = "测试百度官网搜索"
#     config._metadata['测试地址'] = ini.url
# """
#
#
# def pytest_html_results_summary(prefix, summary, postfix):
#     # prefix.clear() # 清空summary中的内容
#     prefix.extend([html.p("所属部门: XX公司测试部")])
#     prefix.extend([html.p("测试执行人: 随风挥手")])
#
#
# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     """收集测试结果"""
#     result = {
#         "total": terminalreporter._numcollected,
#         'passed': len(terminalreporter.stats.get('passed', [])),
#         'failed': len(terminalreporter.stats.get('failed', [])),
#         'error': len(terminalreporter.stats.get('error', [])),
#         'skipped': len(terminalreporter.stats.get('skipped', [])),
#         # terminalreporter._sessionstarttime 会话开始时间
#         'total times': timestamp() - terminalreporter._sessionstarttime
#     }
#     print(result)
#     if result['failed'] or result['error']:
#         send_report()
#
#
# def _capture_screenshot():
#     """截图保存为base64"""
#     now_time, screen_file = settings.screen_path
#     driver.save_screenshot(screen_file)
#     allure.attach.file(screen_file,
#                        "失败截图{}".format(now_time),
#                        allure.attachment_type.PNG)
#     with open(screen_file, 'rb') as f:
#         imagebase64 = base64.b64encode(f.read())
#     return imagebase64.decode()
