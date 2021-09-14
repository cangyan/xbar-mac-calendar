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
from datetime import datetime


class Cal:
    def __init__(self, start="", end="", summary="", loc="", desc="") -> None:
        self.start = start
        self.end = end
        self.summary = summary
        self.loc = loc
        self.desc = desc

    def to_display(self):
        print(self.summary, self.start, self.end)


userHome = os.path.expanduser('~')

path = userHome+"/Library/Calendars"

icsList = glob.glob(path + "/**/*.ics", recursive=True)

days = 10
calList = []

for fileName in icsList:
    cal = {}
    level = 0
    key = ""
    keyStack = []
    with open(fileName, "r") as f:
        for line in f:
            cal["file"] = fileName
            l = str.split(line, ":")
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
        calList.append(cal)

for item in calList:
    if len(item["VEVENT"].keys()) > 0:
        start = ""
        # 过滤条目
        if "TRANSP" in item["VEVENT"]:
            if item["VEVENT"]["TRANSP"] != "OPAQUE":
                continue
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

        loc = ""
        if "LOCATION" in item["VEVENT"]:
            loc = item["VEVENT"]["LOCATION"]

        desc = ""
        if "DESCRIPTION" in item["VEVENT"]:
            desc = item["VEVENT"]["DESCRIPTION"]

        today = datetime.today()

        diff = start - today
        if diff.days >= 0 and diff.days < days:
            # print(item["file"])
            c = Cal(start, end, summary, loc, desc)
            c.to_display()
