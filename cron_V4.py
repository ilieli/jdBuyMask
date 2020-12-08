# coding: utf-8

import datetime

from jdBuyMask_V4 import *
from scheduler import Scheduler


def main():
    # _setDNSCache()
    if len(skuids) != 1:
        logger.info('请准备一件商品')
    skuId = skuids[0]
    flag = 1
    while (1):
        try:
            # 初始化校验
            if flag == 1:
                logger.info('当前是V3版本')
                validate_cookies()
                getUsername()
                # select_all_cart_item()
                # remove_item()
                # add_item_to_cart(skuId)
            # 检测配置文件修改
            if int(time.time()) - configTime >= 60:
                check_Config()
            logger.info('第' + str(flag) + '次 ')
            flag += 1
            # 检查库存模块
            inStockSkuid = check_stock(checksession, skuids, area)  # inStockSkuid =[skuId]
            # 自动下单模块
            V4AutoBuy(skuId, inStockSkuid)
            # 休眠模块
            timesleep = random.randint(1, 3) / 10
            time.sleep(timesleep)
            # 校验是否还在登录模块
            if flag % 100 == 0:
                V4check(skuId)
        except Exception as e:
            print(traceback.format_exc())
            time.sleep(10)

if __name__ == "__main__":
    # main()

    scheduler = Scheduler(
        weekdays=[0, 1, 2, 3, 4, 5, 6],
        start_time=datetime.time(10, 59, 58, 0),
        end_time=datetime.time(11, 1, 0),
        run_child_process=main
    )

    scheduler.run_parent_process()