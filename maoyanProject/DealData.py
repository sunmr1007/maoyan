import datetime
import json
from os.path import dirname

import pandas as pd
from loguru import logger

import maoyanProject.files

FilePath = dirname(maoyanProject.files.__file__)


class DealData():

    def get_cinemas_info(self, is_wanda=True):
        """
        获取要爬取的电影院信息
        :return:
        """
        # cinema_all_df = pd.read_excel(f'{FilePath}/cinemas_all.xlsx')
        # cinema_need_df = pd.read_excel(f'{FilePath}/cinemas_need.xlsx')
        # cinema_other_df = pd.read_excel(f'{FilePath}/cinema_other.xlsx')
        # cinema_df = pd.read_excel(f'{FilePath}/cinemas.xlsx')
        if is_wanda:
            # 台台
            df = pd.read_excel(f'{FilePath}/cinema_tai.xlsx')
        else:
            # 其他
            df = pd.read_excel(f'{FilePath}/cinema_other.xlsx')
        # df.to_excel(f'{FilePath}/cinema_other.xlsx', index=False)
        data = df.to_json(orient="table")
        cinemas_list = json.loads(data)["data"]
        for cinema in cinemas_list:
            if not cinema.get("cinema_url"):
                logger.warning(f'{cinema["cinema_name"]} 未匹配到该影院，请核查！')
                return
        return cinemas_list

    def check_gold(self, date, begin_time, fill_rate_dict):
        """
        判断是否工作日、是否黄金场、填充排场比例
        :param date: 日期
        :param begin_time: 放映时间
        :param fill_rate_dict: 填场比例
        :return:
        """
        cinema_time = datetime.datetime.strptime(date + "" + begin_time, '%Y-%m-%d%H:%M')
        res = len(pd.bdate_range(date, date))
        if res == 0:
            is_weekday = "周末"
            start_time = datetime.datetime.strptime(date + "13:00", '%Y-%m-%d%H:%M')
            end_time = datetime.datetime.strptime(date + "22:00", '%Y-%m-%d%H:%M')

            is_gold = "非黄金场"
            fill_rate = fill_rate_dict["非黄金场"]
            if start_time < cinema_time < end_time:
                is_gold = "黄金场"
                fill_rate = fill_rate_dict["黄金场"]
        else:
            is_weekday = "工作日"
            start_time = datetime.datetime.strptime(date + "18:00", '%Y-%m-%d%H:%M')
            end_time = datetime.datetime.strptime(date + "22:00", '%Y-%m-%d%H:%M')
            is_gold = "非黄金场"
            fill_rate = fill_rate_dict["非黄金场"]
            if start_time < cinema_time < end_time:
                is_gold = "黄金场"
                fill_rate = fill_rate_dict["黄金场"]
        return is_weekday, is_gold, fill_rate

    def deal_data(self, fill_rate_dict: dict, file_path: str):
        df = pd.read_csv(f"{FilePath}/allin.csv")
        # 判断是否是工作日、黄金场
        df[['is_weekday', 'is_gold', 'fill_rate']] = df.apply(
            lambda x: pd.Series(self.check_gold(x['cinema_date'], x['begin_time'], fill_rate_dict)), axis=1)
        # 计算填场数量
        df.eval('fill_seats = all_seats * fill_rate', inplace=True)
        df['fill_seats'] = df['fill_seats'].astype(int)
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
        df.to_excel(file_path, index=False)


if __name__ == '__main__':
    # DealData().deal_data(fill_rate_dict={"非黄金场":0.02, "黄金场":0.05}, file_path="/Users/laysuda/Desktop/allin/八角笼中0728.xlsx")
    DealData().get_cinemas_info(is_wanda=True)
    # pass
