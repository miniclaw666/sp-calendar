"""
飞书日程同步脚本
将飞书日程导出为 .ics 格式
"""

import json
import os
from datetime import datetime, timedelta
from ics import Calendar, Event
import requests

# 从环境变量获取配置
FEISHU_TOKEN = os.environ.get("FEISHU_TOKEN", "")
FEISHU_OPEN_ID = os.environ.get("FEISHU_OPEN_ID", "")
CALENDAR_ID = os.environ.get("CALENDAR_ID", "primary")  # 默认主日历

def get_feishu_events():
    """获取飞书日程"""
    if not FEISHU_TOKEN:
        print("错误: 未设置 FEISHU_TOKEN 环境变量")
        return []
    
    # 获取当前时间往前30天往后60天的日程
    now = datetime.now()
    start_time = (now - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    end_time = (now + timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    
    url = "https://open.feishu.cn/open-apis/calendar/v4/calendars/{}/events".format(CALENDAR_ID)
    headers = {
        "Authorization": f"Bearer {FEISHU_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "start_time": start_time,
        "end_time": end_time,
        "max_results": 500
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if data.get("code") == 0:
            return data.get("data", {}).get("items", [])
        else:
            print(f"获取日程失败: {data.get('msg')}")
            return []
    except Exception as e:
        print(f"请求错误: {e}")
        return []

def convert_to_ics(events):
    """将飞书日程转换为 ICS 格式"""
    c = Calendar()
    c.name = "飞书日程"
    c.description = "从飞书同步的日程"
    
    for event in events:
        e = Event()
        e.name = event.get("summary", "无标题")
        e.description = event.get("description", "")
        
        # 处理开始和结束时间
        start = event.get("start", {})
        end = event.get("end", {})
        
        if start.get("date_time") and end.get("date_time"):
            e.begin = start["date_time"].replace("+08:00", "")
            e.end = end["date_time"].replace("+08:00", "")
        
        # 添加唯一ID
        e.uid = event.get("event_id", "")
        
        c.events.add(e)
    
    return c

def main():
    print("开始同步飞书日程...")
    
    events = get_feishu_events()
    print(f"获取到 {len(events)} 个日程")
    
    if events:
        calendar = convert_to_ics(events)
        
        # 保存 .ics 文件
        output_file = "calendar.ics"
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(calendar.serialize_iter())
        
        print(f"已生成 {output_file}")
        
        # 输出调试信息
        print("\n前5个日程预览:")
        for event in events[:5]:
            print(f"  - {event.get('summary')} | {event.get('start', {}).get('date_time', 'N/A')}")
    else:
        # 创建空日历
        c = Calendar()
        c.name = "飞书日程"
        with open("calendar.ics", "w", encoding="utf-8") as f:
            f.writelines(c.serialize_iter())
        print("未获取到日程，已创建空白日历文件")

if __name__ == "__main__":
    main()
