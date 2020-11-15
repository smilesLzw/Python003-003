# _*_ coding: utf-8 _*_
# @Author: smiles
# @Time  : 2020/11/14 23:43
# @File  : data_process.py

import json

import pymysql
import pandas as pd
from snownlp import SnowNLP


def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


def sava_to_mysql(df_data):
    conn = pymysql.connect(config['host'], config['user'], config['password'], config['db'])
    sql = "INSERT INTO index_comment (nickname, comment, sentiment, comment_time) VALUES (%s, %s, %s, %s)"
    try:
        with conn.cursor() as cur:
            for data in df_data.itertuples():
                s = SnowNLP(getattr(data, 'comment'))
                sentiment = s.sentiments
                cur.execute(sql, (getattr(data, 'nickname'), getattr(data, 'comment'), sentiment, getattr(data, 'comment_time')))
        conn.commit()
    finally:
        conn.close()


def read_data():
    conn = pymysql.connect(config['host'], config['user'], config['password'], config['db'])
    sql = "SELECT * FROM phone_comment"
    df = pd.read_sql(sql, conn)
    conn.close()
    return clean_data(df)


def clean_data(data):
    # 清除空数据
    df1 = data.drop(data[data['comment'] == ''].index)
    # 清除重复的数据
    df2 = df1.drop_duplicates(subset=['comment'])
    return df2


if __name__ == '__main__':
    config = load_config()
    df = read_data()
    sava_to_mysql(df)

