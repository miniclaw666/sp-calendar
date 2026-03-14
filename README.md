# 飞书日程同步

自动从飞书抓取日程并生成 .ics 日历文件，可订阅到苹果日历/Google Calendar等。

## 使用方法

1. Fork 此仓库或手动创建
2. 在 GitHub Secrets 中添加以下变量：
   - `FEISHU_OPEN_ID`: 你的飞书 Open ID
   - `FEISHU_TOKEN`: 飞书开放平台 access_token（需调用通讯录权限）
3. 开启 GitHub Actions
4. 访问 GitHub Pages 获取 .ics 订阅地址

## 订阅地址

```
https://你的用户名.github.io/feishu-calendar/calendar.ics
```

## 自动同步

- 每天自动执行
- 也可手动触发：进入 Actions → Sync Feishu Calendar → Run workflow

## 本地运行

```bash
pip install requests ics
python sync_calendar.py
```
