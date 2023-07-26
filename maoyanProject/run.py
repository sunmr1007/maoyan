import json
import os
import sys

sys.path.append(os.path.abspath('../'))
from maoyanProject.DealData import DealData


def run(movie_date, cookies, file_path):
    from scrapy.cmdline import execute
    execute(["scrapy", "crawl", "ALLIN", "-a", f"movie_date={movie_date}", "-a", f"cookies={json.dumps(cookies)}"])
    # 对爬到的数据处理
    DealData().deal_data(fill_rate_dict, file_path)


if __name__ == '__main__':
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
    # 填场比例说明
    fill_rate_dict = {"非黄金场": 0.02, "黄金场": 0.05}
    file_path = "/Users/laysuda/Desktop/allin/test.xlsx"

    run(movie_date, cookies, file_path)
