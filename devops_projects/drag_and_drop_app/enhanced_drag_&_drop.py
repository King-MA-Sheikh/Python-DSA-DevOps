import tkinter as tk
from tkinter import messagebox, filedialog
from tkinterdnd2 import DND_FILES, DND_TEXT, TkinterDnD
import os
import webbrowser
from datetime import datetime

class DragDropApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("King MA Sheikh")
        self.center_window(800, 600)
        self.configure(bg="#f0f0f0")

        # Custom theme colors
        self.bg_color = "#f0f0f0"
        self.listbox_bg = "#ffffff"
        self.button_bg = "#4a6fa5"
        self.button_fg = "#ffffff"
        self.highlight_color = "#e6f2ff"

        # Main header
        header = tk.Frame(self, bg=self.button_bg)
        header.pack(fill=tk.X, pady=(0, 10))
        tk.Label(header, text="Enhanced Drag & Drop Tool", 
                font=("Helvetica", 16, "bold"), 
                bg=self.button_bg, fg="white").pack(pady=10)

        # Instructions with icon
        instruction_frame = tk.Frame(self, bg=self.bg_color)
        instruction_frame.pack(fill=tk.X, padx=10)
        tk.Label(instruction_frame, 
                text="Drag any items here or click 'Add Files' to browse",
                font=("Arial", 12), 
                bg=self.bg_color).pack(side=tk.LEFT)

        # Main listbox with scrollbar
        list_frame = tk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame, 
            selectmode=tk.EXTENDED, 
            bg=self.listbox_bg,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            relief=tk.GROOVE,
            borderwidth=2,
            highlightthickness=0,
            activestyle="none"
        )
        self.listbox.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.listbox.yview)

        # Button panel
        btn_frame = tk.Frame(self, bg=self.bg_color)
        btn_frame.pack(pady=10)

        button_style = {
            "bg": self.button_bg,
            "fg": self.button_fg,
            "activebackground": "#3a5a8c",
            "activeforeground": "white",
            "font": ("Arial", 10),
            "borderwidth": 1,
            "relief": tk.RAISED,
            "padx": 10,
            "pady": 5
        }

        tk.Button(btn_frame, text="Add Files", command=self.browse_files, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear All", command=self.clear_list, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Count Items", command=self.show_count, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Remove Selected", command=self.remove_selected, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Open Selected", command=self.open_selected, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Export List", command=self.export_list, **button_style).pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status = tk.StringVar()
        self.status.set("Ready")
        status_bar = tk.Label(self, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#e0e0e0")
        status_bar.pack(fill=tk.X, pady=(5, 0))

        # Enable dropping files and text onto the listbox
        self.listbox.drop_target_register(DND_FILES, DND_TEXT)
        self.listbox.dnd_bind("<<Drop>>", self.on_drop)

        # Bind double-click to open files
        self.listbox.bind("<Double-Button-1>", self.open_selected)
        self.listbox.bind("<<ListboxSelect>>", self.update_status)

    def on_drop(self, event):
        """Handle dropped items - files, folders, or text"""
        try:
            # Try to process as files first
            paths = self.tk.splitlist(event.data)
            for path in paths:
                if path not in self.listbox.get(0, tk.END):
                    self.listbox.insert(tk.END, path)
                    self.colorize_item(path)
            self.status.set(f"Added {len(paths)} item(s)")
        except:
            # If not files, treat as plain text
            if event.data not in self.listbox.get(0, tk.END):
                self.listbox.insert(tk.END, event.data)
                self.status.set("Added text item")

    def colorize_item(self, path):
        """Colorize items based on their type (file/folder)"""
        index = self.listbox.size() - 1
        if os.path.isdir(path):
            self.listbox.itemconfig(index, {'fg': 'blue'})
        elif os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            if ext in ('.jpg', '.jpeg', '.png', '.gif', '.bmp'):
                self.listbox.itemconfig(index, {'fg': '#8e44ad'})
            elif ext in ('.txt', '.doc', '.docx', '.pdf', '.rtf'):
                self.listbox.itemconfig(index, {'fg': '#27ae60'})

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(title="Select files")
        if file_paths:
            for path in file_paths:
                if path not in self.listbox.get(0, tk.END):
                    self.listbox.insert(tk.END, path)
                    self.colorize_item(path)
            self.status.set(f"Added {len(file_paths)} item(s)")

    def clear_list(self):
        self.listbox.delete(0, tk.END)
        self.status.set("List cleared")

    def show_count(self):
        count = self.listbox.size()
        messagebox.showinfo("Item Count", f"{count} item(s) in the list")
        self.status.set(f"List contains {count} item(s)")

    def remove_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select items to remove")
            return
            
        for i in reversed(selected):
            self.listbox.delete(i)
        self.status.set(f"Removed {len(selected)} item(s)")

    def open_selected(self, event=None):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select items to open")
            return
            
        for i in selected:
            path = self.listbox.get(i)
            try:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        os.startfile(path)
                    else:
                        webbrowser.open(path)
                else:
                    # Try to open as URL if it's not a file path
                    if path.startswith(('http://', 'https://', 'www.')):
                        webbrowser.open(path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open {path}\n{str(e)}")
        self.status.set(f"Opened {len(selected)} item(s)")

    def export_list(self):
        if self.listbox.size() == 0:
            messagebox.showwarning("Empty List", "There are no items to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save File List"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(f"Item list exported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    for item in self.listbox.get(0, tk.END):
                        f.write(f"{item}\n")
                self.status.set(f"List exported to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Item list exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Could not export list\n{str(e)}")

    def update_status(self, event=None):
        selected = len(self.listbox.curselection())
        total = self.listbox.size()
        self.status.set(f"Total: {total} | Selected: {selected}")

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    app = DragDropApp()
    app.mainloop()
