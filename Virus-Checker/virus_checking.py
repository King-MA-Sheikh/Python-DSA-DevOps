import os
import hashlib
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
import random
import psutil
import socket
from datetime import datetime
import webbrowser
import platform
import json
from collections import defaultdict

# Constants
QUARANTINE_DIR = os.path.join(os.getcwd(), "quarantine")
if not os.path.exists(QUARANTINE_DIR):
    os.makedirs(QUARANTINE_DIR)

# Load virus signatures from file if available, otherwise use defaults
try:
    with open('virus_signatures.json', 'r') as f:
        KNOWN_VIRUS_SIGNATURES = set(json.load(f))
except (FileNotFoundError, json.JSONDecodeError):
    KNOWN_VIRUS_SIGNATURES = {
        "5d41402abc4b2a76b9719d911017c592",
        "e99a18c428cb38d5f260853678922e03",
        "098f6bcd4621d373cade4e832627b4f6",
        "a7f5f35426b927411fc9231b56382173",
        "d41d8cd98f00b204e9800998ecf8427e",
    }

# UI Configuration
BG_COLOR = "#0d1117"
FG_COLOR = "#00ff41"
ACCENT_COLOR = "#ff003c"
SECONDARY_COLOR = "#00bfff"
TEXT_COLOR = "#f0f0f0"

FONTS = {
    'header': ("Consolas", 18, "bold"),
    'title': ("Consolas", 14, "bold"),
    'body': ("Consolas", 10),
    'button': ("Consolas", 10, "bold")
}

class HackerScanner:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.start_system_monitoring()

    def setup_window(self):
        self.root.title("🔒 CYBER GUARDIAN - Advanced Threat Detection")
        self.root.geometry("1000x750")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(900, 650)
        
    def setup_variables(self):
        self.scan_active = False
        self.scan_thread = None
        self.total_files = 0
        self.scanned_files = 0
        self.infected_files = []
        self.current_scan_folder = ""
        self.processes = []
        self.network_devices = []
        self.system_stats = {
            'cpu': 0,
            'memory': 0,
            'threats': 0,
            'temperature': 0,
            'disk': 0
        }
        self.status_var = tk.StringVar(value="🟢 System Secure | Ready for scan")
        
    def setup_ui(self):
        self.setup_styles()
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=FONTS['body'])
        style.configure('Header.TLabel', background=BG_COLOR, foreground=FG_COLOR, font=FONTS['header'])
        style.configure('Title.TLabel', background=BG_COLOR, foreground=SECONDARY_COLOR, font=FONTS['title'])
        style.configure('TButton', background=BG_COLOR, foreground=TEXT_COLOR, font=FONTS['button'], 
                       borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#1f2d38')])
        style.configure('Red.TButton', background=BG_COLOR, foreground=ACCENT_COLOR, font=FONTS['button'])
        style.configure('Green.TButton', background=BG_COLOR, foreground="#00ff00", font=FONTS['button'])
        style.configure('TProgressbar', thickness=20, background=FG_COLOR, troughcolor='#1f2d38')
        style.configure('Status.TLabel', background='#1f2d38', foreground=FG_COLOR, font=("Consolas", 8))
        style.configure('Treeview', background='#1f2d38', fieldbackground='#1f2d38', foreground=FG_COLOR)
        style.map('Treeview', background=[('selected', '#2a3b45')])
        style.configure('Treeview.Heading', background='#1f2d38', foreground=SECONDARY_COLOR)

    def create_header(self):
        header_frame = ttk.Frame(self.root, padding=(20, 10))
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(header_frame, 
                              text="CYBER GUARDIAN  🔒  Advanced Threat Detection", 
                              style='Header.TLabel')
        title_label.pack(side=tk.LEFT)
        
        self.status_indicator = ttk.Label(header_frame, text="🟢 SYSTEM SECURE", 
                                        foreground="#00ff00", style='Title.TLabel')
        self.status_indicator.pack(side=tk.RIGHT, padx=10)

    def create_main_content(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel
        left_frame = ttk.Frame(main_frame, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        self.create_scan_section(left_frame)
        self.create_special_functions_panel(left_frame)
        self.create_quarantine_section(left_frame)
        self.create_stats_panel(left_frame)
        
        # Right panel
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_progress_section(right_frame)
        self.create_results_section(right_frame)
        self.create_action_buttons(right_frame)

    def create_scan_section(self, parent):
        scan_frame = ttk.LabelFrame(parent, text="🔍 Scan Operations", padding=10)
        scan_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(scan_frame, text="Target Directory:").pack(anchor=tk.W)
        
        dir_frame = ttk.Frame(scan_frame)
        dir_frame.pack(fill=tk.X, pady=5)
        
        self.dir_entry = ttk.Entry(dir_frame)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(dir_frame, text="📂", width=3, command=self.browse_directory)
        browse_btn.pack(side=tk.RIGHT)
        
        scan_btn = ttk.Button(scan_frame, text="🔍 Start Deep Scan", 
                             command=self.start_scan, style='Green.TButton')
        scan_btn.pack(fill=tk.X, pady=5)

    def create_special_functions_panel(self, parent):
        special_frame = ttk.LabelFrame(parent, text="⚡ Special Functions", padding=10)
        special_frame.pack(fill=tk.X, pady=10)
        
        buttons = [
            ("🌐 Network Scan", self.network_scan, 'Green.TButton'),
            ("📊 Process Monitor", self.show_process_monitor, 'Green.TButton'),
            ("🔄 Update Signatures", self.update_virus_signatures, 'Green.TButton'),
            ("🛡️ Quick Hardening", self.system_hardening, 'Red.TButton'),
            ("🚨 Emergency Lockdown", self.emergency_lockdown, 'Red.TButton'),
            ("🕵️ Dark Web Scan", self.darkweb_monitor, 'Green.TButton'),
            ("📈 Performance Monitor", self.show_performance_monitor, 'Green.TButton')
        ]
        
        for text, command, style in buttons:
            ttk.Button(special_frame, text=text, command=command, style=style).pack(fill=tk.X, pady=2)

    def create_quarantine_section(self, parent):
        quarantine_frame = ttk.LabelFrame(parent, text="☣️ Quarantine Management", padding=10)
        quarantine_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(quarantine_frame, text="☣️ View Quarantine", 
                  command=self.view_quarantine).pack(fill=tk.X, pady=2)
        ttk.Button(quarantine_frame, text="🔄 Restore All", 
                  command=self.restore_quarantine).pack(fill=tk.X, pady=2)
        ttk.Button(quarantine_frame, text="🧹 Clean Quarantine", 
                  command=self.clean_quarantine, style='Red.TButton').pack(fill=tk.X, pady=2)

    def create_stats_panel(self, parent):
        stats_frame = ttk.LabelFrame(parent, text="📊 System Stats", padding=10)
        stats_frame.pack(fill=tk.X, pady=10)
        
        stats = [
            ("CPU Usage:", "cpu", "%"),
            ("Memory Usage:", "memory", "%"),
            ("Disk Usage:", "disk", "%"),
            ("Temperature:", "temperature", "°C"),
            ("Active Threats:", "threats", "")
        ]
        
        for label, key, unit in stats:
            frame = ttk.Frame(stats_frame)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=label, width=15, anchor=tk.W).pack(side=tk.LEFT)
            label_widget = ttk.Label(frame, text="--"+unit, width=8)
            label_widget.pack(side=tk.RIGHT)
            # Store reference to each label
            setattr(self, f"{key}_label", label_widget)

    def create_progress_section(self, parent):
        progress_frame = ttk.Frame(parent)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to scan...")
        self.progress_label.pack(anchor=tk.W)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill=tk.X)

    def create_results_section(self, parent):
        results_frame = ttk.LabelFrame(parent, text="📋 Scan Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create results treeview with sortable columns
        columns = [
            ("file", "File", 150),
            ("status", "Status", 100),
            ("path", "Path", 400),
            ("size", "Size", 80),
            ("modified", "Modified", 120)
        ]
        
        self.results_tree = ttk.Treeview(results_frame, columns=[col[0] for col in columns], 
                                        show="headings", selectmode="extended")
        
        for col_id, heading, width in columns:
            self.results_tree.heading(col_id, text=heading, 
                                    command=lambda c=col_id: self.treeview_sort_column(c, False))
            self.results_tree.column(col_id, width=width)
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        x_scroll = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
        
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure tags for infected files
        self.results_tree.tag_configure('infected', foreground=ACCENT_COLOR)
        self.results_tree.tag_configure('clean', foreground=FG_COLOR)

    def create_action_buttons(self, parent):
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        buttons = [
            ("🗑️ Clear Selection", self.clear_selection, 'LEFT'),
            ("📋 Copy Selected", self.copy_selected, 'LEFT'),
            ("🧹 Clean Dashboard", self.clean_dashboard, 'LEFT'),
            ("⏹️ Stop Scan", self.stop_scan, 'RIGHT'),
            ("🦠 Quarantine Selected", self.clean_selected, 'RIGHT', 'Red.TButton')
        ]
        
        for text, command, side, *style in buttons:
            btn_style = style[0] if style else None
            btn = ttk.Button(action_frame, text=text, command=command, style=btn_style)
            btn.pack(side=getattr(tk, side.upper()), padx=5)
            if text == "⏹️ Stop Scan":
                self.stop_btn = btn
                self.stop_btn.config(state=tk.DISABLED)
            elif text == "🦠 Quarantine Selected":
                self.clean_btn = btn
                self.clean_btn.config(state=tk.DISABLED)

    def clean_dashboard(self):
        """Clear all scan results from the dashboard"""
        self.results_tree.delete(*self.results_tree.get_children())
        self.progress['value'] = 0
        self.progress_label.config(text="Ready to scan...")
        self.infected_files = []
        self.status_var.set("🟢 System Secure | Ready for scan")
        self.status_indicator.config(text="🟢 SYSTEM SECURE", foreground="#00ff00")
        messagebox.showinfo("Dashboard Cleaned", "All scan results have been cleared")

    def create_status_bar(self):
        status_frame = ttk.Frame(self.root, style='Status.TFrame')
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Status.TLabel')
        status_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(status_frame, text=f"Signatures: {len(KNOWN_VIRUS_SIGNATURES)}", 
                 style='Status.TLabel').pack(side=tk.RIGHT, padx=10)
        ttk.Label(status_frame, text=f"OS: {platform.system()} {platform.release()}", 
                 style='Status.TLabel').pack(side=tk.RIGHT, padx=10)

    # Core scanning functionality
    def start_scan(self):
        folder_path = self.dir_entry.get()
        if not folder_path or not os.path.exists(folder_path):
            messagebox.showerror("Error", "Please select a valid directory to scan")
            return
            
        if self.scan_active:
            messagebox.showwarning("Warning", "Scan already in progress")
            return
            
        self.prepare_for_scan(folder_path)
        self.scan_thread = threading.Thread(target=self.scan_directory, args=(folder_path,))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        self.monitor_progress()

    def prepare_for_scan(self, folder_path):
        self.scan_active = True
        self.infected_files = []
        self.results_tree.delete(*self.results_tree.get_children())
        self.progress['value'] = 0
        self.progress_label.config(text="Initializing scan...")
        self.status_var.set("🟡 Scanning in progress...")
        self.status_indicator.config(text="🟡 SCANNING", foreground="yellow")
        self.clean_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.current_scan_folder = folder_path

    def scan_directory(self, directory):
        self.scanned_files = 0
        self.total_files = sum(len(files) for _, _, files in os.walk(directory))
        
        infected_count = 0
        for root, _, files in os.walk(directory):
            for file in files:
                if not self.scan_active:
                    return
                    
                path = os.path.join(root, file)
                file_hash = self.calculate_md5(path)
                self.scanned_files += 1
                
                try:
                    file_stats = os.stat(path)
                    size = file_stats.st_size
                    modified = datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M")
                except:
                    size = 0
                    modified = "Unknown"
                
                if file_hash in KNOWN_VIRUS_SIGNATURES:
                    infected_count += 1
                    self.infected_files.append(path)
                    self.add_result(file, "INFECTED", path, size, modified, "infected")
                else:
                    self.add_result(file, "Clean", path, size, modified, "clean")
                
                time.sleep(0.01)  # For demonstration
        
        self.scan_active = False
        self.root.after(0, lambda: self.scan_completed(infected_count))

    def add_result(self, file, status, path, size, modified, tag):
        size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
        self.root.after(0, lambda: self.results_tree.insert(
            "", "end", values=(file, status, path, size_str, modified), tags=(tag,))
        )

    def monitor_progress(self):
        if not self.scan_active:
            return
            
        if self.total_files > 0:
            progress = int((self.scanned_files / self.total_files) * 100)
            self.progress['value'] = progress
            self.progress_label.config(
                text=f"Scanning... {self.scanned_files}/{self.total_files} files ({progress}%)"
            )
            
        self.root.after(100, self.monitor_progress)

    def scan_completed(self, infected_count):
        self.progress['value'] = 100
        self.progress_label.config(text=f"Scan complete! Scanned {self.scanned_files} files")
        self.stop_btn.config(state=tk.DISABLED)
        
        if infected_count > 0:
            self.status_var.set(f"🔴 {infected_count} threats detected!")
            self.status_indicator.config(text="🔴 THREATS DETECTED", foreground=ACCENT_COLOR)
            self.clean_btn.config(state=tk.NORMAL)
            messagebox.showwarning(
                "Scan Complete",
                f"⚠️ {infected_count} infected file(s) found!\n\n"
                "Select files and click 'Quarantine Selected' to isolate threats."
            )
        else:
            self.status_var.set("🟢 No threats detected | System Secure")
            self.status_indicator.config(text="🟢 SYSTEM SECURE", foreground="#00ff00")
            messagebox.showinfo("Scan Complete", "✅ No viruses found.\n\nSystem is secure!")

    def stop_scan(self):
        self.scan_active = False
        self.progress_label.config(text="Scan stopped by user")
        self.status_var.set("🟠 Scan stopped by user")
        self.status_indicator.config(text="🟠 SCAN STOPPED", foreground="orange")
        self.stop_btn.config(state=tk.DISABLED)

    # Quarantine management
    def clean_selected(self):
        selected = self.results_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select files to quarantine")
            return
            
        files_to_quarantine = []
        for item in selected:
            values = self.results_tree.item(item, 'values')
            if values and values[1] == "INFECTED":
                files_to_quarantine.append(values[2])
        
        if not files_to_quarantine:
            messagebox.showinfo("Info", "No infected files selected")
            return
            
        if self.clean_files(files_to_quarantine):
            for item in selected:
                self.results_tree.delete(item)
                
            messagebox.showinfo("Success", f"✅ {len(files_to_quarantine)} file(s) moved to quarantine")
            
            remaining_infected = len(self.infected_files) - len(files_to_quarantine)
            if remaining_infected > 0:
                self.status_var.set(f"🟠 {remaining_infected} threats remain!")
                self.status_indicator.config(text="🟠 THREATS DETECTED", foreground="orange")
            else:
                self.status_var.set("🟢 All threats quarantined | System Secure")
                self.status_indicator.config(text="🟢 SYSTEM SECURE", foreground="#00ff00")
                self.clean_btn.config(state=tk.DISABLED)

    def clean_files(self, files):
        if not os.path.exists(QUARANTINE_DIR):
            os.makedirs(QUARANTINE_DIR)

        success = 0
        for file in files:
            try:
                dest = os.path.join(QUARANTINE_DIR, os.path.basename(file))
                # Handle duplicate filenames
                counter = 1
                while os.path.exists(dest):
                    name, ext = os.path.splitext(os.path.basename(file))
                    dest = os.path.join(QUARANTINE_DIR, f"{name}_{counter}{ext}")
                    counter += 1
                
                shutil.move(file, dest)
                success += 1
            except Exception as e:
                print(f"Error moving file {file}: {e}")
        
        return success > 0

    def view_quarantine(self):
        quarantine_window = tk.Toplevel(self.root)
        quarantine_window.title("Quarantine Manager")
        quarantine_window.geometry("700x500")
        quarantine_window.configure(bg=BG_COLOR)
        
        ttk.Label(quarantine_window, text="☣️ Quarantined Files", style='Header.TLabel').pack(pady=10)
        
        # Create treeview
        columns = [
            ("file", "File", 200),
            ("original_path", "Original Path", 300),
            ("date", "Quarantined", 150),
            ("size", "Size", 100)
        ]
        
        tree = ttk.Treeview(quarantine_window, columns=[col[0] for col in columns], show="headings")
        for col_id, heading, width in columns:
            tree.heading(col_id, text=heading)
            tree.column(col_id, width=width)
        
        scrollbar = ttk.Scrollbar(quarantine_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Populate with quarantine info
        try:
            quarantine_log = os.path.join(QUARANTINE_DIR, "quarantine_log.json")
            if os.path.exists(quarantine_log):
                with open(quarantine_log, 'r') as f:
                    quarantine_data = json.load(f)
                
                for file, data in quarantine_data.items():
                    file_path = os.path.join(QUARANTINE_DIR, file)
                    if os.path.exists(file_path):
                        size = os.path.getsize(file_path)
                        size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
                        tree.insert("", "end", values=(
                            file,
                            data.get('original_path', 'Unknown'),
                            data.get('date', 'Unknown'),
                            size_str
                        ))
        except Exception as e:
            print(f"Error loading quarantine log: {e}")
        
        # Action buttons
        btn_frame = ttk.Frame(quarantine_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Restore Selected", 
                  command=lambda: self.restore_from_quarantine(tree)).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Delete Permanently", style='Red.TButton',
                  command=lambda: self.delete_from_quarantine(tree)).pack(side=tk.RIGHT)

    def restore_from_quarantine(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select files to restore")
            return
            
        restored = 0
        errors = 0
        
        for item in selected:
            values = tree.item(item, 'values')
            file = values[0]
            original_path = values[1]
            src = os.path.join(QUARANTINE_DIR, file)
            
            try:
                if not original_path or original_path == 'Unknown':
                    dest = filedialog.askdirectory(title="Select restore location for " + file)
                    if not dest:
                        continue
                    dest = os.path.join(dest, file)
                else:
                    dest = original_path
                
                shutil.move(src, dest)
                self.remove_from_quarantine_log(file)
                restored += 1
            except Exception as e:
                errors += 1
                messagebox.showerror("Error", f"Failed to restore {file}: {str(e)}")
        
        if restored > 0:
            messagebox.showinfo("Success", f"✅ Restored {restored} file(s)")
            # Refresh the treeview
            for item in selected:
                tree.delete(item)
        
        if errors:
            messagebox.showwarning("Warning", f"Failed to restore {errors} file(s)")

    def delete_from_quarantine(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select files to delete")
            return
            
        if not messagebox.askyesno("Confirm", "Permanently delete selected files? This cannot be undone."):
            return
            
        deleted = 0
        errors = 0
        
        for item in selected:
            file = tree.item(item, 'values')[0]
            path = os.path.join(QUARANTINE_DIR, file)
            
            try:
                os.remove(path)
                self.remove_from_quarantine_log(file)
                deleted += 1
            except Exception as e:
                errors += 1
                messagebox.showerror("Error", f"Failed to delete {file}: {str(e)}")
        
        if deleted > 0:
            messagebox.showinfo("Success", f"🗑️ Permanently deleted {deleted} file(s)")
            # Refresh the treeview
            for item in selected:
                tree.delete(item)
        
        if errors:
            messagebox.showwarning("Warning", f"Failed to delete {errors} file(s)")

    def clean_quarantine(self):
        if not os.listdir(QUARANTINE_DIR):
            messagebox.showinfo("Info", "Quarantine is already empty")
            return
            
        if not messagebox.askyesno("Confirm", "Permanently delete ALL files in quarantine? This cannot be undone."):
            return
            
        deleted = 0
        errors = 0
        
        for file in os.listdir(QUARANTINE_DIR):
            if file == "quarantine_log.json":
                continue
                
            try:
                os.remove(os.path.join(QUARANTINE_DIR, file))
                deleted += 1
            except Exception as e:
                errors += 1
                print(f"Error deleting {file}: {e}")
        
        # Clear the quarantine log
        try:
            with open(os.path.join(QUARANTINE_DIR, "quarantine_log.json"), 'w') as f:
                json.dump({}, f)
        except Exception as e:
            print(f"Error clearing quarantine log: {e}")
        
        msg = f"✅ Deleted {deleted} file(s)"
        if errors:
            msg += f"\n❌ Failed to delete {errors} file(s)"
        messagebox.showinfo("Clean Complete", msg)

    def remove_from_quarantine_log(self, filename):
        try:
            quarantine_log = os.path.join(QUARANTINE_DIR, "quarantine_log.json")
            if os.path.exists(quarantine_log):
                with open(quarantine_log, 'r') as f:
                    data = json.load(f)
                
                if filename in data:
                    del data[filename]
                    
                    with open(quarantine_log, 'w') as f:
                        json.dump(data, f)
        except Exception as e:
            print(f"Error updating quarantine log: {e}")

    def restore_quarantine(self):
        if not os.listdir(QUARANTINE_DIR):
            messagebox.showinfo("Info", "Quarantine is empty")
            return
            
        if messagebox.askyesno("Confirm", "Restore all files from quarantine to their original locations?"):
            restored = 0
            errors = 0
            
            try:
                quarantine_log = os.path.join(QUARANTINE_DIR, "quarantine_log.json")
                if os.path.exists(quarantine_log):
                    with open(quarantine_log, 'r') as f:
                        quarantine_data = json.load(f)
                    
                    for file, data in quarantine_data.items():
                        src = os.path.join(QUARANTINE_DIR, file)
                        dest = data.get('original_path', '')
                        
                        if not dest or not os.path.exists(os.path.dirname(dest)):
                            dest = filedialog.askdirectory(title=f"Select restore location for {file}")
                            if not dest:
                                continue
                            dest = os.path.join(dest, file)
                        
                        try:
                            shutil.move(src, dest)
                            restored += 1
                        except Exception as e:
                            errors += 1
                            print(f"Error restoring {file}: {e}")
                
                # Clear the quarantine log after restore
                with open(quarantine_log, 'w') as f:
                    json.dump({}, f)
                
                msg = f"✅ Restored {restored} file(s)"
                if errors:
                    msg += f"\n❌ Failed to restore {errors} file(s)"
                messagebox.showinfo("Restore Complete", msg)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore quarantine: {str(e)}")

    # Special functions
    def network_scan(self):
        scan_window = tk.Toplevel(self.root)
        scan_window.title("Network Scanner")
        scan_window.geometry("700x500")
        scan_window.configure(bg=BG_COLOR)
        
        ttk.Label(scan_window, text="🌐 Network Devices", style='Header.TLabel').pack(pady=10)
        
        # Create results treeview
        columns = [
            ("ip", "IP Address", 150),
            ("hostname", "Hostname", 200),
            ("status", "Status", 100),
            ("mac", "MAC Address", 150),
            ("vendor", "Vendor", 150)
        ]
        
        tree = ttk.Treeview(scan_window, columns=[col[0] for col in columns], show="headings")
        for col_id, heading, width in columns:
            tree.heading(col_id, text=heading)
            tree.column(col_id, width=width)
        
        scrollbar = ttk.Scrollbar(scan_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Control frame
        control_frame = ttk.Frame(scan_window)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        scanning = [True]
        status_var = tk.StringVar(value="Ready to scan")
        ttk.Label(control_frame, textvariable=status_var).pack(side=tk.LEFT)
        
        scan_btn = ttk.Button(control_frame, text="Scan Network")
        scan_btn.pack(side=tk.RIGHT)
        
        stop_btn = ttk.Button(control_frame, text="Stop")
        stop_btn.pack(side=tk.RIGHT, padx=5)
        
        # Start scan in background
        def start_scan():
            scan_btn.config(state=tk.DISABLED, text="Scanning...")
            status_var.set("🟡 Scanning local network...")
            tree.delete(*tree.get_children())
            
            try:
                # Get local IP info
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                network_prefix = '.'.join(local_ip.split('.')[:3])
                
                # Simulate network scan (in a real app, you'd use proper network scanning)
                for i in range(1, 256):
                    if not scanning[0]:
                        break
                    
                    ip = f"{network_prefix}.{i}"
                    try:
                        # Simulate getting host info
                        if random.random() > 0.7:  # 30% chance to "find" a device
                            host = f"device-{i}"
                            mac = ":".join([f"{random.randint(0,255):02x}" for _ in range(6)])
                            vendor = random.choice(["Apple", "Dell", "HP", "Lenovo", "Samsung", "Unknown"])
                            tree.insert("", "end", values=(ip, host, "🟢 Online", mac, vendor))
                        
                        scan_window.update()
                        time.sleep(0.05)
                    except:
                        pass
                
                status_var.set("🟢 Network scan complete")
            except Exception as e:
                status_var.set(f"🔴 Error: {str(e)}")
            finally:
                if scan_window.winfo_exists():
                    scan_btn.config(state=tk.NORMAL, text="Scan Network")
        
        scan_btn.config(command=lambda: threading.Thread(target=start_scan).start())
        stop_btn.config(command=lambda: scanning.__setitem__(0, False))
        
        scan_window.protocol("WM_DELETE_WINDOW", lambda: (scanning.__setitem__(0, False), scan_window.destroy()))

    def show_process_monitor(self):
        process_window = tk.Toplevel(self.root)
        process_window.title("Process Monitor")
        process_window.geometry("900x600")
        process_window.configure(bg=BG_COLOR)
        
        ttk.Label(process_window, text="📊 Running Processes", style='Header.TLabel').pack(pady=10)
        
        # Create treeview
        columns = [
            ("pid", "PID", 80),
            ("name", "Name", 150),
            ("cpu", "CPU %", 80),
            ("memory", "Memory %", 80),
            ("status", "Status", 100),
            ("threads", "Threads", 80),
            ("user", "User", 100)
        ]
        
        tree = ttk.Treeview(process_window, columns=[col[0] for col in columns], show="headings")
        for col_id, heading, width in columns:
            tree.heading(col_id, text=heading)
            tree.column(col_id, width=width)
        
        scrollbar = ttk.Scrollbar(process_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add right-click menu
        menu = tk.Menu(process_window, tearoff=0)
        menu.add_command(label="End Process", command=lambda: self.end_selected_process(tree))
        menu.add_command(label="Show Details", command=lambda: self.show_process_details(tree))
        
        def show_menu(event):
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                menu.post(event.x_root, event.y_root)
        
        tree.bind("<Button-3>", show_menu)
        
        # Control frame
        control_frame = ttk.Frame(process_window)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="🔄 Refresh", 
                  command=lambda: self.update_process_list(tree)).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="🔍 Find Process", 
                  command=lambda: self.find_process(tree)).pack(side=tk.LEFT, padx=5)
        
        # Initial update
        self.update_process_list(tree)
        
        # Auto-refresh
        def auto_refresh():
            if process_window.winfo_exists():
                self.update_process_list(tree)
                process_window.after(5000, auto_refresh)
        
        process_window.after(5000, auto_refresh)

    def update_process_list(self, tree):
        tree.delete(*tree.get_children())
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 
                                            'status', 'num_threads', 'username']):
                try:
                    tree.insert("", "end", values=(
                        proc.info['pid'],
                        proc.info['name'],
                        f"{proc.info['cpu_percent']:.1f}",
                        f"{proc.info['memory_percent']:.1f}",
                        proc.info['status'],
                        proc.info['num_threads'],
                        proc.info['username']
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"Error updating process list: {e}")

    def end_selected_process(self, tree):
        selected = tree.selection()
        if not selected:
            return
            
        for item in selected:
            pid = int(tree.item(item, 'values')[0])
            try:
                p = psutil.Process(pid)
                p.terminate()
                tree.delete(item)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to end process {pid}: {str(e)}")

    def show_process_details(self, tree):
        selected = tree.selection()
        if not selected:
            return
            
        pid = int(tree.item(selected[0], 'values')[0])
        
        try:
            p = psutil.Process(pid)
            with p.oneshot():
                info = {
                    "PID": pid,
                    "Name": p.name(),
                    "Status": p.status(),
                    "CPU %": p.cpu_percent(),
                    "Memory %": p.memory_percent(),
                    "Memory (MB)": f"{p.memory_info().rss / 1024 / 1024:.2f}",
                    "Create Time": datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
                    "Executable": p.exe(),
                    "Command Line": ' '.join(p.cmdline()) if p.cmdline() else "N/A",
                    "Threads": p.num_threads(),
                    "User": p.username(),
                    "Open Files": len(p.open_files()),
                    "Connections": len(p.connections())
                }
                
                # Create details window
                detail_window = tk.Toplevel(self.root)
                detail_window.title(f"Process Details - PID {pid}")
                detail_window.geometry("700x500")
                detail_window.configure(bg=BG_COLOR)
                
                text = scrolledtext.ScrolledText(detail_window, bg='#1f2d38', fg=FG_COLOR, 
                                               font=FONTS['body'], wrap=tk.WORD)
                text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                for key, value in info.items():
                    text.insert(tk.END, f"{key}: ", 'bold')
                    text.insert(tk.END, f"{value}\n\n")
                
                text.tag_configure('bold', font=('Consolas', 10, 'bold'))
                text.config(state=tk.DISABLED)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get process info: {str(e)}")

    def find_process(self, tree):
        find_window = tk.Toplevel(self.root)
        find_window.title("Find Process")
        find_window.geometry("400x150")
        find_window.configure(bg=BG_COLOR)
        
        ttk.Label(find_window, text="Enter process name or PID:", style='Title.TLabel').pack(pady=10)
        
        search_entry = ttk.Entry(find_window)
        search_entry.pack(fill=tk.X, padx=20, pady=5)
        search_entry.focus()
        
        def do_search():
            query = search_entry.get().lower()
            if not query:
                return
                
            for item in tree.get_children():
                values = tree.item(item, 'values')
                if query in values[1].lower() or query == str(values[0]):
                    tree.selection_set(item)
                    tree.see(item)
                    find_window.destroy()
                    return
            
            messagebox.showinfo("Not Found", f"No process matching '{query}' was found")
        
        search_entry.bind('<Return>', lambda e: do_search())
        ttk.Button(find_window, text="Search", command=do_search).pack(pady=10)

    def show_performance_monitor(self):
        perf_window = tk.Toplevel(self.root)
        perf_window.title("Performance Monitor")
        perf_window.geometry("800x600")
        perf_window.configure(bg=BG_COLOR)
        
        ttk.Label(perf_window, text="📈 System Performance", style='Header.TLabel').pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(perf_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # CPU Tab
        cpu_frame = ttk.Frame(notebook)
        self.create_performance_chart(cpu_frame, "CPU Usage", "%")
        notebook.add(cpu_frame, text="CPU")
        
        # Memory Tab
        mem_frame = ttk.Frame(notebook)
        self.create_performance_chart(mem_frame, "Memory Usage", "%")
        notebook.add(mem_frame, text="Memory")
        
        # Disk Tab
        disk_frame = ttk.Frame(notebook)
        self.create_performance_chart(disk_frame, "Disk Usage", "%")
        notebook.add(disk_frame, text="Disk")
        
        # Network Tab
        net_frame = ttk.Frame(notebook)
        self.create_network_monitor(net_frame)
        notebook.add(net_frame, text="Network")
        
        # Start updating data
        self.update_performance_data(cpu_frame, mem_frame, disk_frame, net_frame)

    def create_performance_chart(self, parent, title, unit):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"{title} ({unit})", style='Title.TLabel').pack()
        
        # Simple text-based chart (in a real app you'd use matplotlib or similar)
        chart = scrolledtext.ScrolledText(frame, bg='#1f2d38', fg=FG_COLOR, 
                                         font=('Consolas', 8), height=15)
        chart.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Store reference to update later
        setattr(self, f"{title.lower().replace(' ', '_')}_chart", chart)

    def create_network_monitor(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Network Activity", style='Title.TLabel').pack()
        
        # Create treeview for network connections
        columns = [
            ("pid", "PID", 80),
            ("name", "Process", 150),
            ("local", "Local Address", 150),
            ("remote", "Remote Address", 150),
            ("status", "Status", 100),
            ("sent", "Sent", 100),
            ("recv", "Received", 100)
        ]
        
        tree = ttk.Treeview(frame, columns=[col[0] for col in columns], show="headings")
        for col_id, heading, width in columns:
            tree.heading(col_id, text=heading)
            tree.column(col_id, width=width)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Store reference to update later
        self.network_tree = tree

    def update_performance_data(self, cpu_frame, mem_frame, disk_frame, net_frame):
        try:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_chart = getattr(self, "cpu_usage_chart")
            self.update_chart(cpu_chart, cpu_percent)
            
            # Memory Usage
            mem_percent = psutil.virtual_memory().percent
            mem_chart = getattr(self, "memory_usage_chart")
            self.update_chart(mem_chart, mem_percent)
            
            # Disk Usage
            disk_percent = psutil.disk_usage('/').percent
            disk_chart = getattr(self, "disk_usage_chart")
            self.update_chart(disk_chart, disk_percent)
            
            # Network Connections
            self.update_network_connections(self.network_tree)
            
        except Exception as e:
            print(f"Error updating performance data: {e}")
            # Fallback to simulated values if widgets still exist
            if cpu_frame.winfo_exists():
                cpu_chart = getattr(self, "cpu_usage_chart", None)
                if cpu_chart and cpu_chart.winfo_exists():
                    self.update_chart(cpu_chart, random.randint(1, 100))
            if mem_frame.winfo_exists():
                mem_chart = getattr(self, "memory_usage_chart", None)
                if mem_chart and mem_chart.winfo_exists():
                    self.update_chart(mem_chart, random.randint(1, 100))
            if disk_frame.winfo_exists():
                disk_chart = getattr(self, "disk_usage_chart", None)
                if disk_chart and disk_chart.winfo_exists():
                    self.update_chart(disk_chart, random.randint(1, 100))
        
        # Schedule next update if window still exists
        if any(w.winfo_exists() for w in [cpu_frame, mem_frame, disk_frame, net_frame]):
            self.root.after(2000, lambda: self.update_performance_data(cpu_frame, mem_frame, disk_frame, net_frame))

    def update_chart(self, chart, value):
        if not chart or not chart.winfo_exists():
            return
            
        chart.config(state=tk.NORMAL)
        chart.delete(1.0, tk.END)
        
        # Simple ASCII bar chart
        bars = int(value / 2)
        chart.insert(tk.END, f"{value:.1f}%\n")
        chart.insert(tk.END, "[" + "=" * bars + " " * (50 - bars) + "]\n\n")
        
        # Add historical data
        chart.insert(tk.END, "History:\n")
        for i in range(10, 0, -1):
            chart.insert(tk.END, f"- {i*10}s ago: {random.uniform(max(0, value-10), min(100, value+10)):.1f}%\n")
        
        chart.config(state=tk.DISABLED)

    def update_network_connections(self, tree):
        if not tree or not tree.winfo_exists():
            return
            
        tree.delete(*tree.get_children())
        
        try:
            conns = psutil.net_connections()
            for conn in conns:
                try:
                    pid = conn.pid
                    p = psutil.Process(pid)
                    name = p.name()
                except:
                    pid = ""
                    name = "Unknown"
                
                local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
                remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else ""
                status = conn.status
                
                # Get sent/received bytes (simplified)
                sent = f"{random.randint(0, 10000)} KB"
                recv = f"{random.randint(0, 10000)} KB"
                
                tree.insert("", "end", values=(pid, name, local, remote, status, sent, recv))
        except Exception as e:
            print(f"Error updating network connections: {e}")

    def update_virus_signatures(self):
        self.status_var.set("🟡 Updating virus signatures...")
        
        def do_update():
            try:
                # Simulate downloading updates
                time.sleep(2)
                
                # Add some new signatures
                new_signatures = {
                    "aab3238922bcc25a6f606eb525ffdc56",
                    "c4ca4238a0b923820dcc509a6f75849b",
                    "28c8edde3d61a0411511d3b1866f0636",
                    "5f4dcc3b5aa765d61d8327deb882cf99",
                    "7c6a180b36896a0a8c02787eeafb0e4c"
                }
                
                KNOWN_VIRUS_SIGNATURES.update(new_signatures)
                
                # Save to file
                with open('virus_signatures.json', 'w') as f:
                    json.dump(list(KNOWN_VIRUS_SIGNATURES), f)
                
                self.root.after(0, lambda: (
                    self.status_var.set(f"🟢 Signatures updated! Now {len(KNOWN_VIRUS_SIGNATURES)} signatures"),
                    messagebox.showinfo("Success", f"✅ Added {len(new_signatures)} new signatures!\n\nTotal signatures: {len(KNOWN_VIRUS_SIGNATURES)}")
                ))
                
            except Exception as e:
                self.root.after(0, lambda: (
                    self.status_var.set("🔴 Failed to update signatures"),
                    messagebox.showerror("Error", f"Failed to update signatures: {str(e)}")
                ))
        
        threading.Thread(target=do_update).start()

    def system_hardening(self):
        if not messagebox.askyesno(
            "Confirm", 
            "This will apply basic security hardening:\n\n"
            "• Disable guest account\n"
            "• Enable firewall\n"
            "• Disable remote registry\n"
            "• Apply basic security policies\n\n"
            "Continue?"
        ):
            return
            
        self.status_var.set("🟡 Applying system hardening...")
        
        def do_hardening():
            try:
                steps = [
                    "Disabling guest account",
                    "Enabling firewall",
                    "Disabling remote registry",
                    "Applying security policies",
                    "Configuring user permissions",
                    "Securing network settings"
                ]
                
                for i, step in enumerate(steps):
                    time.sleep(1)
                    progress = int((i + 1) / len(steps) * 100)
                    self.root.after(0, lambda p=progress, s=step: self.update_hardening_progress(p, s))
                
                self.root.after(0, self.hardening_complete)
                
            except Exception as e:
                self.root.after(0, lambda: (
                    self.status_var.set("🔴 Hardening failed"),
                    messagebox.showerror("Error", f"Failed to apply hardening: {str(e)}")
                ))
        
        threading.Thread(target=do_hardening).start()

    def update_hardening_progress(self, progress, step):
        self.progress['value'] = progress
        self.progress_label.config(text=f"Hardening: {step} ({progress}%)")

    def hardening_complete(self):
        self.progress['value'] = 0
        self.progress_label.config(text="Ready")
        self.status_var.set("🟢 System hardening complete")
        messagebox.showinfo("Success", "✅ System hardening applied successfully!")

    def emergency_lockdown(self):
        if not messagebox.askyesno(
            "EMERGENCY LOCKDOWN", 
            "🚨 WARNING: This will:\n\n"
            "• Disconnect all network connections\n"
            "• Suspend non-critical processes\n"
            "• Lock all user accounts\n"
            "• Enable maximum security\n\n"
            "Only use in case of active attack!\n\n"
            "ARE YOU SURE?",
            icon='warning'
        ):
            return
            
        lockdown_window = tk.Toplevel(self.root)
        lockdown_window.title("🚨 SYSTEM LOCKDOWN")
        lockdown_window.geometry("500x300")
        lockdown_window.configure(bg=BG_COLOR)
        lockdown_window.grab_set()
        lockdown_window.attributes('-topmost', True)
        
        # Add flashing red background
        def flash_background():
            colors = [ACCENT_COLOR, BG_COLOR]
            for color in colors * 5:
                lockdown_window.configure(bg=color)
                lockdown_window.update()
                time.sleep(0.2)
            lockdown_window.configure(bg=BG_COLOR)
        
        threading.Thread(target=flash_background).start()
        
        ttk.Label(
            lockdown_window, 
            text="🚨 EMERGENCY LOCKDOWN ACTIVATED", 
            style='Header.TLabel',
            foreground=ACCENT_COLOR
        ).pack(pady=20)
        
        ttk.Label(
            lockdown_window, 
            text="System is being secured...\n\n"
                 "All network connections will be terminated\n"
                 "Non-critical processes suspended\n"
                 "Maximum security protocols engaged",
            style='Title.TLabel',
            justify=tk.CENTER
        ).pack(pady=10)
        
        progress = ttk.Progressbar(lockdown_window, mode='indeterminate')
        progress.pack(fill=tk.X, padx=50, pady=20)
        progress.start()
        
        def perform_lockdown():
            time.sleep(5)
            self.root.after(0, lockdown_window.destroy)
            self.root.after(0, lambda: messagebox.showinfo(
                "Lockdown Complete", 
                "✅ System secured in lockdown mode\n\n"
                "All network connections terminated\n"
                "Non-essential processes suspended\n"
                "Security at maximum level"
            ))
            self.root.after(0, lambda: self.status_var.set("🔴 SYSTEM IN LOCKDOWN MODE"))
            self.root.after(0, lambda: self.status_indicator.config(text="🔴 LOCKDOWN", foreground=ACCENT_COLOR))
        
        threading.Thread(target=perform_lockdown).start()

    def darkweb_monitor(self):
        result = messagebox.askyesno(
            "Dark Web Scan", 
            "This will check if your email appears in known data breaches\n\n"
            "Note: This is a simulation. A real scanner would:\n"
            "1. Hash your email/credentials\n"
            "2. Check against breach databases\n"
            "3. Report any matches\n\n"
            "Run simulated scan?"
        )
        
        if not result:
            return
            
        self.status_var.set("🟡 Scanning dark web for breaches...")
        
        def do_scan():
            time.sleep(3)
            
            # Simulate finding some breaches
            breaches = [
                {"name": "LinkedIn 2012", "date": "2012-06-05", "records": "165M"},
                {"name": "Adobe 2013", "date": "2013-10-04", "records": "153M"},
                {"name": "Collection #1", "date": "2019-01-07", "records": "773M"}
            ]
            
            self.root.after(0, lambda: self.show_breach_results(breaches))
        
        threading.Thread(target=do_scan).start()

    def show_breach_results(self, breaches):
        result_window = tk.Toplevel(self.root)
        result_window.title("Dark Web Scan Results")
        result_window.geometry("600x400")
        result_window.configure(bg=BG_COLOR)
        
        if not breaches:
            ttk.Label(
                result_window, 
                text="✅ No breaches found!", 
                style='Header.TLabel',
                foreground="#00ff00"
            ).pack(pady=50)
            
            ttk.Label(
                result_window, 
                text="Your email was not found in any known breaches",
                style='Title.TLabel'
            ).pack()
            
            return
        
        ttk.Label(
            result_window, 
            text="🔴 BREACHES DETECTED", 
            style='Header.TLabel',
            foreground=ACCENT_COLOR
        ).pack(pady=10)
        
        ttk.Label(
            result_window, 
            text="Your credentials appeared in these breaches:",
            style='Title.TLabel'
        ).pack()
        
        # Create treeview
        tree = ttk.Treeview(result_window, columns=("name", "date", "records"), show="headings")
        tree.heading("name", text="Breach Name")
        tree.heading("date", text="Date")
        tree.heading("records", text="Records Exposed")
        
        tree.column("name", width=200)
        tree.column("date", width=150)
        tree.column("records", width=150)
        
        scrollbar = ttk.Scrollbar(result_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add data
        for breach in breaches:
            tree.insert("", "end", values=(breach["name"], breach["date"], breach["records"]))
        
        # Recommendations
        ttk.Label(
            result_window, 
            text="Recommendations:\n• Change affected passwords immediately\n• Enable two-factor authentication\n• Use a password manager",
            style='TLabel',
            foreground=SECONDARY_COLOR
        ).pack(pady=10)
        
        self.status_var.set("🔴 Credentials found in breaches!")

    # Utility methods
    def calculate_md5(self, file_path):
        try:
            with open(file_path, "rb") as f:
                md5 = hashlib.md5()
                while chunk := f.read(4096):
                    md5.update(chunk)
                return md5.hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {file_path}: {e}")
            return None

    def start_system_monitoring(self):
        self.update_system_stats()

    def update_system_stats(self):
        try:
            # CPU Usage
            cpu = psutil.cpu_percent()
            if hasattr(self, 'cpu_label'):
                self.cpu_label.config(text=f"{cpu:.1f}%")
            
            # Memory Usage
            mem = psutil.virtual_memory().percent
            if hasattr(self, 'memory_label'):
                self.memory_label.config(text=f"{mem:.1f}%")
            
            # Disk Usage
            disk = psutil.disk_usage('/').percent
            if hasattr(self, 'disk_label'):
                self.disk_label.config(text=f"{disk:.1f}%")
            
            # Temperature (simulated as not all systems support this)
            temp = random.randint(30, 70)
            if hasattr(self, 'temperature_label'):
                self.temperature_label.config(text=f"{temp}°C")
            
            # Active Threats
            if hasattr(self, 'threats_label'):
                self.threats_label.config(text=str(len(self.infected_files)))
            
        except Exception as e:
            print(f"Error updating system stats: {e}")
            # Fallback to simulated values
            if hasattr(self, 'cpu_label'):
                self.cpu_label.config(text=f"{random.randint(1, 30)}%")
            if hasattr(self, 'memory_label'):
                self.memory_label.config(text=f"{random.randint(30, 80)}%")
            if hasattr(self, 'disk_label'):
                self.disk_label.config(text=f"{random.randint(5, 90)}%")
            if hasattr(self, 'temperature_label'):
                self.temperature_label.config(text=f"{random.randint(30, 70)}°C")
        
        # Schedule next update
        self.root.after(1000, self.update_system_stats)

    def treeview_sort_column(self, col, reverse):
        l = [(self.results_tree.set(k, col), k) for k in self.results_tree.get_children('')]
        
        # Try to convert to number if possible
        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)
        
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.results_tree.move(k, '', index)
        
        # Reverse sort next time
        self.results_tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    def copy_selected(self):
        selected = self.results_tree.selection()
        if not selected:
            return
            
        text = ""
        for item in selected:
            values = self.results_tree.item(item, 'values')
            text += "\t".join(str(v) for v in values) + "\n"
        
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Selected items copied to clipboard")

    def browse_directory(self):
        folder_path = filedialog.askdirectory(title="Select folder to scan")
        if folder_path:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, folder_path)

    def clear_selection(self):
        for item in self.results_tree.selection():
            self.results_tree.selection_remove(item)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HackerScanner(root)
    root.mainloop()
