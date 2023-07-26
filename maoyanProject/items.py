# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ALLItem(scrapy.Item):
    movie = scrapy.Field()
    cinema_date = scrapy.Field()
    city_name = scrapy.Field()
    cinema_name = scrapy.Field()
    cinema_url = scrapy.Field()
    cinema_address = scrapy.Field()
    begin_time = scrapy.Field()
    lang = scrapy.Field()
    # comment_num = scrapy.Field()
    hall = scrapy.Field()
    url = scrapy.Field()
    all_seats = scrapy.Field()
    selectable_seat = scrapy.Field()
    sold_seat = scrapy.Field()
    occupancy_rate = scrapy.Field()