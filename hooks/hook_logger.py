import sys
import datetime
from pathlib import Path

def log_call(agent_name="Unknown"):
    # 呼び出し時刻の取得
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')
    time_str = now.strftime('%H:%M:%S')

    # ログディレクトリの構築
    log_dir = Path.home() / '.agents' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f'{date_str}.log'

    # 実行ファイル名とコマンドライン引数の取得
    script_path = Path(sys.argv[0]).resolve()
    file_name = script_path.name
    args = sys.argv[1:]

    # 実行元のワークスペースのパス
    workspace_path = Path.cwd()

    # ログエントリの生成と追記
    log_line = f"[{time_str}] Agent: {agent_name} | File: {file_name} | Args: {args} | Workspace: {workspace_path}\n"
    
    with log_file.open('a', encoding='utf-8') as f:
        f.write(log_line)
