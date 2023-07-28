import json
import os
import sys

sys.path.append(os.path.abspath('../'))

# 电影日期
movie_date = "2023-08-11"

# 要爬 台的万达(is_who=0)，兴吧(is_who=1)，散粉(is_who=2)
is_who = 0
# is_who = 1
# is_who = 2

# 写一次之后就不用改了，除非失效
cookies = {
    # 不带上会302跳转
    'uuid': '',
    # 带账号信息
    "token": "",

}

from scrapy.cmdline import execute

execute(["scrapy", "crawl", "ALLIN", "-a", f"movie_date={movie_date}", "-a", f"cookies={json.dumps(cookies)}", "-a",
         f"is_who={is_who}"])
