# coding: utf-8
# PyQuanTrade
#
# Copyright 2011-2019 Chris Bin Hu (porfavor)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Chris Bin Hu (porfavor) <chris.hu.cohen@gmail.com>
"""

import datetime
import time
import multiprocessing


class Scheduler(object):

    def __init__(self, weekdays, start_time, end_time, run_child_process):
        self.weekdays = weekdays
        self.start_time = start_time
        self.end_time = end_time
        self.run_child_process = run_child_process

    def run_parent_process(self):
        print(u'启动守护父进程')

        p = None  # 子进程句柄

        while True:
            currentTime = datetime.datetime.now().time()
            recording = False

            # # 判断当前处于的时间段
            # if ((currentTime >= DAY_START and currentTime <= DAY_END) or
            #     (currentTime >= NIGHT_START) or
            #     (currentTime <= NIGHT_END)):
            #     recording = True
            #
            # # 过滤周末时间段：周六全天，周五夜盘，周日日盘
            # if ((datetime.today().weekday() == 6) or
            #     (datetime.today().weekday() == 5 and currentTime > NIGHT_END) or
            #     (datetime.today().weekday() == 0 and currentTime < DAY_START)):
            #     recording = False

            if datetime.datetime.today().weekday() in self.weekdays and (
                    self.start_time < currentTime < self.end_time
                    or (
                            self.start_time > self.end_time and (
                                    self.start_time < currentTime
                                    or currentTime < self.end_time
                            )
                    )
            ):
                recording = True
            else:
                recording = False

            # 记录时间则需要启动子进程
            if recording and p is None:
                print(u'启动子进程')
                p = multiprocessing.Process(target=self.run_child_process)
                p.start()
                print(u'子进程启动成功')

            # 非记录时间则退出子进程
            if not recording and p is not None:
                print(u'关闭子进程')
                p.terminate()
                p.join()
                p = None
                print(u'子进程关闭成功')

            time.sleep(0.5)

    def run_parent_process_every_x_mins(self, mins):
        print(u'启动守护父进程')

        p = None  # 子进程句柄

        process_start_time = None

        while True:
            currentTime = datetime.datetime.now().time()
            recording = False

            # # 判断当前处于的时间段
            # if ((currentTime >= DAY_START and currentTime <= DAY_END) or
            #     (currentTime >= NIGHT_START) or
            #     (currentTime <= NIGHT_END)):
            #     recording = True
            #
            # # 过滤周末时间段：周六全天，周五夜盘，周日日盘
            # if ((datetime.today().weekday() == 6) or
            #     (datetime.today().weekday() == 5 and currentTime > NIGHT_END) or
            #     (datetime.today().weekday() == 0 and currentTime < DAY_START)):
            #     recording = False

            if datetime.datetime.today().weekday() in self.weekdays and (
                    self.start_time < currentTime < self.end_time
                    or (
                            self.start_time > self.end_time and (
                                    self.start_time < currentTime < datetime.time(23, 59, 59, 999)
                                    or datetime.time(0, 0, 0, 0) < currentTime < self.end_time
                            )
                    )
            ):
                recording = True

                if process_start_time is not None \
                        and datetime.datetime.now() > process_start_time + datetime.timedelta(minutes=mins):
                    recording = False
            else:
                recording = False

            # 记录时间则需要启动子进程
            if recording and p is None:
                print(u'启动子进程')
                process_start_time = datetime.datetime.now()

                p = multiprocessing.Process(target=self.run_child_process)
                p.start()
                print(u'子进程启动成功')

            # 非记录时间则退出子进程
            if not recording and p is not None:
                print(u'关闭子进程')
                p.terminate()
                p.join()
                p = None
                process_start_time = None
                print(u'子进程关闭成功')

            time.sleep(10)