import turtle

# Create screen and turtle
screen = turtle.Screen()
screen.title("Triangle using Turtle")

tri = turtle.Turtle()
tri.pensize(3)
tri.color("blue")
tri.fillcolor("skyblue")

# Draw triangle
tri.begin_fill()
for _ in range(3):
    tri.forward(200)   # Move forward
    tri.left(120)      # Turn left to form 120° angle
tri.end_fill()

# Exit on click
screen.exitonclick()
