import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser
import sys
import win32api
import re

class Updater:
    def __init__(self, master):
        self.master = master
        self.current_version = self.get_current_version()
        self.github_raw_url = "https://raw.githubusercontent.com/keitannunes/KeifunsDatatableEditor/main/version_info.txt"
        self.github_releases_url = "https://github.com/keitannunes/KeifunsDatatableEditor/releases"

    def get_current_version(self):
        try:
            if getattr(sys, 'frozen', False):
                # The application is frozen (compiled)
                executable_path = sys.executable
            else:
                # The application is not frozen (running from script)
                executable_path = __file__

            info = win32api.GetFileVersionInfo(executable_path, "\\")
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            return f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}"
        except:
            return "0.1.0"  # Fallback version if unable to read from executable

    def check_for_updates(self):
        try:
            response = requests.get(self.github_raw_url)
            if response.status_code == 200:
                content = response.text
                latest_version = self.extract_version_from_content(content)
                if latest_version and self.is_version_greater(latest_version, self.current_version):
                    self.show_update_popup(latest_version)
                    return True
            else:
                print(f"Failed to fetch version info. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error checking for updates: {e}")
        return False

    def extract_version_from_content(self, content):
        match = re.search(r'filevers=\((\d+),\s*(\d+),\s*(\d+),\s*\d+\)', content)
        if match:
            return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
        return None

    def is_version_greater(self, v1, v2):
        return tuple(map(int, v1.split('.'))) > tuple(map(int, v2.split('.')))

    def show_update_popup(self, latest_version):
        root = tk.Toplevel(self.master)
        root.withdraw()  # Hide the main window

        message = f"A new version is available!\n\n" \
                  f"Current version: {self.current_version}\n" \
                  f"Latest version: {latest_version}\n\n" \
                  f"Do you want to update?"

        result = messagebox.askyesno("Update Available", message)
        if result:
            webbrowser.open(self.github_releases_url)

        root.destroy()  # Clean up the hidden root window