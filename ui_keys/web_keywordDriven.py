# -*- coding: utf-8 -*-
'''
    关键字驱动类
'''
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from my_conf import log_conf
from my_conf.chrome_options import Options
import logging.config


# 在后续的自动化中，通过调用这个类进行自动化操作，逻辑代码

# 要满足创建任意一个浏览器对象的需求


def open_browser(type_):
    try:
        if type_ == 'Chrome':
            return webdriver.Chrome(options=Options().conf_options())
        else:
            return getattr(webdriver, type_)()
    except:
        return webdriver.Chrome()


class WebKey:
    # 定义常规的测试操作行为
    # 创建一个临时的driver对象，便于代码的编写。
    # driver = webdriver.Chrome()

    # 创建构造函数，用于初始化self.driver对象,要考虑到driver对象可能是任意一种浏览器对象
    def __init__(self, text, log):
        self.driver = open_browser(text)
        self.log = log
        # 隐式等待
        self.driver.implicitly_wait(10)

    # 访问url
    def visit(self, text):
        self.driver.get(text)

    # 关闭浏览器driver释放资源
    def quit(self):
        self.driver.quit()

    # 元素定位:目的是为了通过定义一个方法来实现所有的元素定位。
    # 因为元素定位后，我们会在后续对这个元素进行一系列的操作，所以必须将定位的元素对象return回来，否则后续操作点击、输入等操作时会报错
    def locator(self, name, value):
        return self.driver.find_element(name, value)

    # 输入
    def input(self, name, value, text):
        self.locator(name, value).send_keys(text)

    # 点击
    def click(self, name, value):
        self.locator(name, value).click()

    # 强制等待
    def sleep(self, text):
        sleep(text)

    # 显示等待
    def wait(self, name, value):
        WebDriverWait(self.driver, 10, 0.1).until(lambda el: self.driver.find_element(name, value),
                                                  message='等待失败')

    # 隐式等待：不需要封装，因为它是配置固定的等待时间

    # 句柄的切换：包含关闭原页面
    def handle_close(self):
        handles = self.driver.window_handles
        self.driver.close()
        self.driver.switch_to.window(handles[1])

    # 句柄的切换：不包含关闭原页面
    def handle(self, text=1):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[text])

    # 切换frame
    def switch_frame(self, text):
        self.driver.switch_to.frame(text)

    # 获取元素文本
    # def get_text(self, name, value):
    #     return self.locator(name, value).text

    # 文本断言
    def assert_text(self, name, value, expect):
        try:
            reality = self.locator(name, value).text
            assert reality == expect, '断言失败'
            return True
        except Exception:
            self.log.exception('出现异常，断言失败：{0}!={1}'.format(expect, reality))
            return False

    # 属性断言
    def assert_attr(self, name, value, txt, expect):
        try:
            reality = self.locator(name, value).get_attribute(txt)
            assert reality == expect, '断言失败'
            return True
        except Exception:
            self.log.exception('出现异常，断言失败：{0}!={1}'.format(expect, reality))
            return False

    # 清除文本框内容
    def clear(self, name, value):
        self.locator(name, value).clear()

    # 清除文本框内容并输入新值
    def clear_input(self, name, value, text):
        el = self.locator(name, value)
        el.clear()
        el.send_keys(text)

    # 获取属性值
    def get_attribute(self, name, value, text):
        return self.locator(name, value).get_attribute(text)
