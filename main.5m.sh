#!/usr/bin/env bash
#
#  <xbar.title>mac日历提醒</xbar.title>
#  <xbar.version>v1.0</xbar.version>
#  <xbar.author>蒙德伊彼</xbar.author>
#  <xbar.author.github>git@github.com:cangyan/xbar-mac-calendar.git</xbar.author.github>
#  <xbar.desc>3天内日程提醒</xbar.desc>
#  <xbar.image></xbar.image>
#  <xbar.dependencies></xbar.dependencies>

export PATH="/usr/local/bin:$PATH"





todayNoEventMessage=":tada: 今日无日程安排!!!"


# 常量定义 今日 & 未来2天
today=`date "+%Y%m%d"`

# 查找符合日期的行程
icsList=$(find ~/Library/Calendars -name "*.ics")

showIcsList=()
todayList=()

echo "---"
for icsFile in ${icsList}
do
    file=$(cat $icsFile | awk -v FS=':' -v today="${today}" -v file="${icsFile}" '{if (substr($1,0,7)=="DTSTART"&&substr($2,0,8)==today)   print file}')
    if [ ! -z "$file" -a "$file" != " " ]; then
      #   cat $file
      echo "$(cat $file| grep -e "DESCRIPTION") | color=purple"
    fi
done

# 抽取数据