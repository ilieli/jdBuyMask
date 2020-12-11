# coding: utf-8

import datetime

from jdBuyMask_V4 import *
from scheduler import Scheduler


event_time = datetime.datetime(2020, 12, 12, 0, 0, 0)
timesleep = 100 / 1000
start_time=datetime.time(23, 59, 55, 0)
end_time=datetime.time(1, 0, 0)

# 华硕 ASUS TUF-RTX3080-O10G-GAMING 1440-1815MHz 5499
skuid = '100015285144'


def main():
    # _setDNSCache()
    # if len(skuids) != 1:
    #     logger.info('请准备一件商品')
    # skuid = skuids[0]
    flag = 1
    while (1):
        try:
            # 初始化校验
            if flag == 1:
                logger.info('当前是V3版本, 抢购商品: %s' % skuid)
                validate_cookies()
                getUsername()
                # select_all_cart_item()
                # remove_item()
                # add_item_to_cart(skuid)
            # 检测配置文件修改
            if int(time.time()) - configTime >= 60:
                check_Config()
            logger.info('第' + str(flag) + '次 ')
            flag += 1
            # 检查库存模块
            inStockSkuid = check_stock(checksession, [skuid], area)  # inStockSkuid =[skuid]

            while datetime.datetime.now() < event_time:
                print('等待抢购[%s]...' % skuid)
                time.sleep(timesleep)
                continue

            # 自动下单模块
            success = V4AutoBuy(skuid, inStockSkuid)
            if success:
                break

            # 休眠模块
            # timesleep = random.randint(1, 3) / 10
            time.sleep(timesleep)
            # 校验是否还在登录模块
            if flag % 100 == 0:
                V4check(skuid)
        except Exception as e:
            print(traceback.format_exc())
            time.sleep(10)


if __name__ == "__main__":
    # main()

    scheduler = Scheduler(
        weekdays=[0, 1, 2, 3, 4, 5, 6],
        start_time=start_time,
        end_time=end_time,
        run_child_process=main
    )

    scheduler.run_parent_process()