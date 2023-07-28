# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from os.path import dirname
import pandas as pd
from scrapy.exporters import CsvItemExporter


# useful for handling different item types with a single interface

import maoyanProject.files
from maoyanProject.utils.DealData import check_gold
# from maoyanProject.run import file_to_path, fill_rate_dict

FilePath = dirname(maoyanProject.files.__file__)
# 填场比例说明
fill_rate_dict = {"非黄金场": 0.02, "黄金场": 0.05}

# 数据导出本地路径
file_to_path = "/Users/laysuda/Desktop/allin/test.xlsx"

class MaoyanprojectPipeline:
    def process_item(self, item, spider):
        return item


class ALLPipeline(object):
    def open_spider(self, spider):
        self.count = 0
        # self.file = open(f"C:/Users/Administrator/Desktop/allin.csv", "wb")
        # self.file = open("/Users/laysuda/Desktop/allin/热烈0726.csv", "wb")
        self.file = open(f"{FilePath}/allin.csv", "wb")
        self.exporter = CsvItemExporter(self.file, encoding='utf-8-sig',
                                        fields_to_export=["movie", "city_name", "cinema_date", "cinema_name",
                                                          'cinema_url', "cinema_address", "hall",
                                                          "lang", "begin_time", "all_seats", "selectable_seat", "sold_seat",
                                                          "occupancy_rate", "url"
                                                          ])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.count += 1
        insert_item = item

        insert_item['is_weekday'], insert_item['is_gold'], insert_item['fill_rate'] = check_gold(insert_item['cinema_date'], insert_item['begin_time'], fill_rate_dict)

        insert_item['fill_seats'] = insert_item['all_seats'] * insert_item['fill_rate']
        insert_item['fill_seats'] = round(insert_item['fill_seats'])
        self.exporter.export_item(insert_item)
        return dict(item)

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        print(self.count)
        self.file.close()
        # 处理得到的csv文件
        df = pd.read_csv(f"{FilePath}/allin.csv")
        try:
            df = df.drop(df[df['movie'] == 'movie'].index)
        except:
            pass
        # 排序
        df.sort_values(by=['city_name', 'cinema_name', 'begin_time'], inplace=True)
        df.rename(columns={
            'movie': '电影名',
            'city_name': '城市',
            'cinema_date': '日期',
            'cinema_name': '影院名称',
            'cinema_url': '影院猫眼网址',
            'cinema_address': '影院地址',
            'hall': '影厅类型',
            'lang': '语言版本',
            'begin_time': '放映时间',
            'all_seats': '总座位数',
            'selectable_seat': '可选座位数',
            'sold_seat': '已售座位数',
            'occupancy_rate': '上座率',
            'url': '购票网址',
            'is_weekday': '是否为工作日',
            'is_gold': '是否为黄金场',
            'fill_rate': '填场比例',
            'fill_seats': '需填场数量',
        }, inplace=True)
        # 导出
        df.to_excel(file_to_path, index=False)
