import sys
import logging
import datetime
from pathlib import Path

def _get_logger():
    # 呼び出し日付に応じたログファイルパスの生成
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')
    log_dir = Path.home() / '.agents' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f'{date_str}.log'

    # ロガーの初期化と取得
    logger = logging.getLogger("agent_hook")
    logger.setLevel(logging.INFO)

    # 重複登録防止のハンドラチェック
    if not logger.handlers:
        handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

def info(agent_name="Unknown"):
    # 呼び出し情報のフォーマットとロギング
    logger = _get_logger()
    script_path = Path(sys.argv[0]).resolve()
    file_name = script_path.name
    args = sys.argv[2:]
    workspace_path = Path.cwd()

    msg = f"Agent: {agent_name} | File: {file_name} | Args: {args} | Workspace: {workspace_path}"
    logger.info(msg)

def error(agent_name="Unknown", error_msg=""):
    # エラー情報のフォーマットとロギング
    logger = _get_logger()
    script_path = Path(sys.argv[0]).resolve()
    file_name = script_path.name

    msg = f"[ERROR] Agent: {agent_name} | File: {file_name} | Error: {error_msg}"
    logger.error(msg)



