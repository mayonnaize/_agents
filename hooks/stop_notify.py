import sys
import json
import subprocess
import os
import hook_logger

# クロスプラットフォーム対応のための条件付きインポート
if os.name == 'nt':
    import ctypes
    from ctypes import wintypes

def _get_foreground_pid():
    # 最前面ウィンドウのハンドル取得
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    if not hwnd:
        return None
        
    # 最前面ウィンドウのプロセスID取得
    fg_pid = wintypes.DWORD()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(fg_pid))
    return fg_pid.value

def _get_ancestor_pids(target_pid):
    # プロセス情報の構造体定義
    class PROCESSENTRY32(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD),
                    ("cntUsage", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD),
                    ("th32DefaultHeapID", ctypes.POINTER(wintypes.ULONG)),
                    ("th32ModuleID", wintypes.DWORD),
                    ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD),
                    ("pcPriClassBase", wintypes.LONG),
                    ("dwFlags", wintypes.DWORD),
                    ("szExeFile", ctypes.c_char * 260)]

    TH32CS_SNAPPROCESS = 0x00000002
    kernel32 = ctypes.windll.kernel32
    
    # システム全体のプロセススナップショット取得
    hProcessSnap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if hProcessSnap == -1:
        return set()
        
    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    
    # 全プロセスの親子関係マップ構築
    parent_map = {}
    if kernel32.Process32First(hProcessSnap, ctypes.byref(pe32)):
        while True:
            exe_name = pe32.szExeFile.decode('utf-8', 'ignore').lower()
            parent_map[pe32.th32ProcessID] = (pe32.th32ParentProcessID, exe_name)
            if not kernel32.Process32Next(hProcessSnap, ctypes.byref(pe32)):
                break
                
    # ハンドルの解放
    kernel32.CloseHandle(hProcessSnap)
    
    # 自身の親プロセス群の探索
    ancestors = set()
    current = target_pid
    while current in parent_map:
        parent_id, current_exe = parent_map[current]
        
        # デスクトップやタスクバーへのフォーカスを誤検知しないよう、explorer.exe は親ツリーから除外
        if current_exe == 'explorer.exe':
            ancestors.discard(current)
            break
            
        if parent_id == 0 or parent_id in ancestors:
            break
            
        ancestors.add(parent_id)
        current = parent_id
        
    return ancestors

def is_focused():
    # 非Windows環境での判定スキップ
    if os.name != 'nt':
        return False

    # 最前面プロセスのID取得
    fg_pid = _get_foreground_pid()
    if not fg_pid:
        return False
        
    # 自身のプロセスIDとの直接照合
    my_pid = os.getpid()
    if fg_pid == my_pid:
        return True

    # 自身の親プロセス群の取得と照合結果の返却
    ancestors = _get_ancestor_pids(my_pid)
    return (fg_pid in ancestors)

def _show_popup():
    # tkinterによる通知用コード
    popup_code = """
import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)
messagebox.showinfo('Antigravity', 'エージェントの作業が完了しました。')
"""
    # サブプロセスの入出力無効化
    kwargs = {
        'stdin': subprocess.DEVNULL,
        'stdout': subprocess.DEVNULL,
        'stderr': subprocess.DEVNULL,
    }
    
    # コンソールウィンドウの非表示設定
    if os.name == 'nt':
        kwargs['creationflags'] = 0x08000000
    else:
        kwargs['start_new_session'] = True

    # バックグラウンドでの通知プロセス起動
    subprocess.Popen([sys.executable, '-c', popup_code], **kwargs)

def main():
    # 実行ログの記録
    hook_logger.log_call()

    # 標準入力からのコンテキスト情報の破棄
    if not sys.stdin.isatty():
        sys.stdin.read()

    # 非アクティブ時のみの通知実行
    if not is_focused():
        _show_popup()

    # 規定の空JSON出力によるエージェントの正常停止許可
    print(json.dumps({}))

if __name__ == "__main__":
    main()
