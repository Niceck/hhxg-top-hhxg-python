# 定时获取 A 股日报

数据每个交易日盘后约 20:00 更新。可通过以下方式定时获取。

## macOS launchd（推荐）

### 1. 创建 plist

```bash
cat > ~/Library/LaunchAgents/com.hhxg.snapshot.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hhxg.snapshot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/.claude/skills/hhxg-market/scripts/fetch_snapshot.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>20</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/hhxg-snapshot.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/hhxg-snapshot-err.log</string>
</dict>
</plist>
PLIST
```

> 注意：将 `YOUR_USERNAME` 替换为你的用户名。

### 2. 加载定时任务

```bash
launchctl load ~/Library/LaunchAgents/com.hhxg.snapshot.plist
```

### 3. 卸载

```bash
launchctl unload ~/Library/LaunchAgents/com.hhxg.snapshot.plist
```

## cron 方式

```bash
# 每天 20:00 执行
crontab -e
# 添加以下行:
0 20 * * * /usr/bin/python3 ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py > /tmp/hhxg-snapshot.log 2>&1
```

## 手动获取

随时运行脚本即可获取最新数据：

```bash
python3 ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py
```

或在 Claude Code 中直接问：
- "今天 A 股怎么样"
- "获取最新日报"
- "/hhxg-market"
