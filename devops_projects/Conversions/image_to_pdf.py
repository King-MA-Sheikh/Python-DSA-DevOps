import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
import sys
from PIL import Image, ImageDraw
import math
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ImageToPDFApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🌟 Ultimate Image to PDF Wizard 🌟")
        self.geometry("650x650")
        self.resizable(False, False)
        self.center_window()

        self.selected_image_path = None
        self.save_pdf_path = None
        self.preview_image = None
        self.loading_animation_active = False
        self.angle = 0
        self.animation_frames = []
        self.create_loading_animation_frames()

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)

        # Header Frame with animated gradient effect
        self.header_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1A1A2E")
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))

        # Animated title
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="🪄 Image to PDF Wizard 🎩",
            font=("Arial", 26, "bold"),
            text_color="#4CC9F0"
        )
        self.title_label.pack(pady=(10, 5))

        # Animated subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Transform images into polished PDF documents with magic!",
            font=("Arial", 12),
            text_color="#B8B8B8"
        )
        self.subtitle_label.pack()

        # Magic wand separator
        self.separator = ctk.CTkLabel(
            self.header_frame,
            text="✨" * 30,
            text_color="#F72585",
            font=("Arial", 10)
        )
        self.separator.pack(pady=5)

        # Main content frame with glass morphism effect (using valid color codes)
        self.main_frame = ctk.CTkFrame(
            self, 
            corner_radius=20, 
            fg_color="#2B2B2B",  # Changed from transparent to dark background
            border_width=2,
            border_color="#4CC9F0"  # Removed alpha channel from color
        )
        self.main_frame.grid(row=1, column=0, rowspan=6, sticky="nsew", padx=20, pady=(0, 20))

        # Image selection section
        self.image_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.image_frame.pack(pady=(20, 10), padx=20, fill="x")

        # Select Image Button with hover animation
        self.select_image_btn = ctk.CTkButton(
            self.image_frame,
            text="🔍 Browse Image",
            command=self.select_image,
            fg_color="#4361EE",
            hover_color="#3A0CA3",
            font=("Arial", 14, "bold"),
            height=45,
            corner_radius=12,
            border_width=2,
            border_color="#4CC9F0",
            compound="left"
        )
        self.select_image_btn.pack(fill="x", pady=(0, 10))

        # Display Selected Image Path
        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="🖼️ No image selected",
            text_color="#B8B8B8",
            font=("Arial", 12)
        )
        self.image_label.pack()

        # Preview frame with shadow effect
        self.preview_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="transparent",
            height=180
        )
        self.preview_label = ctk.CTkLabel(
            self.preview_frame, 
            text="🎇 Preview will appear here",
            text_color="#6C757D",
            font=("Arial", 12, "italic")
        )
        self.preview_label.pack(pady=10)

        # Save location section
        self.save_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.save_frame.pack(pady=15, padx=20, fill="x")

        # Select Save Location Button
        self.select_save_btn = ctk.CTkButton(
            self.save_frame,
            text="📁 Choose Destination",
            command=self.select_save_path,
            fg_color="#4895EF",
            hover_color="#3F37C9",
            font=("Arial", 14, "bold"),
            height=45,
            corner_radius=12,
            border_width=2,
            border_color="#4CC9F0"
        )
        self.select_save_btn.pack(fill="x", pady=(0, 10))

        # Display Save Path
        self.save_label = ctk.CTkLabel(
            self.save_frame,
            text="📂 No save location selected",
            text_color="#B8B8B8",
            font=("Arial", 12)
        )
        self.save_label.pack()

        # Action buttons frame
        self.action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.action_frame.pack(pady=15, fill="x", padx=20)

        # Convert Button with magic sparkle effect
        self.convert_btn = ctk.CTkButton(
            self.action_frame,
            text="✨ Cast Conversion Spell ✨",
            command=self.start_conversion,
            fg_color="#F72585",
            hover_color="#B5179E",
            font=("Arial", 16, "bold"),
            height=55,
            corner_radius=15,
            border_width=3,
            border_color="#4CC9F0"
        )
        self.convert_btn.pack(fill="x", pady=(0, 10))

        # Additional action buttons
        self.quick_actions_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.quick_actions_frame.pack(fill="x", pady=(10, 0))

        # Open Folder Button
        self.open_folder_btn = ctk.CTkButton(
            self.quick_actions_frame,
            text="📂 Open Output Folder",
            command=self.open_output_folder,
            fg_color="#7209B7",
            hover_color="#560BAD",
            font=("Arial", 12),
            width=150,
            height=35,
            corner_radius=10
        )
        self.open_folder_btn.pack(side="left", padx=5)

        # Clear Selection Button
        self.clear_btn = ctk.CTkButton(
            self.quick_actions_frame,
            text="🧹 Clear Selection",
            command=self.clear_selections,
            fg_color="#6A4C93",
            hover_color="#5A3D7A",
            font=("Arial", 12),
            width=150,
            height=35,
            corner_radius=10
        )
        self.clear_btn.pack(side="right", padx=5)

        # Footer with version and creator
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=6, column=0, pady=(0, 10))

        self.footer_label = ctk.CTkLabel(
            self.footer_frame,
            text="Magic PDF Converter v2.0 • Made with ❤️ using Python",
            text_color="#6C757D",
            font=("Arial", 10)
        )
        self.footer_label.pack()

    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (650 // 2)
        y = (screen_height // 2) - (650 // 2)
        self.geometry(f"650x650+{x}+{y}")

    def create_loading_animation_frames(self):
        """Create frames for the circular loading animation"""
        size = 100
        for i in range(0, 360, 15):
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.arc(
                [(10, 10), (size-10, size-10)],
                start=i,
                end=i+270,
                fill="#F72585",
                width=8
            )
            self.animation_frames.append(img)

    def update_loading_animation(self):
        """Update the circular loading animation"""
        if self.loading_animation_active:
            frame_index = int(self.angle / 15) % len(self.animation_frames)
            frame = self.animation_frames[frame_index]
            
            # Convert to CTkImage
            loading_img = ctk.CTkImage(
                light_image=frame,
                dark_image=frame,
                size=(150, 150)
            )
            
            self.preview_label.configure(
                image=loading_img,
                text=""
            )
            self.preview_label.image = loading_img  # Keep reference
            
            self.angle = (self.angle + 15) % 360
            self.after(100, self.update_loading_animation)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        if file_path:
            self.selected_image_path = file_path
            self.image_label.configure(
                text=f"🖼️ Selected: {os.path.basename(file_path)}", 
                text_color="#4CC9F0"
            )
            
            # Show preview of the image
            try:
                img = Image.open(file_path)
                img.thumbnail((300, 300))
                
                # Convert to CTkImage
                self.preview_image = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(250, 250)
                )
                
                self.preview_label.configure(
                    image=self.preview_image,
                    text=""
                )
                self.preview_frame.pack(pady=10)
            except Exception as e:
                print(f"Preview error: {e}")
                self.preview_label.configure(
                    text="⚠️ Could not load preview", 
                    image=None
                )

    def select_save_path(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save PDF As"
        )
        if save_path:
            self.save_pdf_path = save_path
            self.save_label.configure(
                text=f"📄 Will save to: {os.path.basename(save_path)}", 
                text_color="#4CC9F0"
            )

    def start_conversion(self):
        if not self.selected_image_path:
            messagebox.showwarning("Oops!", "Please select an image file first!")
            return
        if not self.save_pdf_path:
            messagebox.showwarning("Almost there!", "Please choose where to save your PDF!")
            return

        # Show loading animation
        self.loading_animation_active = True
        self.update_loading_animation()
        
        # Disable buttons during conversion
        self.convert_btn.configure(state="disabled", text="🔮 Casting spell...")
        self.select_image_btn.configure(state="disabled")
        self.select_save_btn.configure(state="disabled")
        self.open_folder_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")

        # Start conversion in a thread
        threading.Thread(target=self.convert_image_to_pdf, daemon=True).start()

    def convert_image_to_pdf(self):
        try:
            # Suppress pop-up using flags (Windows only)
            creation_flags = 0
            if sys.platform.startswith("win"):
                creation_flags = subprocess.CREATE_NO_WINDOW

            subprocess.run(
                ["magick", self.selected_image_path, self.save_pdf_path],
                check=True,
                creationflags=creation_flags
            )
            
            # Simulate processing time for better animation visibility
            time.sleep(2)
            
            self.after(100, lambda: messagebox.showinfo(
                "Success!", 
                f"🎉 PDF successfully created at:\n{self.save_pdf_path}\n\nYour magical document is ready to share!"
            ))
        except subprocess.CalledProcessError:
            self.after(100, lambda: messagebox.showerror(
                "Conversion Failed", 
                "❌ The magic spell failed!\n\nPlease check:\n1. ImageMagick is installed\n2. The image file is valid\n3. You have write permissions"
            ))
        except Exception as e:
            self.after(100, lambda: messagebox.showerror(
                "Error", 
                f"⚠️ A magical disturbance occurred:\n{str(e)}"
            ))
        finally:
            self.after(0, self.reset_ui)

    def reset_ui(self):
        self.loading_animation_active = False
        self.convert_btn.configure(state="normal", text="✨ Cast Conversion Spell ✨")
        self.select_image_btn.configure(state="normal")
        self.select_save_btn.configure(state="normal")
        self.open_folder_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
        
        # Restore the image preview if available
        if self.preview_image:
            self.preview_label.configure(image=self.preview_image, text="")
        else:
            self.preview_label.configure(
                image=None,
                text="🎇 Preview will appear here",
                text_color="#6C757D"
            )

    def open_output_folder(self):
        """Open the output folder in file explorer"""
        if self.save_pdf_path:
            folder_path = os.path.dirname(self.save_pdf_path)
            if sys.platform == "win32":
                os.startfile(folder_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder_path])
            else:
                subprocess.Popen(["xdg-open", folder_path])
        else:
            messagebox.showinfo(
                "Information",
                "No output folder selected yet. Please choose a save location first."
            )

    def clear_selections(self):
        """Clear all selections and reset the UI"""
        self.selected_image_path = None
        self.save_pdf_path = None
        self.preview_image = None

        self.image_label.configure(
            text="🖼️ No image selected",
            text_color="#B8B8B8"
        )

        self.save_label.configure(
            text="📂 No save location selected",
            text_color="#B8B8B8"
        )

        # Safely remove image and reset text
        try:
            self.preview_label.configure(image="", text="🎇 Preview will appear here", text_color="#6C757D")
            self.preview_label.image = None  # drop reference
        except Exception as e:
            print(f"Preview clear failed: {e}")

        # Optionally hide preview frame
        self.preview_frame.pack_forget()


if __name__ == "__main__":
    app = ImageToPDFApp()
    app.mainloop()
