import os
import hashlib
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import threading
import time
import random

# Create quarantine directory if it doesn't exist
QUARANTINE_DIR = os.path.join(os.getcwd(), "quarantine")
if not os.path.exists(QUARANTINE_DIR):
    os.makedirs(QUARANTINE_DIR)

# Example known virus signatures (use real ones in practice)
KNOWN_VIRUS_SIGNATURES = {
    "5d41402abc4b2a76b9719d911017c592",  # Example hash
    "e99a18c428cb38d5f260853678922e03",
    "098f6bcd4621d373cade4e832627b4f6",
    "a7f5f35426b927411fc9231b56382173",
    "d41d8cd98f00b204e9800998ecf8427e",
}

# Hacker-themed color scheme
BG_COLOR = "#0d1117"  # Dark blue-black
FG_COLOR = "#00ff41"  # Matrix green
ACCENT_COLOR = "#ff003c"  # Bright red
SECONDARY_COLOR = "#00bfff"  # Bright blue
TEXT_COLOR = "#f0f0f0"  # Light gray

# Fonts
HEADER_FONT = ("Consolas", 18, "bold")
TITLE_FONT = ("Consolas", 14, "bold")
BODY_FONT = ("Consolas", 10)
BUTTON_FONT = ("Consolas", 10, "bold")

class HackerScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 CYBER GUARDIAN - Advanced Threat Detection")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)
        
        # Initialize state
        self.scan_active = False
        self.scan_thread = None
        self.total_files = 0
        self.scanned_files = 0
        self.infected_files = []
        self.current_scan_folder = ""
        
        # Setup UI
        self.setup_ui()
        
        # Load icons
        self.load_icons()
        
        # Create header frame
        self.create_header()
        
        # Create main content area
        self.create_main_content()
        
        # Create status bar
        self.create_status_bar()
        
        # Start system monitoring
        self.update_system_stats()

    def load_icons(self):
        try:
            # Create simple icons using PIL
            self.scan_icon = self.create_icon("🔍", FG_COLOR)
            self.settings_icon = self.create_icon("⚙️", SECONDARY_COLOR)
            self.quarantine_icon = self.create_icon("☣️", ACCENT_COLOR)
            self.report_icon = self.create_icon("📊", SECONDARY_COLOR)
            self.shield_icon = self.create_icon("🛡️", "#00ff00")
            self.virus_icon = self.create_icon("🦠", ACCENT_COLOR)
        except Exception as e:
            print(f"Error creating icons: {e}")
            # Fallback to text if icons fail
            self.scan_icon = "🔍"
            self.settings_icon = "⚙️"
            self.quarantine_icon = "☣️"
            self.report_icon = "📊"
            self.shield_icon = "🛡️"
            self.virus_icon = "🦠"

    def create_icon(self, text, color, size=24):
        # Create a simple text-based icon
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        return text

    def setup_ui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=BODY_FONT)
        style.configure('Header.TLabel', background=BG_COLOR, foreground=FG_COLOR, font=HEADER_FONT)
        style.configure('Title.TLabel', background=BG_COLOR, foreground=SECONDARY_COLOR, font=TITLE_FONT)
        style.configure('TButton', background=BG_COLOR, foreground=TEXT_COLOR, font=BUTTON_FONT, 
                        borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#1f2d38')])
        style.configure('Red.TButton', background=BG_COLOR, foreground=ACCENT_COLOR, font=BUTTON_FONT)
        style.configure('Green.TButton', background=BG_COLOR, foreground="#00ff00", font=BUTTON_FONT)
        style.configure('TProgressbar', thickness=20, background=FG_COLOR, troughcolor='#1f2d38')
        style.configure('Status.TLabel', background='#1f2d38', foreground=FG_COLOR, font=("Consolas", 8))
        style.configure('TEntry', fieldbackground='#1f2d38', foreground=FG_COLOR, insertcolor=FG_COLOR)
        style.configure('TCombobox', fieldbackground='#1f2d38', foreground=FG_COLOR)
        style.configure('TCheckbutton', background=BG_COLOR, foreground=FG_COLOR)
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
        
        # Status indicator
        self.status_indicator = ttk.Label(header_frame, text="🟢 SYSTEM SECURE", 
                                        foreground="#00ff00", style='Title.TLabel')
        self.status_indicator.pack(side=tk.RIGHT, padx=10)

    def create_main_content(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - controls
        left_frame = ttk.Frame(main_frame, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Scan section
        scan_frame = ttk.LabelFrame(left_frame, text="🔍 Scan Operations", padding=10)
        scan_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(scan_frame, text="Target Directory:").pack(anchor=tk.W)
        
        dir_frame = ttk.Frame(scan_frame)
        dir_frame.pack(fill=tk.X, pady=5)
        
        self.dir_entry = ttk.Entry(dir_frame)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(dir_frame, text="📂", width=3, command=self.browse_directory)
        browse_btn.pack(side=tk.RIGHT)
        
        scan_btn = ttk.Button(scan_frame, text=f"{self.scan_icon} Start Deep Scan", 
                             command=self.start_scan, style='Green.TButton')
        scan_btn.pack(fill=tk.X, pady=5)
        
        # Quarantine section
        quarantine_frame = ttk.LabelFrame(left_frame, text="☣️ Quarantine Management", padding=10)
        quarantine_frame.pack(fill=tk.X, pady=(10, 0))
        
        quarantine_btn = ttk.Button(quarantine_frame, text=f"{self.quarantine_icon} View Quarantine", 
                                  command=self.view_quarantine)
        quarantine_btn.pack(fill=tk.X, pady=2)
        
        restore_btn = ttk.Button(quarantine_frame, text="🔄 Restore All", command=self.restore_quarantine)
        restore_btn.pack(fill=tk.X, pady=2)
        
        # Statistics panel
        stats_frame = ttk.LabelFrame(left_frame, text="📊 System Stats", padding=10)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.cpu_label = ttk.Label(stats_frame, text="CPU Usage: --%")
        self.cpu_label.pack(anchor=tk.W)
        
        self.mem_label = ttk.Label(stats_frame, text="Memory Usage: --%")
        self.mem_label.pack(anchor=tk.W)
        
        self.threat_label = ttk.Label(stats_frame, text="Active Threats: 0", foreground=ACCENT_COLOR)
        self.threat_label.pack(anchor=tk.W)
        
        # Right panel - results
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Scan progress
        progress_frame = ttk.Frame(right_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to scan...")
        self.progress_label.pack(anchor=tk.W)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill=tk.X)
        
        # Results display
        results_frame = ttk.LabelFrame(right_frame, text="📋 Scan Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create results treeview
        columns = ("file", "status", "path")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", selectmode="extended")
        
        # Configure columns
        self.results_tree.heading("file", text="File", anchor=tk.W)
        self.results_tree.heading("status", text="Status", anchor=tk.W)
        self.results_tree.heading("path", text="Path", anchor=tk.W)
        
        self.results_tree.column("file", width=150)
        self.results_tree.column("status", width=100)
        self.results_tree.column("path", width=400)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.clean_btn = ttk.Button(action_frame, text=f"{self.virus_icon} Quarantine Selected", 
                                  state=tk.DISABLED, command=self.clean_selected, style='Red.TButton')
        self.clean_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.stop_btn = ttk.Button(action_frame, text="⏹️ Stop Scan", 
                                  command=self.stop_scan, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.RIGHT)

    def create_status_bar(self):
        status_frame = ttk.Frame(self.root, style='Status.TFrame')
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="🟢 System Secure | Ready for scan")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Status.TLabel')
        status_label.pack(side=tk.LEFT, padx=10)
        
        # Add signature count
        sig_count = ttk.Label(status_frame, text=f"Signatures: {len(KNOWN_VIRUS_SIGNATURES)}", 
                             style='Status.TLabel')
        sig_count.pack(side=tk.RIGHT, padx=10)

    def browse_directory(self):
        folder_path = filedialog.askdirectory(title="Select folder to scan")
        if folder_path:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, folder_path)

    def start_scan(self):
        folder_path = self.dir_entry.get()
        if not folder_path or not os.path.exists(folder_path):
            messagebox.showerror("Error", "Please select a valid directory to scan")
            return
            
        if self.scan_active:
            messagebox.showwarning("Warning", "Scan already in progress")
            return
            
        # Reset UI for new scan
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
        
        # Start scan in separate thread
        self.scan_thread = threading.Thread(target=self.scan_directory, args=(folder_path,))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        # Start progress monitoring
        self.monitor_progress()

    def scan_directory(self, directory):
        self.scanned_files = 0
        self.total_files = 0
        
        # Count files first for progress
        for root, _, files in os.walk(directory):
            self.total_files += len(files)
        
        # Reset counters
        self.scanned_files = 0
        infected_count = 0
        
        # Perform actual scan
        for root, _, files in os.walk(directory):
            for file in files:
                if not self.scan_active:
                    return
                    
                path = os.path.join(root, file)
                file_hash = self.calculate_md5(path)
                
                # Update progress
                self.scanned_files += 1
                
                if file_hash in KNOWN_VIRUS_SIGNATURES:
                    infected_count += 1
                    self.infected_files.append(path)
                    self.add_result(file, "INFECTED", path, "infected")
                else:
                    self.add_result(file, "Clean", path, "clean")
                
                # Slow down for demonstration
                time.sleep(0.01)
        
        # Update UI when scan completes
        self.scan_active = False
        self.root.after(0, self.scan_completed, infected_count)

    def add_result(self, file, status, path, tag):
        self.root.after(0, lambda: 
            self.results_tree.insert("", "end", values=(file, status, path), tags=(tag,)))
        
        # Apply tag styling
        if tag == "infected":
            self.results_tree.tag_configure(tag, foreground=ACCENT_COLOR)
        else:
            self.results_tree.tag_configure(tag, foreground=FG_COLOR)

    def monitor_progress(self):
        if not self.scan_active:
            return
            
        if self.total_files > 0:
            progress = int((self.scanned_files / self.total_files) * 100)
            self.progress['value'] = progress
            self.progress_label.config(
                text=f"Scanning... {self.scanned_files}/{self.total_files} files ({progress}%)"
            )
            
        # Continue monitoring
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
            messagebox.showinfo(
                "Scan Complete",
                "✅ No viruses found.\n\nSystem is secure!"
            )

    def stop_scan(self):
        self.scan_active = False
        self.progress_label.config(text="Scan stopped by user")
        self.status_var.set("🟠 Scan stopped by user")
        self.status_indicator.config(text="🟠 SCAN STOPPED", foreground="orange")
        self.stop_btn.config(state=tk.DISABLED)

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
            # Update UI
            for item in selected:
                self.results_tree.delete(item)
                
            messagebox.showinfo(
                "Success",
                f"✅ {len(files_to_quarantine)} file(s) moved to quarantine"
            )
            
            # Update status
            remaining_infected = len(self.infected_files) - len(files_to_quarantine)
            if remaining_infected > 0:
                self.status_var.set(f"🟠 {remaining_infected} threats remain!")
                self.status_indicator.config(text="🟠 THREATS DETECTED", foreground="orange")
            else:
                self.status_var.set("🟢 All threats quarantined | System Secure")
                self.status_indicator.config(text="🟢 SYSTEM SECURE", foreground="#00ff00")
                self.clean_btn.config(state=tk.DISABLED)

    def view_quarantine(self):
        quarantine_window = tk.Toplevel(self.root)
        quarantine_window.title("Quarantine Manager")
        quarantine_window.geometry("600x400")
        quarantine_window.configure(bg=BG_COLOR)
        quarantine_window.resizable(True, True)
        
        # Create UI
        ttk.Label(quarantine_window, text="☣️ Quarantined Files", style='Header.TLabel').pack(pady=10)
        
        # Create listbox
        frame = ttk.Frame(quarantine_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        listbox = tk.Listbox(frame, bg='#1f2d38', fg=FG_COLOR, selectbackground='#2a3b45', 
                            font=BODY_FONT, selectmode=tk.EXTENDED)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Populate listbox
        try:
            files = os.listdir(QUARANTINE_DIR)
            for file in files:
                listbox.insert(tk.END, file)
        except Exception as e:
            listbox.insert(tk.END, f"Error accessing quarantine: {str(e)}")
        
        # Action buttons
        btn_frame = ttk.Frame(quarantine_window)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Restore Selected", 
                  command=lambda: self.restore_from_quarantine(listbox)).pack(side=tk.LEFT)
        
        ttk.Button(btn_frame, text="Delete Permanently", style='Red.TButton',
                  command=lambda: self.delete_from_quarantine(listbox)).pack(side=tk.RIGHT)

    def restore_from_quarantine(self, listbox):
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select files to restore")
            return
            
        restored = 0
        for index in selected:
            file = listbox.get(index)
            src = os.path.join(QUARANTINE_DIR, file)
            dest = os.path.join(self.current_scan_folder, file) if self.current_scan_folder else os.getcwd()
            
            try:
                shutil.move(src, dest)
                restored += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore {file}: {str(e)}")
        
        if restored > 0:
            messagebox.showinfo("Success", f"✅ Restored {restored} file(s)")
            # Refresh list
            listbox.delete(0, tk.END)
            for file in os.listdir(QUARANTINE_DIR):
                listbox.insert(tk.END, file)

    def delete_from_quarantine(self, listbox):
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select files to delete")
            return
            
        if not messagebox.askyesno("Confirm", "Permanently delete selected files? This cannot be undone."):
            return
            
        deleted = 0
        for index in selected:
            file = listbox.get(index)
            path = os.path.join(QUARANTINE_DIR, file)
            
            try:
                os.remove(path)
                deleted += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete {file}: {str(e)}")
        
        if deleted > 0:
            messagebox.showinfo("Success", f"🗑️ Permanently deleted {deleted} file(s)")
            # Refresh list
            listbox.delete(0, tk.END)
            for file in os.listdir(QUARANTINE_DIR):
                listbox.insert(tk.END, file)

    def restore_quarantine(self):
        if not os.listdir(QUARANTINE_DIR):
            messagebox.showinfo("Info", "Quarantine is empty")
            return
            
        if messagebox.askyesno("Confirm", "Restore all files from quarantine?"):
            restored = 0
            errors = 0
            for file in os.listdir(QUARANTINE_DIR):
                src = os.path.join(QUARANTINE_DIR, file)
                dest = os.path.join(self.current_scan_folder, file) if self.current_scan_folder else os.getcwd()
                
                try:
                    shutil.move(src, dest)
                    restored += 1
                except Exception as e:
                    errors += 1
                    print(f"Error restoring {file}: {e}")
            
            msg = f"✅ Restored {restored} file(s)"
            if errors:
                msg += f"\n❌ Failed to restore {errors} file(s)"
            messagebox.showinfo("Restore Complete", msg)

    def update_system_stats(self):
        # Simulate system monitoring
        cpu = random.randint(1, 30)
        mem = random.randint(30, 80)
        threats = len(self.infected_files)
        
        self.cpu_label.config(text=f"CPU Usage: {cpu}%")
        self.mem_label.config(text=f"Memory Usage: {mem}%")
        self.threat_label.config(text=f"Active Threats: {threats}")
        
        # Schedule next update
        self.root.after(3000, self.update_system_stats)

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

    def clean_files(self, files):
        if not os.path.exists(QUARANTINE_DIR):
            os.makedirs(QUARANTINE_DIR)

        success = 0
        for file in files:
            try:
                # Move file to quarantine
                shutil.move(file, os.path.join(QUARANTINE_DIR, os.path.basename(file)))
                success += 1
            except Exception as e:
                print(f"Error moving file {file}: {e}")
        
        return success > 0

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HackerScanner(root)
    root.mainloop()
