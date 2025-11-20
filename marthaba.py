#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import json
import os
import time
import threading
import subprocess
import re

CONFIG_FILE = os.path.expanduser("~/.marthaba_config.json")
DEFAULT_BLOCKED_SITES = {
    "youtube.com": ["/shorts", "/reel"],
    "facebook.com": ["/reel", "/watch"],
    "instagram.com": ["/reels"]
}

class MarThabaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MarThaba - Productivity Guard")
        self.root.geometry("750x700")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        self.config = self.load_config()
        self.setup_ui()
        self.check_block_status()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        title_label = tk.Label(header_frame, text="MarThaba", font=('Arial', 24, 'bold'), fg='#ecf0f1', bg='#34495e')
        title_label.pack(pady=20)
        
        # Main Content
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Theme Selection
        theme_frame = tk.Frame(main_frame, bg='#2c3e50')
        theme_frame.pack(fill=tk.X, pady=10)
        tk.Label(theme_frame, text="Select Theme:", font=('Arial', 12), fg='white', bg='#2c3e50').pack(side=tk.LEFT)
        self.theme_var = tk.StringVar(value=self.config.get('theme', 'dark'))
        themes = [('Dark', 'dark'), ('Light', 'light'), ('Blue', 'blue')]
        for text, mode in themes:
            tk.Radiobutton(theme_frame, text=text, variable=self.theme_var, value=mode, command=self.change_theme, fg='white', bg='#2c3e50', selectcolor='black').pack(side=tk.LEFT, padx=10)
        
        # Block Duration
        duration_frame = tk.Frame(main_frame, bg='#2c3e50')
        duration_frame.pack(fill=tk.X, pady=15)
        tk.Label(duration_frame, text="Block Duration (Days):", font=('Arial', 12), fg='white', bg='#2c3e50').pack()
        self.duration_var = tk.StringVar(value=str(self.config.get('duration', 7)))
        duration_combo = ttk.Combobox(duration_frame, textvariable=self.duration_var, values=[7, 10, 15, 30, 60], state="readonly")
        duration_combo.pack(pady=5)
        
        # YouTube Channels
        channels_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        channels_frame.pack(fill=tk.X, pady=10)
        tk.Label(channels_frame, text="🎬 Allowed YouTube Channels", font=('Arial', 12, 'bold'), fg='white', bg='#34495e').pack(pady=5)
        listbox_frame = tk.Frame(channels_frame, bg='#34495e')
        listbox_frame.pack(fill=tk.X, padx=10, pady=5)
        self.channels_listbox = tk.Listbox(listbox_frame, height=3, font=('Arial', 9))
        self.channels_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.channels_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.channels_listbox.config(yscrollcommand=scrollbar.set)
        channels_btn_frame = tk.Frame(channels_frame, bg='#34495e')
        channels_btn_frame.pack(pady=5)
        add_btn = tk.Button(channels_btn_frame, text="Add Channel", font=('Arial', 9), bg='#27ae60', fg='white', command=self.add_channel)
        add_btn.pack(side=tk.LEFT, padx=3)
        remove_btn = tk.Button(channels_btn_frame, text="Remove Selected", font=('Arial', 9), bg='#c0392b', fg='white', command=self.remove_channel)
        remove_btn.pack(side=tk.LEFT, padx=3)
        
        # Custom Sites
        sites_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        sites_frame.pack(fill=tk.X, pady=10)
        tk.Label(sites_frame, text="🌐 Custom Blocked Websites", font=('Arial', 12, 'bold'), fg='white', bg='#34495e').pack(pady=5)
        sites_listbox_frame = tk.Frame(sites_frame, bg='#34495e')
        sites_listbox_frame.pack(fill=tk.X, padx=10, pady=5)
        self.sites_listbox = tk.Listbox(sites_listbox_frame, height=3, font=('Arial', 9))
        self.sites_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sites_scrollbar = tk.Scrollbar(sites_listbox_frame, orient=tk.VERTICAL)
        sites_scrollbar.config(command=self.sites_listbox.yview)
        sites_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sites_listbox.config(yscrollcommand=sites_scrollbar.set)
        sites_btn_frame = tk.Frame(sites_frame, bg='#34495e')
        sites_btn_frame.pack(pady=5)
        add_site_btn = tk.Button(sites_btn_frame, text="Add Website", font=('Arial', 9), bg='#e67e22', fg='white', command=self.add_custom_site)
        add_site_btn.pack(side=tk.LEFT, padx=3)
        remove_site_btn = tk.Button(sites_btn_frame, text="Remove Selected", font=('Arial', 9), bg='#c0392b', fg='white', command=self.remove_custom_site)
        remove_site_btn.pack(side=tk.LEFT, padx=3)
        default_sites_label = tk.Label(sites_frame, text="Default: YouTube Shorts, Facebook/Instagram Reels", font=('Arial', 8), fg='#bdc3c7', bg='#34495e')
        default_sites_label.pack(pady=2)
        
        # Status Display
        self.status_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        self.status_frame.pack(fill=tk.X, pady=15)
        self.status_label = tk.Label(self.status_frame, text="", font=('Arial', 12), fg='white', bg='#34495e', wraplength=700)
        self.status_label.pack(pady=10)
        
        # Control Buttons
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        self.start_btn = tk.Button(button_frame, text="Start Blocking", font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white', relief=tk.RAISED, bd=3, command=self.start_blocking, width=15, height=2)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        self.reset_btn = tk.Button(button_frame, text="Emergency Reset", font=('Arial', 10), bg='#f39c12', fg='white', command=self.emergency_reset)
        
        dev_label = tk.Label(main_frame, text="Developer: Arafat Rahman", font=('Arial', 10), fg='#bdc3c7', bg='#2c3e50')
        dev_label.pack(side=tk.BOTTOM, pady=10)
        
        self.load_channels_list()
        self.load_custom_sites_list()
    
    def load_channels_list(self):
        self.channels_listbox.delete(0, tk.END)
        channels = self.config.get('allowed_channels', [])
        for channel in channels:
            self.channels_listbox.insert(tk.END, channel)
    
    def load_custom_sites_list(self):
        self.sites_listbox.delete(0, tk.END)
        custom_sites = self.config.get('custom_sites', {})
        for site, paths in custom_sites.items():
            if paths:
                self.sites_listbox.insert(tk.END, f"{site} {paths}")
            else:
                self.sites_listbox.insert(tk.END, site)
    
    def add_channel(self):
        if self.config.get('active', False):
            messagebox.showwarning("Not Available", "Channel editing disabled while blocking active.")
            return
        channel_url = simpledialog.askstring("Add YouTube Channel", "Enter YouTube Channel URL:")
        if channel_url:
            channel_id = self.extract_channel_id(channel_url)
            if channel_id:
                channels = self.config.get('allowed_channels', [])
                if channel_id not in channels:
                    channels.append(channel_id)
                    self.config['allowed_channels'] = channels
                    self.save_config()
                    self.load_channels_list()
                    messagebox.showinfo("Success", f"Channel added: {channel_id}")
    
    def add_custom_site(self):
        if self.config.get('active', False):
            messagebox.showwarning("Not Available", "Website editing disabled while blocking active.")
            return
        website = simpledialog.askstring("Add Website to Block", "Enter website domain:")
        if website:
            website = website.lower().strip()
            website = website.replace('https://', '').replace('http://', '').replace('www.', '')
            if website:
                custom_sites = self.config.get('custom_sites', {})
                if website not in custom_sites:
                    custom_sites[website] = []
                    self.config['custom_sites'] = custom_sites
                    self.save_config()
                    self.load_custom_sites_list()
                    messagebox.showinfo("Success", f"Website added: {website}")
    
    def remove_channel(self):
        if self.config.get('active', False):
            messagebox.showwarning("Not Available", "Channel editing disabled while blocking active.")
            return
        selection = self.channels_listbox.curselection()
        if selection:
            channel = self.channels_listbox.get(selection[0])
            channels = self.config.get('allowed_channels', [])
            if channel in channels:
                channels.remove(channel)
                self.config['allowed_channels'] = channels
                self.save_config()
                self.load_channels_list()
    
    def remove_custom_site(self):
        if self.config.get('active', False):
            messagebox.showwarning("Not Available", "Website editing disabled while blocking active.")
            return
        selection = self.sites_listbox.curselection()
        if selection:
            site_entry = self.sites_listbox.get(selection[0])
            site_name = site_entry.split(' ')[0]
            custom_sites = self.config.get('custom_sites', {})
            if site_name in custom_sites:
                del custom_sites[site_name]
                self.config['custom_sites'] = custom_sites
                self.save_config()
                self.load_custom_sites_list()
    
    def extract_channel_id(self, url):
        patterns = [
            r'youtube\.com/@([a-zA-Z0-9_-]+)',
            r'youtube\.com/c/([a-zA-Z0-9_-]+)',
            r'youtube\.com/channel/([a-zA-Z0-9_-]+)',
            r'youtube\.com/user/([a-zA-Z0-9_-]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def change_theme(self):
        theme = self.theme_var.get()
        self.config['theme'] = theme
        self.save_config()
    
    def load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                if 'allowed_channels' not in config:
                    config['allowed_channels'] = []
                if 'custom_sites' not in config:
                    config['custom_sites'] = {}
                return config
        except:
            return {'active': False, 'end_time': None, 'duration': 7, 'theme': 'dark', 'allowed_channels': [], 'custom_sites': {}}
    
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f)
    
    def get_all_blocked_sites(self):
        all_sites = DEFAULT_BLOCKED_SITES.copy()
        custom_sites = self.config.get('custom_sites', {})
        for site, paths in custom_sites.items():
            all_sites[site] = paths
        return all_sites
    
    def start_blocking(self):
        duration = int(self.duration_var.get())
        end_time = datetime.datetime.now() + datetime.timedelta(days=duration)
        self.config.update({
            'active': True,
            'start_time': datetime.datetime.now().isoformat(),
            'end_time': end_time.isoformat(),
            'duration': duration
        })
        self.save_config()
        threading.Thread(target=self.block_sites, daemon=True).start()
        channels_count = len(self.config.get('allowed_channels', []))
        custom_sites_count = len(self.config.get('custom_sites', {}))
        messagebox.showinfo("Success", f"Blocking activated for {duration} days!")
        self.check_block_status()
        self.start_btn.config(state=tk.DISABLED, bg='#95a5a6')
    
    def block_sites(self):
        hosts_file = "/etc/hosts"
        redirect_ip = "127.0.0.1"
        while self.config.get('active', False):
            end_time = datetime.datetime.fromisoformat(self.config['end_time'])
            if datetime.datetime.now() > end_time:
                self.config['active'] = False
                self.save_config()
                break
            try:
                subprocess.run(['sudo', 'sed', '-i', '/# MarThaba Block/d', hosts_file], capture_output=True)
                all_sites = self.get_all_blocked_sites()
                block_entries = []
                for site, paths in all_sites.items():
                    block_entries.append(f"{redirect_ip} {site}")
                    block_entries.append(f"{redirect_ip} www.{site}")
                    for path in paths:
                        block_entries.append(f"{redirect_ip} {site}{path}")
                if block_entries:
                    with open(hosts_file, "a") as f:
                        f.write("\n# MarThaba Block\n" + "\n".join(block_entries) + "\n")
            except Exception as e:
                print(f"Blocking error: {e}")
            time.sleep(60)
    
    def check_block_status(self):
        if self.config.get('active', False):
            end_time = datetime.datetime.fromisoformat(self.config['end_time'])
            remaining = end_time - datetime.datetime.now()
            if remaining.total_seconds() > 0:
                days = remaining.days
                hours = remaining.seconds // 3600
                channels_count = len(self.config.get('allowed_channels', []))
                custom_sites_count = len(self.config.get('custom_sites', {}))
                status_text = (f"🚫 BLOCKING ACTIVE\nRemaining: {days} days, {hours} hours")
                self.status_label.config(text=status_text, fg='#e74c3c')
                self.start_btn.config(state=tk.DISABLED)
                if datetime.datetime.now() > datetime.datetime.fromisoformat(self.config['start_time']) + datetime.timedelta(hours=1):
                    self.reset_btn.pack(side=tk.LEFT, padx=10)
            else:
                self.config['active'] = False
                self.save_config()
                self.status_label.config(text="✅ Blocking Completed!", fg='#2ecc71')
                self.start_btn.config(state=tk.NORMAL, bg='#e74c3c')
        else:
            channels_count = len(self.config.get('allowed_channels', []))
            custom_sites_count = len(self.config.get('custom_sites', {}))
            status_text = (f"🔓 Blocking Inactive")
            self.status_label.config(text=status_text, fg='#2ecc71')
            self.start_btn.config(state=tk.NORMAL, bg='#e74c3c')
        self.root.after(60000, self.check_block_status)
    
    def emergency_reset(self):
        if messagebox.askyesno("Emergency Reset", "Stop blocking immediately?"):
            self.config['active'] = False
            self.save_config()
            try:
                subprocess.run(['sudo', 'sed', '-i', '/# MarThaba Block/d', '/etc/hosts'])
            except:
                pass
            messagebox.showinfo("Reset", "Blocking stopped!")
            self.check_block_status()

if __name__ == "__main__":
    root = tk.Tk()
    app = MarThabaApp(root)
    root.mainloop()
