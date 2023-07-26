# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from os.path import dirname

from scrapy.exporters import CsvItemExporter


# useful for handling different item types with a single interface

import maoyanProject.files


FilePath = dirname(maoyanProject.files.__file__)

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
                                        fields_to_export=["movie", "city_name", "cinema_date", "cinema_name",
                                                          'cinema_url', "cinema_address", "hall",
                                                          "lang", "begin_time", "all_seats", "selectable_seat", "sold_seat",
                                                          "occupancy_rate", "url"
                                                          ])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        # print(item)
        self.count += 1
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        print(self.count)
        self.file.close()
