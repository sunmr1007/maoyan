import json

import scrapy

from maoyanProject.DealData import DealData
from maoyanProject.items import ALLItem

"""
爬取每个电影院每个场次信息
"""


class Spider(scrapy.Spider):
    name = "ALLIN"

    def __init__(self, movie_date, cookies, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie_date = movie_date  # 日期（要填）
        # self.movieId = '1439161'  # 电影id（热烈）
        self.movieId = '1413252'  # 电影id（热烈）
        self.movie = '八角笼中'  # 电影名（热烈）
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',

        }

        # 不确定能用多久
        # self.cookies = {
        #     # 不带上会302跳转
        #     'uuid': '0D3967E0264C11EEB6A41DA4355E52AD0CF4EA203D9B4C4C87A92A91B8530B1B',
        #     # 带账号信息
        #     "token": "AgFrIGfnjMWSn06fBToS8lbrobT46--jEls-t0aOwbwty2_5d6yUapCo8SNtiwxHYp2_LPw0NV3l8QAAAACpGQAAA0P6gd32VWPE88YWaATUITKfqHBQepPDDQWNKCsKcYvQKUkEjcoYi13wEY9b5nBy",
        #
        #     # 'token': 'AgHzH_f29UaMi59If77Rs_LW9HgDMuXqQ1lyfVRGs22jX-88opLYj62tj5wa473A0QAv-W1MrD8VZQAAAACpGQAAh1wIYfG23pnnNGMpMRHJR3PiL4YYTgJS05xJTssvRCO0p0AIfa7aJJcsnhUwjqp7',
        #
        # }

        self.cookies = json.loads(cookies)
        self.cinemas_list = DealData().get_cinemas_info()

    def start_requests(self):
        for cinema in self.cinemas_list[1000:1166]:
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
            # return

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
    # 要爬取的影院信息列表
    cinemas_list = DealData().get_cinemas_info()
    # 辛
    cookies = {
        # 不带上会302跳转
        'uuid': '53A74BA02AA411EEBE787F4E202C30183C00B5645C594930889421530C736F9D',
        # 带账号信息
        "token": "AgEFJZt2EivC9L3IYC9TrtsgaiqnrILqn2lAHgJB0JQWwTmzawx8CKWLUCJ-yO8id6H3qLeX-tCfBgAAAACpGQAAwTfPXP1XEf49FAX89lmFs8aky7VEpO-Mm70NUiNq3q_mxpdC20G2QrEsAY01YbKI",

        # 'token': 'AgHzH_f29UaMi59If77Rs_LW9HgDMuXqQ1lyfVRGs22jX-88opLYj62tj5wa473A0QAv-W1MrD8VZQAAAACpGQAAh1wIYfG23pnnNGMpMRHJR3PiL4YYTgJS05xJTssvRCO0p0AIfa7aJJcsnhUwjqp7',

    }
    execute(["scrapy", "crawl", "ALLIN", "-a", f"movie_date={movie_date}", "-a", f"cookies={json.dumps(cookies)}"])
