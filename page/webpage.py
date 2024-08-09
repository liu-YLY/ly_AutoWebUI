#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
selenium基类
本文件存放了selenium基类的封装方法
"""
from typing import Union, Callable
from selenium.webdriver import Chrome, Firefox, Edge, Ie, Safari, Remote
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config.conf import settings
from utils.times import sleep
from utils.logger import logger


class WebPage(object):
    """selenium基类"""

    def __init__(self, driver):
        self.driver: Union[Chrome, Firefox, Edge, Ie, Safari, Remote] = driver
        self.timeout: int = 20
        self.wait: WebDriverWait = WebDriverWait(self.driver, self.timeout)

    def get_url(self, url):
        """
        打开并加载指定URL。

        此方法尝试最大化浏览器窗口，并设置页面加载超时时间为60秒，以确保页面能够及时加载完成。
        如果页面加载超时，将抛出TimeoutException异常。

        参数:
        url (str): 需要打开的URL地址。

        抛出:
        TimeoutException: 如果页面在指定的超时时间内未能加载完成。
        """
        # 最大化浏览器窗口以获得更好的用户体验
        self.driver.maximize_window()
        # 设置页面加载的超时时间，超过这个时间将抛出超时异常
        self.driver.set_page_load_timeout(60)
        try:
            # 尝试打开指定的URL
            self.driver.get(url)
            # 设置隐式等待时间，即在查找元素时等待页面加载的时间
            self.driver.implicitly_wait(10)
            # 记录日志，表示页面打开成功
            logger.info("打开网页：%s" % url)
        except TimeoutException:
            # 如果页面加载超时，抛出异常并提示用户
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    @staticmethod
    def element_locator(func: Callable, locator: tuple):
        """
        元素定位器静态方法。

        参数:
        - func: Callable - 定位元素的函数。
        - locator: tuple - 元素定位信息的元组，包含定位方式名称和定位值。

        返回值:
        - 使用给定的定位方式和值，通过func函数定位出的元素。
        """
        logger.info("locator is:{}".format(locator))  # 记录定位器信息
        name, value = locator  # 解包定位器元组
        return func(settings.LOCATE_MODE[name], value)  # 使用定位方式和值调用函数进行元素定位

    def find_element(self, locator: tuple):
        """寻找单个元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)

    def find_elements(self, locator: tuple):
        """查找多个相同的元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def elements_num(self, locator: tuple) -> int:
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        logger.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, locator: tuple, txt: str):
        """输入(输入前先清空)"""
        sleep(0.5)
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(txt)
        logger.info("输入文本：{}".format(txt))

    def click(self, locator: tuple):
        """点击"""
        self.find_element(locator).click()
        sleep()
        logger.info("点击元素：{}".format(locator))

    def is_visible(self, locator: tuple) -> bool:
        """元素是否可见"""
        try:
            ele = WebPage.element_locator(lambda *args: self.visible_obj.until(
                EC.visibility_of_element_located(args), locator))
            if ele:
                return True
            return False
        except TimeoutException:
            return False

    def element_text(self, locator: tuple):
        """获取当前的text"""
        _text = self.find_element(locator).text
        logger.info("获取文本：{}".format(_text))
        return _text

    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)


if __name__ == "__main__":
    pass
