import json

import scrapy

from maoyanProject.items import ALLItem
from maoyanProject.utils.DealData import get_cinemas_info

"""
爬取每个电影院每个场次信息
"""


class Spider(scrapy.Spider):
    name = "ALLIN"

    def __init__(self, movie_date, cookies, is_who, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie_date = movie_date  # 日期（要填）
        # self.movieId = '1413252'  # 电影id（八角笼中）
        self.movieId = '1374349'  # 电影id（孤注一掷）
        self.movie = '孤注一掷'  # 电影名（孤注一掷）
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',

        }

        self.cookies = json.loads(cookies)
        self.cinemas_list = get_cinemas_info(is_who)

    def start_requests(self):
        for cinema in self.cinemas_list:
            if not cinema["cinema_url"]:
                return
            url = f'{cinema["cinema_url"]}&movieId={self.movieId}'
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                meta={'cinema_item': cinema}
            )
            # return

    def parse(self, response, **kwargs):
        cinema_item = response.meta["cinema_item"]
        # print(response.text)
        movie_data = self.movie_date.replace("-", "")
        xpath_params = f'//*[contains(@class,"show-list")]//a[contains(@href,"movieId={self.movieId}")][contains(@href,"{movie_data}")]/../..'
        rows = response.xpath(xpath_params)
        for row in rows:
            item = ALLItem()
            item["movie"] = self.movie
            item["cinema_date"] = self.movie_date
            item["city_name"] = cinema_item["city_name"]
            item["cinema_name"] = cinema_item["cinema_name"]
            item["cinema_url"] = cinema_item["cinema_url"]
            item["cinema_address"] = cinema_item["cinema_address"]

            item["begin_time"] = row.xpath('.//span[@class="begin-time"]/text()').get()
            item["lang"] = row.xpath('.//span[@class="lang"]/text()').get()
            item["hall"] = row.xpath('.//span[@class="hall"]/text()').get()
            # item["sell-price"] = row.xpath('.//span[@class="sell-price"]/text()').get()

            href = row.xpath('./td[last()]/a/@href').get()
            url = f"https://www.maoyan.com{href}"
            item["url"] = url
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.detail_parse,
                meta={"item": item}
            )
            # continue

    def detail_parse(self, response):
        item = response.meta["item"]
        selectable_seat = response.xpath('//span[contains(@class,"seat")][contains(@class,"selectable")]')
        sold_seat = response.xpath('//span[contains(@class,"seat")][contains(@class,"sold")]')
        item["selectable_seat"] = len(selectable_seat)
        item["sold_seat"] = len(sold_seat)
        item["all_seats"] = item["sold_seat"] + item["selectable_seat"]
        try:
            occupancy_rate = item["sold_seat"] / (item["sold_seat"] + item["selectable_seat"])
        except:
            occupancy_rate = 0.00
            print(item["all_seats"])
            print(item["selectable_seat"])
            print(item["sold_seat"])
        item["occupancy_rate"] = f"{occupancy_rate:.2%}"
        # print(item)
        yield item


if __name__ == "__main__":
    from scrapy.cmdline import execute

    # execute(["scrapy", "crawl", Spider.name])
    # 电影日期
    movie_date = "2023-07-27"
    # 要爬 台的万达(is_who=0)，兴吧(is_who=1)，散粉(is_who=2)
    is_who = 0
    # is_who = 1
    # is_who = 2
    # 要爬取的影院信息列表
    cinemas_list = get_cinemas_info(is_who)

    # 辛
    cookies = {
        # 不带上会302跳转
        'uuid': '',
        # 带账号信息
        "token": "",

    }
    execute(["scrapy", "crawl", "ALLIN", "-a", f"movie_date={movie_date}", "-a", f"cookies={json.dumps(cookies)}", "-a",
             f"is_who={is_who}"])
