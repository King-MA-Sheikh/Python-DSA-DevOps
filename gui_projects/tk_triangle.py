import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Triangle using Tkinter")
root.geometry("350x350")

# Create a canvas widget
canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Draw a triangle (3 points: x1,y1, x2,y2, x3,y3)
canvas.create_polygon(170, 70, 70, 270, 270, 270, fill="skyblue", outline="black", width=2)

# Run the application
root.mainloop()
