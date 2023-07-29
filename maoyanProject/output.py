from os.path import dirname

import pandas as pd

import maoyanProject.files

FilePath = dirname(maoyanProject.files.__file__)


def output_excel(file_path):
    # 数据导出本地路径
    df = pd.read_csv(f"{FilePath}/allin.csv")
    try:
        df = df.drop(df[df['movie'] == 'movie'].index)
    except:
        pass
    df.drop_duplicates(keep='first', inplace=True)
    # 排序
    df.sort_values(by=['city_name', 'cinema_name', 'begin_time'], inplace=True)
    df.rename(columns={
        'movie': '电影名',
        'owner': '负责人',
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
    owner_list = df['负责人'].tolist()
    for i in owner_list:
        df_to = df[df['负责人'] == i]
        df_to.to_excel(f'{file_path}/{i}.xlsx', index=False)


if __name__ == '__main__':
    # 导出到本地的文件夹路径
    file_path = "/Users/laysuda/Desktop/allin/0729/"
    output_excel(file_path)
