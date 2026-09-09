import sys, os, socket, winreg, subprocess, requests, re

def ensure_single_instance():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', 54321))
        sock.listen(1)
        return True
    except OSError:
        return False

def set_autostart(enabled):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE)
        if enabled:
            exe_path = sys.argv[0]
            winreg.SetValueEx(key, "NeteaseTimer", 0, winreg.REG_SZ, f'"{exe_path}" --minimized')
        else:
            try:
                winreg.DeleteValue(key, "NeteaseTimer")
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Autostart error: {e}")

def is_network_available():
    try:
        requests.get("https://music.163.com", timeout=3)
        return True
    except:
        return False

def parse_share_link(url):
    patterns = [
        r'playlist/(\d+)',
        r'song\?id=(\d+)',
        r'album\?id=(\d+)'
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None
