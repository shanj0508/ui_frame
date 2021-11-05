# -*- coding: utf-8 -*-
'''
    生成日志器的配置
'''
import logging.config


# 路径需要在调用的时候进行填写，否则会报错
def get_log(path):
    logging.config.fileConfig(path)
    return logging.getLogger()
