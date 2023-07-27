import json
import os
import sys

sys.path.append(os.path.abspath('../'))
from maoyanProject.DealData import DealData


def run(movie_date, cookies, file_path, is_wanda):
    from scrapy.cmdline import execute
    execute(["scrapy", "crawl", "ALLIN", "-a", f"movie_date={movie_date}", "-a", f"cookies={json.dumps(cookies)}", "-a",
             f"is_wanda={is_wanda}"])
    # 对爬到的数据处理
    DealData().deal_data(fill_rate_dict, file_path)


if __name__ == '__main__':
    # 电影日期
    movie_date = "2023-07-28"
    # 要爬 台的万达(is_wanda=True)，散粉(is_wanda=False)
    is_wanda = True
    # 辛
    cookies = {
        # 不带上会302跳转
        'uuid': '',
        # 带账号信息
        "token": "",

        # 'token': 'AgHzH_f29UaMi59If77Rs_LW9HgDMuXqQ1lyfVRGs22jX-88opLYj62tj5wa473A0QAv-W1MrD8VZQAAAACpGQAAh1wIYfG23pnnNGMpMRHJR3PiL4YYTgJS05xJTssvRCO0p0AIfa7aJJcsnhUwjqp7',

    }
    # 填场比例说明
    fill_rate_dict = {"非黄金场": 0.02, "黄金场": 0.05}
    file_path = "/Users/laysuda/Desktop/allin/test.xlsx"

    run(movie_date, cookies, file_path, is_wanda)
