# -*- coding: utf-8 -*-
'''
    Excel数据驱动效果实现。
    实现目的：基于excel中的内容，来调用关键字类，实现自动化测试的执行效果
            相当于，excel文件就是一个测试用例，底层代码就是关键字驱动类以及excel驱动类
'''
import openpyxl

from excel_driver.excel_conf import ExcelConf
from my_conf import log_conf
from ui_keys.web_keywordDriven import WebKey


# Excel数据驱动类
def excel_option(path, log):
    # 读取excel文件，创建workbook实例化对象
    excel = openpyxl.load_workbook(path)

    try:
        # 获取所有的sheet页
        sheets = excel.sheetnames
        # 遍历所有sheet页
        for sheet in sheets:
            sheet_temp = excel[sheet]
            log.info('----------{}----------'.format(sheet))
            # 遍历sheet页中所有单元格
            for values in sheet_temp.values:
                # 读取用例的执行部分内容，表头的一些描述内容不需要读取，即从编号为1开始读取
                if type(values[0]) is int:
                    # 控制台打印日志信息
                    log.info('正在执行：{}'.format(values[5]))
                    # 提取本行的测试数据
                    data = {}
                    data['name'] = values[2]  # 定位方法
                    data['value'] = values[3]  # 定位路径
                    data['text'] = values[4]  # 输入文本
                    data['expect'] = values[6]  # 预期结果
                    # 优化测试数据内容，将所有值为None的数据全部清除出data中
                    for key in list(data.keys()):
                        # print(key)
                        if data[key] is None:
                            del data[key]
                    # 调用对应的关键字来执行操作行为
                    '''
                        执行操作分为三种场景：
                            1.open_browser：创建实例化类对象WebKey
                            2.assert_text：断言，返回True或False,将结果写入excel的实际结果单元格中
                            3.其他常规操作：访问、点击、输入等
                        每种不同的场景，需要不同的处理。
                    '''

                    if values[1] == 'open_browser':
                        # 实例化对象
                        wk = WebKey(values[4], log)
                        # wk = WebKey(**data)
                    # 断言可能有多种，例如文本断言、属性断言等，对应多个断言方法。
                    # 因此这里判断：values[1]的值中包含'assert_'即表示是个断言
                    elif 'assert_' in values[1]:
                        # 用变量接收断言的返回值：True或False
                        status = getattr(wk, values[1])(**data)
                        # 基于status写入测试结果
                        if status:
                            # 写入单元格样式
                            ExcelConf.pass_(cell=sheet_temp.cell, row=values[0] + 2, column=8)

                        else:
                            # 写入单元格样式
                            ExcelConf.failed_(cell=sheet_temp.cell, row=values[0] + 2, column=8)
                        # 执行excel保存
                        excel.save(path)
                    else:
                        getattr(wk, values[1])(**data)
    except Exception as e:
        log.info('运行异常：{}'.format(e))
    finally:
        # 关闭excel
        excel.close()

# if __name__ == '__main__':
#     excel_option()
