#!/usr/bin/env PYTHONIOENCODING=UTF-8 TIME_ZONE='Asia/Shanghai' USE_TZ=True /usr/bin/python3
#
#  <xbar.title>mac日历提醒</xbar.title>
#  <xbar.version>v1.0</xbar.version>
#  <xbar.author>蒙德伊彼</xbar.author>
#  <xbar.author.github>git@github.com:cangyan/xbar-mac-calendar.git</xbar.author.github>
#  <xbar.desc>3天内日程提醒</xbar.desc>
#  <xbar.image></xbar.image>
#  <xbar.dependencies></xbar.dependencies>

import os
import glob
from datetime import date, datetime

days = 3
filterIcs = []


def formatSeconds(sec=0):
    h = sec // 3600
    hr = sec % 3600
    m = hr // 60
    sec = hr % 60

    s = ""
    if sec < 60 and m == 0 and h == 0:
        s = "不足1分钟"

    if m > 0:
        s = str(m)+"分"

    if h > 0:
        s = str(h)+"小时"+s

    return s


class Cal:
    def __init__(self, start: datetime = "", end: datetime = "", summary="", loc="", desc="") -> None:
        self.start = start
        self.end = end
        self.summary = summary
        self.loc = loc
        self.desc = desc

    # 获取状态 0.未开始 1.进行中 2.已结束 3.未开始非当日
    def get_status(self):
        now = datetime.today()
        if self.start > now:
            if self.start.day == now.day:
                return 0
            else:
                return 3
        else:
            if self.end < now:
                return 2
            else:
                return 1

    def to_display(self):
        status = self.get_status()
        if status == 0:
            print(":rocket: "+self.summary)
        if status == 1:
            print(":construction: "+self.summary)
        if status == 2:
            print(":white_check_mark: "+self.summary)
        if status == 3:
            print(":lock: "+self.summary)
        print("----")
        print("--简介:" + self.desc)
        print("--开始时间: " + self.start.__str__())
        print("--结束时间: " + self.end.__str__())


userHome = os.path.expanduser('~')

path = userHome+"/Library/Calendars"

icsList = glob.glob(path + "/**/*.ics", recursive=True)


formatFileList = []
calList = []

# 获取日历内容
for fileName in icsList:
    if len(filterIcs) > 0:
        filterRes = True
        for fs in filterIcs:
            if fs in fileName:
                filterRes = False
        if filterRes:
            continue

    cal = {}
    level = 0
    key = ""
    keyStack = []
    with open(fileName, "r") as f:
        for line in f:
            cal["file"] = fileName
            l = str.split(line, ":", 1)
            # print(l)
            if (l[0] == "BEGIN" and (l[1] == "VCALENDAR\n" or l[1] == "VEVENT\n" or l[1] == "VALARM\n")):
                level += 1
                keyStack.append(l[1].rstrip("\n"))
                key = keyStack[len(keyStack)-1]
                cal[key] = {}
                continue
            if (l[0] == "END" and (l[1] == "VCALENDAR\n" or l[1] == "VEVENT\n" or l[1] == "VALARM\n")):
                level -= 1
                keyStack.pop()
                if len(keyStack) > 0:
                    key = keyStack[len(keyStack)-1]
                continue
            # print(key, keyStack)

            if len(l) > 1:
                cal[key].update({l[0].strip(): l[1].strip().rstrip("\n")})
    if len(cal.keys()) > 0:
        formatFileList.append(cal)

# 格式化内容转对象Cal列表
for item in formatFileList:
    if len(item["VEVENT"].keys()) > 0:
        start = ""

        # 20190809T160000
        if "DTSTART;TZID=Asia/Shanghai" in item["VEVENT"]:
            start = datetime.strptime(
                item["VEVENT"]["DTSTART;TZID=Asia/Shanghai"], "%Y%m%dT%H%M%S")
        if "DTSTART;VALUE=DATE" in item["VEVENT"]:
            start = datetime.strptime(
                item["VEVENT"]["DTSTART;VALUE=DATE"], "%Y%m%d")

        if "DTEND;TZID=Asia/Shanghai" in item["VEVENT"]:
            end = datetime.strptime(
                item["VEVENT"]["DTEND;TZID=Asia/Shanghai"], "%Y%m%dT%H%M%S")
        if "DTEND;VALUE=DATE" in item["VEVENT"]:
            end = datetime.strptime(
                item["VEVENT"]["DTEND;VALUE=DATE"], "%Y%m%d")

        summary = ""
        if "SUMMARY" in item["VEVENT"]:
            summary = item["VEVENT"]["SUMMARY"]
        if "SUMMARY;LANGUAGE=zh_CN" in item["VEVENT"]:
            summary = item["VEVENT"]["SUMMARY;LANGUAGE=zh_CN"]

        loc = ""
        if "LOCATION" in item["VEVENT"]:
            loc = item["VEVENT"]["LOCATION"]

        desc = ""
        if "DESCRIPTION" in item["VEVENT"]:
            desc = item["VEVENT"]["DESCRIPTION"]

        today = datetime.today()
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)

        diff = start - today
        if diff.days >= 0 and diff.days <= days:
            # print(item["file"])
            c = Cal(start, end, summary, loc, desc)
            calList.append(c)

# 输出到xbar
preTips = ""
futureTips = ""
todayCount = 0
futureCount = 0
todayFinishCount = 0
todayList = []
futureList = []
for item in calList:
    status = item.get_status()

    if status == 0:
        if preTips == "":
            # 还有多久开始
            now = datetime.now()
            diff = item.start - now

            preTips = ":rocket: 还有" + \
                formatSeconds(diff.seconds) + "开始: "+item.summary
        todayList.append(item)

    if status == 1:
        if preTips == "":
            # 还有多久结束
            preTips = ":construction: 还有" + \
                formatSeconds(diff.seconds) + "结束: "+item.summary
        todayList.append(item)

    if status == 2:
        todayFinishCount += 1
        todayList.append(item)

    if status == 3:
        futureCount += 1
        futureList.append(item)


preShow = False
if preTips == "":
    preShow = True
    preTips = ":coffee: 今天无日程安排"
    if todayFinishCount > 0:
        preTips = ":tada: 今天日程已完结"

if len(futureList) == 0:
    futureTips = ":coffee: 未来无日程安排"

if len(futureList) > 0:
    futureTips = ":pencil: 未来"+str(days)+"天有"+str(len(futureList))+"个日程待办"

print(preTips + "| size=14 ")
print("---")
if preShow:
    print(preTips)
for item in todayList:
    item.to_display()

print("---")
print(futureTips + "| size=14")
for item in futureList:
    item.to_display()
