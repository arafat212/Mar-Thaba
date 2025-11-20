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
import sys
import base64
import tempfile

CONFIG_FILE = os.path.expanduser("~/.marthaba_config.json")
HISTORY_FILE = os.path.expanduser("~/.marthaba_history.json")

class AnimatedMarThaba:
    def __init__(self, root):
        self.root = root
        self.root.title("MarThaba Pro - Ultimate Focus System")
        self.root.geometry("480x750")
        self.root.configure(bg='#0d1117')
        self.root.resizable(False, False)
        
        # Set app icon (Shield + Clock design)
        self.setup_app_icon()
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        self.setup_styles()
        self.config = self.load_config()
        self.history = self.load_history()
        self.current_theme = 'enhanced_dark'
        self.animation_running = True
        self.emergency_used = False
        self.setup_ui()
        self.auto_resume_session()
        self.check_block_status()

    def setup_app_icon(self):
        """Create and set shield + clock icon"""
        try:
            # Simple shield + clock icon using text symbols as fallback
            # In professional install, this will use system icon
            pass
        except:
            pass

    def setup_styles(self):
        self.themes = {
            'enhanced_dark': {
                'bg': '#0d1117',
                'card_bg': '#161b22', 
                'card_hover': '#21262d',
                'accent': '#58a6ff',
                'accent_hover': '#79c0ff',
                'danger': '#f85149',
                'danger_hover': '#ff7b72',
                'success': '#3fb950',
                'warning': '#d29922',
                'text': '#f0f6fc',
                'text_light': '#8b949e',
                'border': '#30363d',
                'gradient_start': '#1a5fb4',
                'gradient_end': '#26a269'
            },
            'light_theme': {
                'bg': '#ffffff',
                'card_bg': '#f8f9fa', 
                'card_hover': '#e9ecef',
                'accent': '#007bff',
                'accent_hover': '#0056b3',
                'danger': '#dc3545',
                'danger_hover': '#c82333',
                'success': '#28a745',
                'warning': '#ffc107',
                'text': '#212529',
                'text_light': '#6c757d',
                'border': '#dee2e6',
                'gradient_start': '#007bff',
                'gradient_end': '#28a745'
            },
            'blue_dark': {
                'bg': '#0a1929',
                'card_bg': '#132f4c', 
                'card_hover': '#1e3a5c',
                'accent': '#3399ff',
                'accent_hover': '#66b3ff',
                'danger': '#ff6b6b',
                'danger_hover': '#ff8e8e',
                'success': '#4ecdc4',
                'warning': '#ffd166',
                'text': '#e1e5e9',
                'text_light': '#8fa3b7',
                'border': '#1e4976',
                'gradient_start': '#3399ff',
                'gradient_end': '#4ecdc4'
            }
        }
        self.colors = self.themes['enhanced_dark']
        
    def setup_ui(self):
        # Create notebook for tabs with custom style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.TNotebook", 
                       background=self.colors['bg'],
                       borderwidth=0)
        style.configure("Custom.TNotebook.Tab",
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_light'],
                       padding=[15, 5],
                       focuscolor=self.colors['bg'])
        style.map("Custom.TNotebook.Tab",
                 background=[("selected", self.colors['accent']),
                           ("active", self.colors['accent_hover'])],
                 foreground=[("selected", 'black')])
        
        self.notebook = ttk.Notebook(self.root, style="Custom.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Main Tab
        self.main_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.main_frame, text="🎯 Focus")
        
        # History Tab
        self.history_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.history_frame, text="📊 History")
        
        # Settings Tab
        self.settings_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.settings_frame, text="⚙️ Settings")
        
        self.create_main_ui()
        self.create_history_ui()
        self.create_settings_ui()
    
    def create_main_ui(self):
        main_container = tk.Frame(self.main_frame, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.create_enhanced_header(main_container)
        self.create_time_control(main_container)
        self.create_sites_section(main_container)
        self.create_notification_control(main_container)
        self.create_status_section(main_container)
    
    def create_enhanced_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Animated logo with shield + clock design
        self.logo_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        self.logo_frame.pack()
        
        # Shield + Clock icon
        self.logo_label = tk.Label(self.logo_frame, text="🛡️⏰", font=('Arial', 42), 
                                  bg=self.colors['bg'], fg=self.colors['accent'])
        self.logo_label.pack()
        
        # Start enhanced animation
        self.animate_logo_enhanced()
        
        title_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        title_frame.pack(pady=8)
        
        tk.Label(title_frame, text="MARTHABA PRO", font=('Arial', 18, 'bold'),
                bg=self.colors['bg'], fg=self.colors['accent']).pack()
        
        tk.Label(title_frame, text="Focus Guard • Shield Your Time", 
                font=('Arial', 10), 
                bg=self.colors['bg'], fg=self.colors['text_light']).pack()
    
    def create_time_control(self, parent):
        card = self.create_modern_card(parent)
        card.pack(fill=tk.X, pady=(0, 15))
        
        header = tk.Frame(card, bg=self.colors['card_bg'])
        header.pack(fill=tk.X, padx=15, pady=12)
        
        tk.Label(header, text="⏰ FOCUS DURATION", font=('Arial', 12, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        
        # Time input grid with modern styling
        time_frame = tk.Frame(card, bg=self.colors['card_bg'])
        time_frame.pack(fill=tk.X, padx=15, pady=(0, 12))
        
        time_units = [
            ("Hours", "hours", "1"), 
            ("Minutes", "minutes", "0"),
            ("Seconds", "seconds", "0")
        ]
        
        for i, (label, var_name, default) in enumerate(time_units):
            unit_frame = tk.Frame(time_frame, bg=self.colors['card_bg'])
            unit_frame.grid(row=0, column=i, padx=6, pady=5, sticky='nsew')
            time_frame.columnconfigure(i, weight=1)
            
            tk.Label(unit_frame, text=label, font=('Arial', 9),
                    bg=self.colors['card_bg'], fg=self.colors['text_light']).pack()
            
            var = tk.StringVar(value=default)
            setattr(self, f"{var_name}_var", var)
            
            entry = tk.Entry(unit_frame, textvariable=var, font=('Arial', 11, 'bold'),
                           width=4, bg=self.colors['border'], fg=self.colors['text'],
                           justify=tk.CENTER, relief='flat', bd=0,
                           insertbackground=self.colors['text'])
            entry.pack(pady=3, ipady=4)
            self.create_modern_entry_style(entry)
        
        # Quick actions with modern buttons
        quick_frame = tk.Frame(card, bg=self.colors['card_bg'])
        quick_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        quick_times = [
            ("25m", 0, 25, 0),
            ("1H", 1, 0, 0),
            ("2H", 2, 0, 0),
            ("4H", 4, 0, 0)
        ]
        
        quick_btn_frame = tk.Frame(quick_frame, bg=self.colors['card_bg'])
        quick_btn_frame.pack()
        
        for text, h, m, s in quick_times:
            btn = self.create_modern_button(quick_btn_frame, text, 
                                          lambda h=h, m=m, s=s: self.set_quick_time(h, m, s),
                                          size='small', style='secondary')
            btn.pack(side=tk.LEFT, padx=2)
        
        # Modern focus button with shield icon
        self.focus_btn = self.create_modern_button(card, "🛡️ START FOCUS SESSION", 
                                                 self.start_focus, 
                                                 style='primary', size='large')
        self.focus_btn.pack(fill=tk.X, padx=10, pady=10)
    
    def create_sites_section(self, parent):
        card = self.create_modern_card(parent)
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        header = tk.Frame(card, bg=self.colors['card_bg'])
        header.pack(fill=tk.X, padx=15, pady=12)
        
        tk.Label(header, text="🌐 ALLOWED SITES", font=('Arial', 12, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        
        # Add/Remove buttons frame
        self.button_frame = tk.Frame(header, bg=self.colors['card_bg'])
        self.button_frame.pack(side=tk.RIGHT)
        
        self.add_btn = self.create_modern_button(self.button_frame, "➕ Add", self.add_site, size='small')
        self.add_btn.pack(side=tk.LEFT, padx=2)
        
        self.remove_btn = self.create_modern_button(self.button_frame, "🗑️ Remove", self.remove_site, size='small', style='danger')
        self.remove_btn.pack(side=tk.LEFT, padx=2)
        
        list_frame = tk.Frame(card, bg=self.colors['card_bg'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.sites_listbox = tk.Listbox(list_frame, 
                                       bg=self.colors['border'],
                                       fg=self.colors['text'],
                                       selectbackground=self.colors['accent'],
                                       selectforeground='black',
                                       font=('Arial', 10), 
                                       relief='flat', 
                                       bd=0,
                                       highlightthickness=0,
                                       activestyle='none')
        
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                bg=self.colors['border'], 
                                troughcolor=self.colors['card_bg'],
                                activebackground=self.colors['accent'])
        scrollbar.config(command=self.sites_listbox.yview)
        self.sites_listbox.config(yscrollcommand=scrollbar.set)
        
        self.sites_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 2))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_sites_list()
        self.update_site_buttons_state()
    
    def create_notification_control(self, parent):
        card = self.create_modern_card(parent)
        card.pack(fill=tk.X, pady=(0, 15))
        
        header = tk.Frame(card, bg=self.colors['card_bg'])
        header.pack(fill=tk.X, padx=15, pady=12)
        
        tk.Label(header, text="🔔 NOTIFICATION SETTINGS", font=('Arial', 12, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        
        settings_frame = tk.Frame(card, bg=self.colors['card_bg'])
        settings_frame.pack(fill=tk.X, padx=15, pady=(0, 12))
        
        self.notify_var = tk.BooleanVar(value=self.config.get('notifications', True))
        
        # Modern checkbox
        check_frame = tk.Frame(settings_frame, bg=self.colors['card_bg'])
        check_frame.pack(anchor=tk.W)
        
        def toggle_check():
            self.notify_var.set(not self.notify_var.get())
            self.toggle_notifications()
            self.update_check_display()
        
        self.check_btn = tk.Label(check_frame, text="☐", font=('Arial', 14),
                                 bg=self.colors['card_bg'], fg=self.colors['text_light'])
        self.check_btn.pack(side=tk.LEFT)
        self.check_btn.bind("<Button-1>", lambda e: toggle_check())
        
        tk.Label(check_frame, text="Enable Notifications", font=('Arial', 10),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(side=tk.LEFT, padx=5)
        
        self.update_check_display()
    
    def create_status_section(self, parent):
        self.status_card = self.create_modern_card(parent)
        self.status_card.pack(fill=tk.X, pady=(0, 10))
        
        # Timer display frame
        self.timer_frame = tk.Frame(self.status_card, bg=self.colors['card_bg'])
        self.timer_frame.pack(fill=tk.X, pady=10)
        
        self.elapsed_label = tk.Label(self.timer_frame, text="Elapsed: 00:00:00", 
                                    font=('Arial', 10),
                                    bg=self.colors['card_bg'], fg=self.colors['text_light'])
        self.elapsed_label.pack(side=tk.LEFT, padx=10)
        
        self.remaining_label = tk.Label(self.timer_frame, text="Remaining: 00:00:00", 
                                      font=('Arial', 10),
                                      bg=self.colors['card_bg'], fg=self.colors['text_light'])
        self.remaining_label.pack(side=tk.RIGHT, padx=10)
        
        # Countdown display
        self.countdown_frame = tk.Frame(self.status_card, bg=self.colors['card_bg'])
        self.countdown_frame.pack(fill=tk.X, pady=5)
        
        self.countdown_label = tk.Label(self.countdown_frame, text="", 
                                      font=('Arial', 16, 'bold'),
                                      bg=self.colors['card_bg'], fg=self.colors['accent'])
        self.countdown_label.pack()
        
        self.status_label = tk.Label(self.status_card, text="🛡️ SYSTEM READY", 
                                   font=('Arial', 12, 'bold'),
                                   bg=self.colors['card_bg'], 
                                   fg=self.colors['accent'],
                                   pady=10)
        self.status_label.pack()
        
        # Emergency button - always visible when active
        self.emergency_btn = self.create_modern_button(self.status_card, 
                                                     "🆘 EMERGENCY STOP (30min)", 
                                                     self.emergency_stop, 
                                                     style='danger', 
                                                     size='large')
        # Initially hidden
        self.emergency_btn.pack_forget()
    
    def create_history_ui(self):
        history_container = tk.Frame(self.history_frame, bg=self.colors['bg'])
        history_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        header = tk.Frame(history_container, bg=self.colors['bg'])
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header, text="📊 FOCUS HISTORY", font=('Arial', 18, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text']).pack()
        
        tk.Label(header, text="Your previous focus sessions and achievements", 
                font=('Arial', 10),
                bg=self.colors['bg'], fg=self.colors['text_light']).pack()
        
        # Modern history list
        list_frame = tk.Frame(history_container, bg=self.colors['bg'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_text = tk.Text(list_frame, 
                                   bg=self.colors['border'],
                                   fg=self.colors['text'],
                                   font=('Arial', 10), 
                                   wrap=tk.WORD,
                                   relief='flat', 
                                   bd=0, 
                                   padx=12, 
                                   pady=12,
                                   selectbackground=self.colors['accent'])
        
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                bg=self.colors['border'], 
                                troughcolor=self.colors['bg'],
                                activebackground=self.colors['accent'])
        scrollbar.config(command=self.history_text.yview)
        self.history_text.config(yscrollcommand=scrollbar.set)
        
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_history_data()
    
    def create_settings_ui(self):
        settings_container = tk.Frame(self.settings_frame, bg=self.colors['bg'])
        settings_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        header = tk.Frame(settings_container, bg=self.colors['bg'])
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header, text="⚙️ SETTINGS", font=('Arial', 18, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text']).pack()
        
        tk.Label(header, text="Customize your MarThaba experience", 
                font=('Arial', 10),
                bg=self.colors['bg'], fg=self.colors['text_light']).pack()
        
        # Theme selection card
        theme_card = self.create_modern_card(settings_container)
        theme_card.pack(fill=tk.X, pady=(0, 15))
        
        theme_header = tk.Frame(theme_card, bg=self.colors['card_bg'])
        theme_header.pack(fill=tk.X, padx=15, pady=12)
        
        tk.Label(theme_header, text="🎨 THEME SELECTOR", font=('Arial', 12, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        
        # Theme buttons
        theme_buttons_frame = tk.Frame(theme_card, bg=self.colors['card_bg'])
        theme_buttons_frame.pack(fill=tk.X, padx=15, pady=(0, 12))
        
        themes = [
            ("🌙 Dark Theme", "enhanced_dark"),
            ("☀️ Light Theme", "light_theme"),
            ("🔵 Blue Dark", "blue_dark")
        ]
        
        for theme_name, theme_key in themes:
            theme_btn = self.create_modern_button(theme_buttons_frame, theme_name,
                                                lambda key=theme_key: self.change_theme(key),
                                                style='secondary', size='normal')
            theme_btn.pack(fill=tk.X, pady=3)
    
    def create_modern_card(self, parent):
        card = tk.Frame(parent, bg=self.colors['card_bg'], relief='flat', bd=0)
        card.config(highlightbackground=self.colors['border'], 
                   highlightcolor=self.colors['border'],
                   highlightthickness=1)
        return card
    
    def create_modern_button(self, parent, text, command, style='primary', size='normal'):
        if style == 'primary':
            bg, fg, hover_bg = self.colors['accent'], 'black', self.colors['accent_hover']
        elif style == 'danger':
            bg, fg, hover_bg = self.colors['danger'], 'white', self.colors['danger_hover']
        elif style == 'secondary':
            bg, fg, hover_bg = self.colors['card_bg'], self.colors['text_light'], self.colors['card_hover']
        else:
            bg, fg, hover_bg = self.colors['card_bg'], self.colors['text'], self.colors['card_hover']
        
        font_size = 9 if size == 'small' else 11 if size == 'normal' else 12
        padding = 8 if size == 'small' else 12 if size == 'normal' else 14
        
        btn = tk.Label(parent, text=text, font=('Arial', font_size, 'bold'),
                      bg=bg, fg=fg, relief='flat', bd=0,
                      padx=padding, pady=padding)
        
        btn.bind("<Button-1>", lambda e: command())
        
        # Enhanced hover effect
        def on_enter(e):
            if btn.cget('state') != 'disabled':
                btn.config(bg=hover_bg, cursor='hand2')
        def on_leave(e):
            if btn.cget('state') != 'disabled':
                btn.config(bg=bg, cursor='')
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_modern_entry_style(self, entry):
        def on_focusin(e):
            entry.config(highlightbackground=self.colors['accent'],
                        highlightcolor=self.colors['accent'],
                        highlightthickness=1)
        def on_focusout(e):
            entry.config(highlightbackground=self.colors['border'],
                        highlightcolor=self.colors['border'],
                        highlightthickness=1)
        
        entry.bind("<FocusIn>", on_focusin)
        entry.bind("<FocusOut>", on_focusout)
    
    def animate_logo_enhanced(self):
        if not self.animation_running:
            return
            
        colors = [self.colors['accent'], self.colors['success'], self.colors['warning']]
        current_color = self.logo_label.cget('fg')
        
        try:
            current_index = colors.index(current_color)
        except:
            current_index = 0
            
        next_index = (current_index + 1) % len(colors)
        
        self.logo_label.config(fg=colors[next_index])
        self.root.after(1500, self.animate_logo_enhanced)
    
    def update_check_display(self):
        """Update the notification checkbox display"""
        if self.notify_var.get():
            self.check_btn.config(text="☑", fg=self.colors['success'])
        else:
            self.check_btn.config(text="☐", fg=self.colors['text_light'])
    
    def set_quick_time(self, hours, minutes, seconds):
        self.hours_var.set(str(hours))
        self.minutes_var.set(str(minutes))
        self.seconds_var.set(str(seconds))
    
    def add_site(self):
        # Check if focus session is active
        if self.config.get('active', False):
            self.show_notification("❌ Cannot add sites during an active focus session!\nPlease wait until the session ends.")
            return
            
        site_url = simpledialog.askstring("Add Allowed Site", 
                                        "Enter website URL (e.g., youtube.com, facebook.com):")
        
        if site_url:
            # Clean the URL
            site_url = site_url.lower().replace('https://', '').replace('http://', '').replace('www.', '')
            sites = self.config.get('allowed_sites', [])
            if site_url not in sites:
                sites.append(site_url)
                self.config['allowed_sites'] = sites
                self.save_config()
                self.load_sites_list()
                self.show_notification(f"✅ Site added: {site_url}")
    
    def remove_site(self):
        # Check if focus session is active
        if self.config.get('active', False):
            self.show_notification("❌ Cannot remove sites during an active focus session!\nPlease wait until the session ends.")
            return
            
        selection = self.sites_listbox.curselection()
        if selection:
            site = self.sites_listbox.get(selection[0])
            # Extract site name from display text
            site_name = site.replace("🌐 ", "")
            sites = self.config.get('allowed_sites', [])
            if site_name in sites:
                sites.remove(site_name)
                self.config['allowed_sites'] = sites
                self.save_config()
                self.load_sites_list()
                self.show_notification(f"✅ Site removed: {site_name}")
    
    def load_sites_list(self):
        self.sites_listbox.delete(0, tk.END)
        sites = self.config.get('allowed_sites', [])
        for site in sites:
            self.sites_listbox.insert(tk.END, f"🌐 {site}")
    
    def toggle_notifications(self):
        self.config['notifications'] = self.notify_var.get()
        self.save_config()
        status = "enabled" if self.notify_var.get() else "disabled"
        self.show_notification(f"Notifications {status}")
    
    def show_notification(self, message):
        if self.config.get('notifications', True):
            messagebox.showinfo("MarThaba Pro", message)
    
    def load_history_data(self):
        self.history_text.delete(1.0, tk.END)
        
        if not self.history:
            self.history_text.insert(tk.END, "🌟 No focus sessions yet.\n\nStart your first focus session to build your productivity history!")
            self.history_text.tag_configure("center", justify='center')
            self.history_text.tag_add("center", "1.0", "end")
            return
        
        for session in reversed(self.history[-10:]):  # Show last 10 sessions
            start_time = datetime.datetime.fromisoformat(session['start_time'])
            end_time = datetime.datetime.fromisoformat(session['end_time'])
            duration = session['duration']
            
            self.history_text.insert(tk.END, 
                                   f"📅 {start_time.strftime('%Y-%m-%d %H:%M')}\n"
                                   f"⏰ Duration: {duration:.1f} hours\n"
                                   f"✅ Status: Completed\n"
                                   f"─────────────────────\n\n")
    
    def start_focus(self):
        try:
            hours = int(self.hours_var.get() or 0)
            minutes = int(self.minutes_var.get() or 0)
            seconds = int(self.seconds_var.get() or 0)
            
            total_seconds = hours*3600 + minutes*60 + seconds
            if total_seconds <= 0:
                self.show_notification("Please set a valid time duration")
                return
                
        except ValueError:
            self.show_notification("Please enter valid numbers")
            return
        
        self.start_time = datetime.datetime.now()
        end_time = self.start_time + datetime.timedelta(seconds=total_seconds)
        total_hours = total_seconds / 3600
        
        self.config.update({
            'active': True,
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration': total_hours
        })
        self.save_config()
        
        # Add to history
        self.history.append({
            'start_time': self.config['start_time'],
            'end_time': self.config['end_time'],
            'duration': total_hours,
            'sites': self.config.get('allowed_sites', [])
        })
        self.save_history()
        
        # Start blocking
        threading.Thread(target=self.block_sites, daemon=True).start()
        
        # Update UI
        self.focus_btn.config(text="🛡️ FOCUS ACTIVE", bg=self.colors['warning'])
        self.status_label.config(text=f"🛡️ FOCUS MODE ACTIVE", 
                               fg=self.colors['warning'])
        
        # Show timer and emergency button
        self.timer_frame.pack(fill=tk.X, pady=10)
        self.countdown_frame.pack(fill=tk.X, pady=5)
        self.emergency_btn.pack(fill=tk.X, padx=10, pady=5)
        self.emergency_used = False
        
        # Disable site buttons
        self.update_site_buttons_state()
        
        self.show_notification(f"Focus started for {total_hours:.1f} hours!")
    
    def block_sites(self):
        hosts_file = "/etc/hosts"
        redirect_ip = "127.0.0.1"
        
        while self.config.get('active', False):
            end_time = datetime.datetime.fromisoformat(self.config['end_time'])
            if datetime.datetime.now() > end_time:
                self.config['active'] = False
                self.save_config()
                self.check_block_status()
                break
            
            try:
                subprocess.run(['sudo', 'sed', '-i', '/# MarThaba Focus/d', hosts_file], capture_output=True)
                
                # Default blocked sites
                block_entries = [
                    f"{redirect_ip} www.youtube.com",
                    f"{redirect_ip} youtube.com", 
                    f"{redirect_ip} m.youtube.com",
                    f"{redirect_ip} www.youtube.com/shorts",
                    f"{redirect_ip} www.youtube.com/reel",
                    f"{redirect_ip} m.youtube.com/shorts",
                    f"{redirect_ip} www.facebook.com",
                    f"{redirect_ip} facebook.com",
                    f"{redirect_ip} m.facebook.com",
                    f"{redirect_ip} www.facebook.com/reel",
                    f"{redirect_ip} www.facebook.com/watch",
                    f"{redirect_ip} www.instagram.com",
                    f"{redirect_ip} instagram.com",
                    f"{redirect_ip} www.instagram.com/reels"
                ]
                
                # Unblock allowed sites
                allowed_sites = self.config.get('allowed_sites', [])
                for site in allowed_sites:
                    subprocess.run(['sudo', 'sed', '-i', f'/{site}/d', hosts_file], capture_output=True)
                
                if block_entries:
                    with open(hosts_file, "a") as f:
                        f.write("\n# MarThaba Focus\n" + "\n".join(block_entries) + "\n")
                
            except Exception as e:
                print(f"Blocking error: {e}")
            
            time.sleep(30)
    
    def emergency_stop(self):
        if self.emergency_used:
            self.show_notification("Emergency stop can only be used once per session!")
            return
            
        # Set focus to end in 30 minutes
        emergency_end_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        self.config['end_time'] = emergency_end_time.isoformat()
        self.save_config()
        
        self.emergency_used = True
        self.emergency_btn.config(text="🆘 EMERGENCY USED", bg=self.colors['text_light'])
        
        self.show_notification("Emergency stop activated! Focus will end in 30 minutes.")
    
    def update_timer_display(self):
        if self.config.get('active', False):
            current_time = datetime.datetime.now()
            start_time = datetime.datetime.fromisoformat(self.config['start_time'])
            end_time = datetime.datetime.fromisoformat(self.config['end_time'])
            
            # Calculate elapsed time
            elapsed = current_time - start_time
            elapsed_hours = int(elapsed.total_seconds() // 3600)
            elapsed_minutes = int((elapsed.total_seconds() % 3600) // 60)
            elapsed_seconds = int(elapsed.total_seconds() % 60)
            
            # Calculate remaining time
            remaining = end_time - current_time
            if remaining.total_seconds() > 0:
                remaining_hours = int(remaining.total_seconds() // 3600)
                remaining_minutes = int((remaining.total_seconds() % 3600) // 60)
                remaining_seconds = int(remaining.total_seconds() % 60)
                
                # Update labels
                self.elapsed_label.config(text=f"Elapsed: {elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_seconds:02d}")
                self.remaining_label.config(text=f"Remaining: {remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}")
                
                # Update countdown
                if remaining.total_seconds() > 3600:  # More than 1 hour
                    countdown_text = f"⏳ {remaining_hours}h {remaining_minutes}m {remaining_seconds}s"
                elif remaining.total_seconds() > 60:  # More than 1 minute
                    countdown_text = f"⏳ {remaining_minutes}m {remaining_seconds}s"
                else:  # Less than 1 minute
                    countdown_text = f"⏳ {remaining_seconds}s"
                
                self.countdown_label.config(text=countdown_text)
    
    def check_block_status(self):
        self.update_timer_display()
        
        if self.config.get('active', False):
            end_time = datetime.datetime.fromisoformat(self.config['end_time'])
            remaining = end_time - datetime.datetime.now()
            
            if remaining.total_seconds() > 0:
                hours = int(remaining.total_seconds() // 3600)
                mins = int((remaining.total_seconds() % 3600) // 60)
                secs = int(remaining.total_seconds() % 60)
                
                status_text = f"🛡️ FOCUS ACTIVE"
                self.status_label.config(text=status_text, fg=self.colors['warning'])
                
                # Show emergency button and timer
                self.emergency_btn.pack(fill=tk.X, padx=10, pady=5)
                self.timer_frame.pack(fill=tk.X, pady=10)
                self.countdown_frame.pack(fill=tk.X, pady=5)
            else:
                self.config['active'] = False
                self.save_config()
                self.status_label.config(text="✅ FOCUS COMPLETE", fg=self.colors['success'])
                self.focus_btn.config(text="🛡️ START FOCUS SESSION", bg=self.colors['accent'])
                self.emergency_btn.pack_forget()
                self.timer_frame.pack_forget()
                self.countdown_frame.pack_forget()
                self.countdown_label.config(text="")
                self.emergency_used = False
                
                # Enable site buttons after focus session ends
                self.update_site_buttons_state()
                
                self.show_notification("Focus session completed!")
        else:
            self.status_label.config(text="🛡️ SYSTEM READY", fg=self.colors['accent'])
            self.emergency_btn.pack_forget()
            self.timer_frame.pack_forget()
            self.countdown_frame.pack_forget()
            self.countdown_label.config(text="")
            self.emergency_used = False
            
            # Enable site buttons when no focus session is active
            self.update_site_buttons_state()
        
        self.root.after(1000, self.check_block_status)
    
    def load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'active': False, 'allowed_sites': [], 'notifications': True}
    
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f)
    
    def load_history(self):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_history(self):
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimatedMarThaba(root)
    app.animate_logo_enhanced()
    root.mainloop()
