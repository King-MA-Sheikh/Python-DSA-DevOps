import tkinter as tk
import customtkinter as ctk
import math
import webbrowser
import random
from datetime import datetime
from PIL import Image, ImageTk

# ---------- Config ----------
FLAG_RATIO = (3, 2)  # 3:2
BASE_WIDTH = 600
SLICE_COUNT = 180
SPOKES = 24

# Colors
SAFFRON = "#FF9933"
WHITE = "#FFFFFF"
GREEN = "#138808"
NAVY = "#000080"
POLE = "#8B7D6B"
POLE_METAL = "#C0C0C0"
SHADOW = "#000000"
GOLD = "#FFD700"
TEXT_COLOR_LIGHT = "#333333"
TEXT_COLOR_DARK = "#E0E0E0"

class FlagApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # ---- Theme / window ----
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.title("Indian Flag — CustomTkinter (Enhanced Animation)")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # Load cloud background image
        try:
            self.cloud_img = Image.open("clouds.gif")
            self.cloud_photo = None
        except:
            # Create a blank image if clouds.png not found
            self.cloud_img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
            self.cloud_photo = None

        # ---- Root grid (Left: flag/controls, Right: wishes) ----
        self.grid_columnconfigure(0, weight=3)  # left
        self.grid_columnconfigure(1, weight=2)  # right
        self.grid_rowconfigure(0, weight=1)

        # ===== Left column: controls (top) + canvas (bottom) =====
        self.left_frame = ctk.CTkFrame(self, corner_radius=16)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self.left_frame.grid_rowconfigure(0, weight=0)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Top bar (controls)
        self.top_bar = ctk.CTkFrame(self.left_frame, corner_radius=16)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        self.top_bar.grid_columnconfigure(0, weight=1)
        self.top_bar.grid_columnconfigure(1, weight=0)
        self.top_bar.grid_columnconfigure(2, weight=0)

        title = ctk.CTkLabel(
            self.top_bar,
            text="Indian Flag",
            font=("Times New Roman", 16, "bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=12, pady=8)

        # Buttons
        self.btn_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.btn_frame.grid(row=0, column=1, sticky="e", padx=8)
        
        # Button with icons
        self.btn_start = ctk.CTkButton(
            self.btn_frame, 
            text="▶ Start", 
            command=self.start_animation,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.btn_pause = ctk.CTkButton(
            self.btn_frame, 
            text="⏸ Pause", 
            command=self.pause_animation,
            fg_color="#FF9800",
            hover_color="#e68a00"
        )
        self.btn_reset = ctk.CTkButton(
            self.btn_frame, 
            text="🔄 Reset", 
            command=self.reset_animation,
            fg_color="#2196F3",
            hover_color="#0b7dda"
        )
        
        self.btn_start.grid(row=0, column=0, padx=4, pady=6)
        self.btn_pause.grid(row=0, column=1, padx=4, pady=6)
        self.btn_reset.grid(row=0, column=2, padx=4, pady=6)

        # Sliders
        self.slider_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.slider_frame.grid(row=0, column=2, sticky="e", padx=8)
        
        # Improved sliders with better labels
        self.speed = ctk.CTkSlider(
            self.slider_frame,
            from_=0.2,
            to=4.0,
            number_of_steps=76,
            width=160,
            command=self._on_speed_change,
            button_color="#2196F3",
            button_hover_color="#0b7dda"
        )
        self.speed.set(1.2)
        
        self.amp = ctk.CTkSlider(
            self.slider_frame,
            from_=2,
            to=24,
            number_of_steps=44,
            width=160,
            command=self._on_amp_change,
            button_color="#4CAF50",
            button_hover_color="#45a049"
        )
        self.amp.set(12)
        
        self.lbl_speed = ctk.CTkLabel(
            self.slider_frame,
            text=f"🌊 Speed: {self.speed.get():.1f}x",
            font=("Segoe UI", 11)
        )
        self.lbl_amp = ctk.CTkLabel(
            self.slider_frame,
            text=f"🌊 Wave: {self.amp.get():.0f}px",
            font=("Segoe UI", 11)
        )
        
        self.lbl_speed.grid(row=0, column=0, sticky="ew", pady=(6, 0))
        self.speed.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        self.lbl_amp.grid(row=2, column=0, sticky="ew", pady=(6, 0))
        self.amp.grid(row=3, column=0, sticky="ew", pady=(0, 6))

        # Theme / info
        self.switch_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.switch_frame.grid(row=0, column=3, sticky="e", padx=8)
        
        self.theme_switch = ctk.CTkSwitch(
            self.switch_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            progress_color="#4CAF50"
        )
        
        self.info_btn = ctk.CTkButton(
            self.switch_frame,
            text="ℹ️ Info",
            width=80,
            command=self.show_info,
            fg_color="#607D8B",
            hover_color="#455A64"
        )
        
        self.theme_switch.grid(row=0, column=0, padx=6)
        self.info_btn.grid(row=1, column=0, padx=6, pady=(4, 0))

        # Canvas container (left bottom)
        self.canvas_frame = ctk.CTkFrame(self.left_frame, corner_radius=16)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.canvas_frame, highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        # ===== Right column: wishes panel =====
        self.message_frame = ctk.CTkFrame(self, corner_radius=20)
        self.message_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 12), pady=12)
        self.message_frame.grid_rowconfigure(0, weight=0)
        self.message_frame.grid_rowconfigure(1, weight=1)
        self.message_frame.grid_rowconfigure(2, weight=0)  # For footer
        self.message_frame.grid_columnconfigure(0, weight=1)

        # Current year calculation
        current_year = datetime.now().year
        independence_year = 1947
        years_since_independence = current_year - independence_year

        heading = ctk.CTkLabel(
            self.message_frame,
            text=f"Happy 79th Independence Day",
            font=("Helvetica", 28, "bold"),
            text_color=SAFFRON,
            justify="center",
        )
        heading.grid(row=0, column=0, sticky="ew", padx=16, pady=(24, 8))

        wishes = (
            "🎉 Freedom in our hearts\n"
            "💚 Love for our nation\n"
            "🕊️ Peace in our minds\n"
            "🌟 Pride in our souls\n\n"
            "🇮🇳 Let's salute our great nation\n"
            "💪 Be proud to be an Indian\n"
            "🎆 Jai Hind! 🇮🇳 \n\n\n"
            "Jana-gana-mana-adhinayaka jaya he\n"
            "Bharata-bhagya-vidhata\n"
            "Punjaba-Sindhu-Gujarata-Maratha\n"
            "Dravida-Utkala-Banga\n"
            "Vindhya-Himachala-Yamuna-Ganga\n"
            "uchchala-jaladhi-taranga\n"
            "Tava Shubha name jage\n,tava shubha asisa mage\n,gahe tava jaya-gatha.\n"
            "Jana-gana-mangala-dayaka jaya he.\n"
            "Bharata-bhagya-vidhata.\n"
            "Jaya he, Jaya he, Jaya he, jaya jaya jaya, jaya he.\n\n\n"
            "Created By King MA Sheikh"
        )
        
        wishes_label = ctk.CTkLabel(
            self.message_frame,
            text=wishes,
            font=("Times New Roman", 20),
            text_color=GOLD,
            justify="center",
        )
        wishes_label.grid(row=1, column=0, sticky="n", padx=18, pady=(6, 18))

        # Footer with clickable link
        footer_frame = ctk.CTkFrame(self.message_frame, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="sew", padx=12, pady=(0, 12))
        footer_frame.grid_columnconfigure(0, weight=1)
        
        footer_text = ctk.CTkLabel(
            footer_frame,
            text="Learn more about India's independence",
            font=("Helvetica", 12),
            text_color="#607D8B",
            cursor="hand2"
        )
        footer_text.grid(row=0, column=0, sticky="ew")
        footer_text.bind("<Button-1>", lambda e: webbrowser.open("https://en.wikipedia.org/wiki/Independence_Day_(India)"))

        # ---- Bindings ----
        self.bind("<Configure>", self._on_resize)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<space>", lambda e: self.toggle_animation())
        self.bind("<Left>", lambda e: self.adjust_speed(-0.1))
        self.bind("<Right>", lambda e: self.adjust_speed(0.1))
        self.bind("<Up>", lambda e: self.adjust_amplitude(1))
        self.bind("<Down>", lambda e: self.adjust_amplitude(-1))

        # ---- Animation state ----
        self.phase = 0.0
        self.running = True
        self.wave_speed = self.speed.get()
        self.amplitude = self.amp.get()
        self.wavelength = 180.0
        self._after_id = None
        self.drag_start = None
        self.flag_bounds = (0, 0, 0, 0)  # set before first draw
        self.cloud_bg = None  # For cloud background image

        # ---- Canvas item ids ----
        self.items = {
            "shadow": None,
            "pole": None,
            "pole_top": None,
            "pole_ball": None,
            "pole_base": None,
            "rope": None,
            "edge_gloss": None,
            "saffron": None,
            "white": None,
            "green": None,
            "chakra_ring": None,
            "chakra_inner_ring": None,
            "chakra_hub": None,
            "spokes": [],
            "glitter": [],
        }

        # Initial draw + start animation loop
        self._redraw_all()
        self.start_animation()

    # ================= UI handlers =================
    def toggle_theme(self):
        mode = "dark" if ctk.get_appearance_mode().lower() != "dark" else "light"
        ctk.set_appearance_mode(mode)
        self._redraw_all()

    def show_info(self):
        info_text = (
            "Indian Flag Animation\n\n"
            "Features:\n"
            "• Realistic waving flag with adjustable parameters\n"
            "• Interactive controls (drag to reposition)\n"
            "• Detailed pole with metallic highlights\n"
            "• Dark/Light mode toggle\n"
            "• Keyboard shortcuts (Space, Arrow keys)\n\n"
            "Controls:\n"
            "• Start / Pause / Reset buttons\n"
            "• Speed & Wave amplitude sliders\n"
            "• Drag flag to reposition\n\n"
            "Keyboard Shortcuts:\n"
            "• Space: Toggle animation\n"
            "• Left/Right: Adjust speed\n"
            "• Up/Down: Adjust wave height"
        )
        
        info_window = ctk.CTkToplevel(self)
        info_window.title("About")
        info_window.geometry("450x500")
        info_window.resizable(False, False)
        
        # Make window stay on top
        info_window.attributes('-topmost', True)
        info_window.after(100, lambda: info_window.attributes('-topmost', False))
        
        textbox = ctk.CTkTextbox(info_window, wrap="word", font=("Consolas", 12))
        textbox.pack(fill="both", expand=True, padx=10, pady=10)
        textbox.insert("1.0", info_text)
        textbox.configure(state="disabled")
        
        close_btn = ctk.CTkButton(
            info_window,
            text="Close",
            command=info_window.destroy,
            fg_color="#607D8B",
            hover_color="#455A64"
        )
        close_btn.pack(pady=10)

    def _on_speed_change(self, _=None):
        self.wave_speed = self.speed.get()
        self.lbl_speed.configure(text=f"🌊 Speed: {self.wave_speed:.1f}x")

    def _on_amp_change(self, _=None):
        self.amplitude = self.amp.get()
        self.lbl_amp.configure(text=f"🌊 Wave: {self.amplitude:.0f}px")

    def adjust_speed(self, delta):
        new_val = max(0.2, min(4.0, self.speed.get() + delta))
        self.speed.set(new_val)
        self._on_speed_change()

    def adjust_amplitude(self, delta):
        new_val = max(2, min(24, self.amp.get() + delta))
        self.amp.set(new_val)
        self._on_amp_change()

    def _on_resize(self, event):
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None
        
        # Update cloud background when window resizes
        if hasattr(self, 'cloud_bg') and self.cloud_bg:
            self.canvas.delete(self.cloud_bg)
            self.cloud_bg = None
            
        self._redraw_all()

    def on_canvas_click(self, event):
        x0, y0, x1, y1 = self.flag_bounds
        if x0 <= event.x <= x1 and y0 <= event.y <= y1:
            self.drag_start = (event.x, event.y, x0, y0)

    def on_canvas_drag(self, event):
        if self.drag_start:
            orig_x, orig_y, orig_x0, orig_y0 = self.drag_start
            dx = event.x - orig_x
            dy = event.y - orig_y
            new_x0 = orig_x0 + dx
            new_y0 = orig_y0 + dy
            
            # keep inside canvas
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            fw = self.flag_bounds[2] - self.flag_bounds[0]
            fh = self.flag_bounds[3] - self.flag_bounds[1]
            new_x0 = max(60, min(new_x0, cw - fw - 20))
            new_y0 = max(20, min(new_y0, ch - fh - 20))
            
            self.flag_bounds = (new_x0, new_y0, new_x0 + fw, new_y0 + fh)
            self._update_flag_geometry()
            self._update_pole_position(new_x0)
            self.drag_start = (event.x, event.y, new_x0, new_y0)

    def toggle_animation(self):
        if self.running:
            self.pause_animation()
        else:
            self.start_animation()

    def pause_animation(self):
        self.running = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None
        self.btn_start.configure(state="normal")
        self.btn_pause.configure(state="disabled")

    def reset_animation(self):
        self.phase = 0.0
        self._redraw_all()
        if not self.running:
            self.start_animation()

    def start_animation(self):
        if not self.running:
            self.running = True
            self.btn_start.configure(state="disabled")
            self.btn_pause.configure(state="normal")
        if self._after_id is None:
            self._tick()

    # ================= Geometry helpers =================
    def _compute_flag_rect(self):
        cw = max(self.canvas.winfo_width(), 200)
        ch = max(self.canvas.winfo_height(), 200)

        margin = max(int(min(cw, ch) * 0.03), 15)
        avail_w = cw - margin * 2 - 80  # room for pole on the left
        avail_h = ch - margin * 2

        target_w = min(avail_w, 600)  # cap width a bit larger here
        target_h = int(target_w * FLAG_RATIO[1] / FLAG_RATIO[0])
        if target_h > avail_h:
            target_h = avail_h
            target_w = int(target_h * FLAG_RATIO[0] / FLAG_RATIO[1])

        x0 = margin + 60
        y0 = (ch - target_h) // 2
        x1 = x0 + target_w
        y1 = y0 + target_h
        return x0, y0, x1, y1

    # ================= Drawing =================
    def _redraw_all(self):
        self.canvas.delete("all")
        # Reset item ids
        self.items["spokes"] = []
        self.items["glitter"] = []
        for k in list(self.items.keys()):
            if k not in ("spokes", "glitter"):
                self.items[k] = None

        # Background to match CTk theme
        tmp = ctk.CTkFrame(self.canvas_frame)
        bg = tmp.cget("fg_color")
        tmp.destroy()
        if isinstance(bg, tuple):
            bg = bg[0] if ctk.get_appearance_mode().lower() == "light" else bg[1]
        try:
            self.canvas.configure(bg=bg)
        except Exception:
            self.canvas.configure(bg="#1f1f1f")

        # Add cloud background if image is available
        if self.cloud_img and self.cloud_img.size != (100, 100):  # Not the blank image
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            
            # Resize cloud image to fit canvas while maintaining aspect ratio
            img_ratio = self.cloud_img.width / self.cloud_img.height
            canvas_ratio = cw / ch
            
            if canvas_ratio > img_ratio:
                # Canvas is wider than image
                new_height = ch
                new_width = int(new_height * img_ratio)
            else:
                # Canvas is taller than image
                new_width = cw
                new_height = int(new_width / img_ratio)
                
            resized_img = self.cloud_img.resize((new_width, new_height), Image.LANCZOS)
            self.cloud_photo = ImageTk.PhotoImage(resized_img)
            
            # Center the image
            x_pos = (cw - new_width) // 2
            y_pos = (ch - new_height) // 2
            
            self.cloud_bg = self.canvas.create_image(x_pos, y_pos, image=self.cloud_photo, anchor="nw")

        x0, y0, x1, y1 = self._compute_flag_rect()
        self.flag_bounds = (x0, y0, x1, y1)
        self.slice_count = max(80, int(SLICE_COUNT * (x1 - x0) / BASE_WIDTH))

        self._draw_shadow(x0, y0, x1, y1)
        self._draw_pole(x0, y0, y1)
        self._build_waving_flag()
        self._draw_edge_gloss(x0, y0, x1, y1)
        self._update_flag_geometry()
        self._add_glitter_effects()

    def _draw_shadow(self, x0, y0, x1, y1):
        bands = 8  # Increased bands for smoother shadow
        dx, dy = 12, 10
        alpha_stipples = ("gray75", "gray50", "gray25", "gray12")
        
        for i in range(bands):
            st = alpha_stipples[min(i // 2, len(alpha_stipples)-1)]
            offset = i * 1.5
            self.canvas.create_rectangle(
                x0 + dx + offset, y0 + dy + offset,
                x1 + dx + offset, y1 + dy + offset,
                fill=SHADOW, outline="", stipple=st
            )

    def _draw_pole(self, x_left, y_top, y_bottom):
        pole_w = 20
        pole_top_h = 40

        # Main pole with gradient effect
        for i in range(pole_w):
            shade = int(210 - i * 3)
            color = f"#{shade:02x}{shade-20:02x}{shade-40:02x}"
            self.canvas.create_rectangle(
                x_left - 40 + i, y_top - pole_top_h,
                x_left - 39 + i, y_bottom + 30,
                fill=color, outline="", tags=f"pole_segment_{i}"
            )

        # Pole top with metallic shine
        self.items["pole_top"] = self.canvas.create_rectangle(
            x_left - 45, y_top - pole_top_h,
            x_left - 15, y_top - pole_top_h + 30,
            fill=POLE_METAL, outline=""
        )
        
        # Add metallic shine effect
        self.canvas.create_line(
            x_left - 42, y_top - pole_top_h + 5,
            x_left - 35, y_top - pole_top_h + 15,
            x_left - 28, y_top - pole_top_h + 5,
            fill="white", width=2, smooth=True
        )

        self.items["pole_ball"] = self.canvas.create_oval(
            x_left - 35, y_top - pole_top_h - 15,
            x_left - 25, y_top - pole_top_h - 5,
            fill=GOLD, outline="black"
        )
        
        # More realistic rope with curve
        self.items["rope"] = self.canvas.create_line(
            x_left - 30, y_top - pole_top_h + 5,
            x_left - 20, y_top - pole_top_h + 10,
            x_left - 10, y_top - pole_top_h + 8,
            x_left, y_top + 10,
            fill="#F5F5F5", width=3, smooth=True
        )
        
        # Pole base with 3D effect
        self.items["pole_base"] = self.canvas.create_rectangle(
            x_left - 50, y_bottom + 20,
            x_left - 20, y_bottom + 50,
            fill=POLE, outline="black"
        )
        
        # Add base shadow
        self.canvas.create_rectangle(
            x_left - 50, y_bottom + 45,
            x_left - 20, y_bottom + 50,
            fill="#5D4C3C", outline=""
        )

    def _update_pole_position(self, flag_x):
        y_top = self.flag_bounds[1]
        y_bottom = self.flag_bounds[3]
        pole_w = 20

        # Update all pole components
        for i in range(pole_w):
            self.canvas.coords(
                f"pole_segment_{i}",
                flag_x - 40 + i, y_top - 40,
                flag_x - 39 + i, y_bottom + 30
            )

        self.canvas.coords(self.items["pole_top"],
            flag_x - 45, y_top - 40,
            flag_x - 15, y_top - 10
        )
        
        self.canvas.coords(self.items["rope"],
            flag_x - 30, y_top - 35,
            flag_x - 20, y_top - 30,
            flag_x - 10, y_top - 32,
            flag_x, y_top + 10
        )
        
        self.canvas.coords(self.items["pole_ball"],
            flag_x - 35, y_top - 55,
            flag_x - 25, y_top - 45
        )
        
        self.canvas.coords(self.items["pole_base"],
            flag_x - 50, y_bottom + 20,
            flag_x - 20, y_bottom + 50
        )

    def _draw_edge_gloss(self, x0, y0, x1, y1):
        steps = 15  # Increased steps for smoother gloss
        alpha_stipples = ("gray12", "gray25", "gray50", "gray75")
        
        # Top edge gloss
        for i in range(steps):
            y = y0 + i
            st = alpha_stipples[min(i // 4, len(alpha_stipples)-1)]
            self.canvas.create_line(x0, y, x1, y, fill="#FFFFFF", stipple=st)
        
        # Left edge gloss
        for i in range(steps):
            x = x0 + i
            st = alpha_stipples[min(i // 4, len(alpha_stipples)-1)]
            self.canvas.create_line(x, y0, x, y1, fill="#FFFFFF", stipple=st)

    def _add_glitter_effects(self):
        """Add sparkling effects to the flag"""
        x0, y0, x1, y1 = self.flag_bounds
        W = x1 - x0
        H = y1 - y0
        
        # Clear existing glitter
        for glitter in self.items["glitter"]:
            self.canvas.delete(glitter)
        self.items["glitter"] = []
        
        # Add random glitter spots
        for _ in range(20):  # Number of glitter spots
            x = x0 + W * 0.1 + 0.8 * W * random.random()
            y = y0 + H * 0.1 + 0.8 * H * random.random()
            
            # Only add to saffron and green bands
            if y < y0 + H/3 or y > y0 + 2*H/3:
                size = 1 + 3 * random.random()
                glitter = self.canvas.create_oval(
                    x - size, y - size,
                    x + size, y + size,
                    fill="white", outline=""
                )
                self.items["glitter"].append(glitter)

    def _build_waving_flag(self):
        # Create small placeholder polygons
        self.items["saffron"] = self.canvas.create_polygon(
            0, 0, 1, 0, 1, 1, fill=SAFFRON, outline="", smooth=True
        )
        self.items["white"] = self.canvas.create_polygon(
            0, 0, 1, 0, 1, 1, fill=WHITE, outline="", smooth=True
        )
        self.items["green"] = self.canvas.create_polygon(
            0, 0, 1, 0, 1, 1, fill=GREEN, outline="", smooth=True
        )

        # Chakra ring & hub
        x0, y0, x1, y1 = self.flag_bounds
        W = x1 - x0
        H = y1 - y0
        stripe_h = H / 3
        cx = x0 + W * 0.5
        cy = y0 + H * 0.5
        r_outer = stripe_h * 0.38
        r_hub = r_outer * 0.08

        # Chakra with subtle inner circle
        self.items["chakra_ring"] = self.canvas.create_oval(
            cx - r_outer, cy - r_outer,
            cx + r_outer, cy + r_outer,
            outline=NAVY, width=2.5
        )
        
        # Inner ring (now stored in items dict)
        self.items["chakra_inner_ring"] = self.canvas.create_oval(
            cx - r_outer * 0.7, cy - r_outer * 0.7,
            cx + r_outer * 0.7, cy + r_outer * 0.7,
            outline=NAVY, width=1, dash=(2, 1)
        )
        
        self.items["chakra_hub"] = self.canvas.create_oval(
            cx - r_hub, cy - r_hub,
            cx + r_hub, cy + r_hub,
            fill=NAVY, outline=NAVY
        )

        # Spokes with improved appearance
        self.items["spokes"] = []
        for i in range(SPOKES):
            a = (2 * math.pi) * i / SPOKES
            x_end = cx + (r_outer - 3) * math.cos(a)
            y_end = cy + (r_outer - 3) * math.sin(a)
            
            # Thicker line at the outer end
            line = self.canvas.create_line(
                cx + (r_outer * 0.7) * math.cos(a),
                cy + (r_outer * 0.7) * math.sin(a),
                x_end, y_end,
                fill=NAVY, width=1.5
            )
            self.items["spokes"].append(line)

    # ================= Wave maths =================
    def _wave_offset(self, x):
        rel_x = (x - self.flag_bounds[0]) / max(1, (self.flag_bounds[2] - self.flag_bounds[0]))
        edge_damp = math.sin(max(0.0, min(1.0, rel_x)) * math.pi)  # 0 at edges, 1 in middle
        
        # More complex wave function with secondary wave
        main_wave = math.sin((x / self.wavelength) + self.phase) * self.amplitude * edge_damp
        secondary_wave = math.sin((x / (self.wavelength * 0.7)) + self.phase * 1.3) * (self.amplitude * 0.3) * edge_damp
        
        return main_wave + secondary_wave

    def _make_wavy_polygon(self, x0, y_top, x1, y_bottom):
        n = self.slice_count
        xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
        top = [(x, y_top + self._wave_offset(x)) for x in xs]
        bot = [(x, y_bottom + self._wave_offset(x)) for x in reversed(xs)]
        coords = []
        for px, py in (top + bot):
            coords.extend((px, py))
        return coords

    def _update_flag_geometry(self):
        x0, y0, x1, y1 = self.flag_bounds
        W = x1 - x0
        H = y1 - y0
        stripe_h = H / 3

        saffron_coords = self._make_wavy_polygon(x0, y0, x1, y0 + stripe_h)
        white_coords = self._make_wavy_polygon(x0, y0 + stripe_h, x1, y0 + 2 * stripe_h)
        green_coords = self._make_wavy_polygon(x0, y0 + 2 * stripe_h, x1, y1)

        self.canvas.coords(self.items["saffron"], *saffron_coords)
        self.canvas.coords(self.items["white"], *white_coords)
        self.canvas.coords(self.items["green"], *green_coords)

        # Chakra follow mid band wave at center x
        cx = x0 + W * 0.5
        center_wave_y = y0 + H * 0.5 + self._wave_offset(cx)
        r_outer = stripe_h * 0.38
        r_hub = r_outer * 0.08

        # Update all chakra components to wave together
        self.canvas.coords(self.items["chakra_ring"],
                          cx - r_outer, center_wave_y - r_outer,
                          cx + r_outer, center_wave_y + r_outer)
        
        self.canvas.coords(self.items["chakra_inner_ring"],
                          cx - r_outer * 0.7, center_wave_y - r_outer * 0.7,
                          cx + r_outer * 0.7, center_wave_y + r_outer * 0.7)

        self.canvas.coords(self.items["chakra_hub"],
                          cx - r_hub, center_wave_y - r_hub,
                          cx + r_hub, center_wave_y + r_hub)

        for i, line in enumerate(self.items["spokes"]):
            a = (2 * math.pi) * i / SPOKES
            inner_x = cx + (r_outer * 0.7) * math.cos(a)
            inner_y = center_wave_y + (r_outer * 0.7) * math.sin(a)
            outer_x = cx + (r_outer - 3) * math.cos(a)
            outer_y = center_wave_y + (r_outer - 3) * math.sin(a)
            self.canvas.coords(line, inner_x, inner_y, outer_x, outer_y)

    # ================= Animation loop =================
    def _tick(self):
        dt = 1 / 60.0
        self.phase += dt * self.wave_speed * 2.0
        
        # Randomly move some glitter spots
        if random.random() < 0.1:  # 10% chance to move a glitter spot each frame
            self._move_random_glitter()
        
        self._update_flag_geometry()
        
        if self.running:
            self._after_id = self.after(int(dt * 1000), self._tick)
        else:
            self._after_id = None

    def _move_random_glitter(self):
        if not self.items["glitter"]:
            return
            
        x0, y0, x1, y1 = self.flag_bounds
        W = x1 - x0
        H = y1 - y0
        
        # Move 1-3 glitter spots
        for _ in range(random.randint(1, 3)):
            idx = random.randint(0, len(self.items["glitter"]) - 1)
            glitter = self.items["glitter"][idx]
            
            # Only move glitter in saffron or green bands
            if random.random() < 0.5:
                # Saffron band
                new_x = x0 + W * 0.1 + 0.8 * W * random.random()
                new_y = y0 + H * 0.1 + (H/3 - 20) * random.random()
            else:
                # Green band
                new_x = x0 + W * 0.1 + 0.8 * W * random.random()
                new_y = y0 + 2*H/3 + 20 + (H/3 - 40) * random.random()
            
            size = 1 + 3 * random.random()
            self.canvas.coords(
                glitter,
                new_x - size, new_y - size,
                new_x + size, new_y + size
            )


if __name__ == "__main__":
    app = FlagApp()
    app.mainloop()
