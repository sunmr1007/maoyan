# -*- coding : utf-8 -*-
# @Time :2023/1/31 9:33
# @Author :sun
# @File :  19249.py

"""
用playwright 爬取12个城市的所有影院信息
"""
import scrapy
from loguru import logger
from lxml import etree
from playwright import sync_api

# from items import CinemaItem


class Spider(scrapy.Spider):
    # playwright
    name = 'city'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://www.maoyan.com"
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        self.headless = False

    def start_requests(self):
        playwright = sync_api.sync_playwright().start()
        browser = playwright.firefox.launch(headless=self.headless)
        # playwright使用代理会严重影响页面渲染速度
        # browser = playwright.chromium.launch(headless=self.headless)
        self.context = browser.new_context()
        # 禁止请求图片
        self.context.route("**/*", lambda route:
        route.abort() if route.request.resource_type in ('image', 'media') else route.continue_())

        page = self.context.new_page()

        try:
            page.goto(self.url)
            page.wait_for_load_state('networkidle')  # 等待页面到至少500ms没有网络连接
            page.wait_for_load_state()  # 等待load事件被触发
            page.click(f'//a[@data-act="cinemas-click"]')
            page.wait_for_timeout(3000)
            page.wait_for_load_state('networkidle')
        except Exception as e:
            logger.warning(e)

        else:
            # for city_id in ['1', '10', '20', '30', '80', '45', '59', '50', '57', '42', '65', '73']:
            for city_id in ['73']:
                xpath_part = f'//a[@data-ci="{city_id}"]'
                print(xpath_part)
                page.click(xpath_part)
                page.wait_for_timeout(3000)
                page.wait_for_load_state('networkidle')  # 等待页面到至少500ms没有网络连接
                for page_num in range(14):
                    html = etree.HTML(page.content())
                    page.click('text=下一页')
                    page.wait_for_load_state()  # 等待load事件被触发

                    yield scrapy.Request(
                        url="https://www.baidu.com/",
                        dont_filter=True,
                        meta={
                            'html': html,
                            'city_id': city_id,
                            'page_num': page_num
                        }
                    )
        # playwright.stop()

    def parse(self, response, **kwargs):
        for meta in self.parse_page(response.meta['html'], response.meta['page_num']):
            # item = CinemaItem()  # 项目信息
            item = {}
            item["city_id"] = response.meta['city_id']
            item["cinema_name"] = meta['cinema_name']
            item["cinema_address"] = meta['cinema_address']
            item["cinema_url"] = meta['cinema_url']
            item["pager_index"] = meta['pager_index']
            item["pager_item_index"] = meta['pager_item_index']
            # print(item)
            # yield item

    def parse_page(self, html, page_num):
        rows = html.xpath('//*[@class="cinema-info"]')

        for index, row in enumerate(rows):
            # 项目名
            cinema_name = row.xpath("./a/text()")[0]
            # 详情页url
            href = row.xpath("./a/@href")[0]
            url = f"https://www.maoyan.com{href}"
            cinema_address = row.xpath('./p[@class="cinema-address"]/text()')[0]
            # 页数行数
            pager_index = page_num
            pager_item_index = index
            meta = {
                'cinema_name': cinema_name,
                'cinema_address': cinema_address,
                'cinema_url': url,
                'pager_index': pager_index,
                'pager_item_index': pager_item_index,
            }
            yield meta


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(["scrapy", "crawl", Spider.name])
