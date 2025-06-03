# 勤怠システムの出社を自動化する
2025年現在、配属先の現場の勤怠処理は"勤怠システム"を使用して勤怠を行っている。
出勤時に、勤怠システムのURLから開いて"9:00"と毎回決まった時間を入力するのが面倒だと思ったため、朝の出社の勤怠入力をPythonのSeleniumを使用して自動化をしました。

## 仕様
ターミナルから`attend`と入力すると、`run_attendance.sh`が起動し `attenance.py`を叩いて、勤怠処理の自動入力が始まります。
`~/.bashrc`に`alias attend='python ~/python/attendance.py'`を設定し、コマンド入力も最小限にしました。

スクリプト内容は以下
```bash
#!/bin/bash

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# Pythonスクリプト実行
python attendance.py

```

