# -*- coding: utf-8 -*-
from selenium import webdriver


# ChromeOptions类的封装
class Options:
    def conf_options(self):
        # 配置ChromeOptions
        options = webdriver.ChromeOptions()
        # 1.默认启动的driver窗体最大化
        options.add_argument('start-maximized')
        # 2.去掉提示正在执行自动化的警告条
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 老版本去掉警告条方式：现在已经用不了了
        # options.add_argument('disable-infobars')
        # 3.让driver对象加载本地缓存
        # options.add_argument(r'--user-data-dir=C:\Users\SN-468\AppData\Local\Google\Chrome\User Data')
        # 4.添加无头指令
        # options.add_argument('--headless')
        # 5.添加去掉密码弹窗管理
        prefs = {}
        prefs['creadentials_enable_service'] = False
        prefs['profile.password_manager_enable'] = False
        options.add_experimental_option('prefs', prefs)
        # 6.隐身模式
        # options.add_argument('incognito')
        # 7.指定窗口大小
        # options.add_argument('window-size=2000,4000')
        # 8.在指定位置打开浏览器
        # options.add_argument('window-position=200,400')
        return options
