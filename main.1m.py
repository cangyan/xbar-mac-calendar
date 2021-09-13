#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/bin/python3
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
import json


class Cal:
    def __init__(self, start="", end="", summary="", loc="", desc="") -> None:
        self.start = start
        self.end = end
        self.summary = summary
        self.loc = loc
        self.desc = desc



userHome = os.path.expanduser('~')

path = userHome+"/Library/Calendars"

icsList = glob.glob(path + "/**/*.ics", recursive=True)

i = 0

for fileName in icsList:
    cal = {}
    level = 0
    key = ""
    keyStack = []
    with open(fileName, "r") as f:
        for line in f:
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
            if len(l)>1:
                cal[key].update({l[0].strip():l[1].strip().rstrip("\n")})

    i += 1
    if (i > 2):
        break

    print(json.dumps(cal))
