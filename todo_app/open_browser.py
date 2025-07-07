import webbrowser
import time
import os

def open_web_browser(url, delay=1):
    time.sleep(delay)  # サーバー起動を少し待つ
    webbrowser.open_new_tab(url)

if __name__ == "__main__":
    target_url = "http://localhost:8001/login/"
    open_web_browser(target_url)