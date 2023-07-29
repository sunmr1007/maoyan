# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from os.path import dirname

from scrapy.exporters import CsvItemExporter

import maoyanProject.files
from maoyanProject.utils.DealData import check_gold

# useful for handling different item types with a single interface
# from maoyanProject.run import file_to_path, fill_rate_dict

FilePath = dirname(maoyanProject.files.__file__)
# 填场比例说明
fill_rate_dict = {"非黄金场": 0.02, "黄金场": 0.05}


class MaoyanprojectPipeline:
    def process_item(self, item, spider):
        return item


class ALLPipeline(object):
    def open_spider(self, spider):
        self.count = 0
        # self.file = open(f"C:/Users/Administrator/Desktop/allin.csv", "wb")
        # self.file = open("/Users/laysuda/Desktop/allin/热烈0726.csv", "wb")
        self.file = open(f"{FilePath}/allin.csv", "ab")
        self.exporter = CsvItemExporter(self.file, encoding='utf-8-sig',
                                        fields_to_export=["movie", "owner", "city_name", "cinema_date", "cinema_name",
                                                          'cinema_url', "cinema_address", "hall",
                                                          "lang", "begin_time", "all_seats", "selectable_seat",
                                                          "sold_seat",
                                                          "occupancy_rate", "url", "is_weekday", "is_gold", "fill_rate",
                                                          "fill_seats"
                                                          ])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.count += 1
        insert_item = item

        insert_item['is_weekday'], insert_item['is_gold'], insert_item['fill_rate'] = check_gold(
            insert_item['cinema_date'], insert_item['begin_time'], fill_rate_dict)

        insert_item['fill_seats'] = insert_item['all_seats'] * insert_item['fill_rate']
        insert_item['fill_seats'] = round(insert_item['fill_seats'])
        item = insert_item
        self.exporter.export_item(item)
        return dict(item)

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        print(self.count)
        self.file.close()
