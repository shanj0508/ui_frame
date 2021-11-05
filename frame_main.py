# -*- coding: utf-8 -*-
'''
    关键字驱动框架程序的主入口
'''
import os

from excel_driver import excel_read
from my_conf import log_conf

if __name__ == '__main__':
    # 通过主入口调用excel的驱动读写,实现自动化测试
    # 1.生成日志器
    log = log_conf.get_log('./my_conf/log.ini')
    # 2.excel驱动实现
    # excel_read.excel_option(log)

    # 2.读取指定路径，获取所有的测试用例文件
    # 定义一个case的list:用于接收所有的测试用例文件 即.xlsx文件
    cases = []
    # 读取指定路径下的所有文件
    # print(os.listdir('./data'))  # ['data.xlsx', 'data1.xlsx', 'demo.txt']
    for path, dir, files in os.walk('./data/'):
        for file in files:
            # 获取文件的后缀名
            file_type = os.path.splitext(file)[1]
            if file_type == '.xlsx':
                excel_path = path + file
                cases.append(excel_path)
                print(excel_path)
            else:
                log.info('文件类型错误：{}'.format(file))
        # 3.调用excel_read进行关键字驱动自动化测试
        for case in cases:
            log.info('运行{}测试用例'.format(case))
            excel_read.excel_option(case, log)
