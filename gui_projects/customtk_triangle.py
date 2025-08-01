import customtkinter as ctk

# Set the appearance mode and theme (optional)
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.title("Triangle using CustomTkinter")
app.geometry("400x400")

# Create a canvas inside CustomTkinter window
canvas = ctk.CTkCanvas(app, width=400, height=400, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Define triangle coordinates (x1,y1, x2,y2, x3,y3)
x1, y1 = 200, 50
x2, y2 = 100, 300
x3, y3 = 300, 300

# Draw the triangle
canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="skyblue", outline="black", width=2)

# Start the app
app.mainloop()
