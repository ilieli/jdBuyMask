# -*- coding=utf-8 -*-
from jdlogger import logger

'''
测试 https://c0.3.cn/stock?skuId=100003406321&area=19_1607_4773_0&venderId=1000000946&buyNum=1&choseSuitSkuIds=&cat=9192,9197,12588&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_7c3992aa27d1a&pduid=1580535906442142991701&ch=1&callback=jQuery4291064
请看教程寻找自己的url
'''
url = 'https://c0.3.cn/stocks?callback=jQuery4030577&type=getstocks&skuIds=100015062706%2C100008433193%2C100015062658%2C100015589498%2C100015589488%2C100008783967%2C100015589490%2C100016723174%2C100016723154%2C100016827390%2C100002138879%2C100008520909%2C100015193936%2C100009390612%2C100006897879%2C100009489869&area=22_1930_49324_0&_=1606931097846'
skuId = url.split('skuId=')[1].split('&')[0]
area = url.split('area=')[1].split('&')[0]
logger.info('你的area是[ %s ]，链接的商品id是[ %s ]', area, skuId)
