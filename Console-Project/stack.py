print("\n*************************Stack in Python*************************")

stack = []

def push():
    item = input("Enter item to push: ")
    stack.append(item)
    print(f"Pushed: {item}")

def pop():
    if not stack:
        print("Stack Underflow! Cannot pop from empty stack.")
    else:
        item = stack.pop()
        print(f"Popped: {item}")

def peek():
    if not stack:
        print("Stack is empty.")
    else:
        print(f"Top element: {stack[-1]}")

def display():
    print("Current Stack:", stack)

def is_empty():
    print("Stack is empty." if not stack else "Stack is not empty.")

while True:
    print("\nOptions:\n1. Push\n2. Pop\n3. Peek\n4. Display\n5. Is Empty\n6. Exit")
    choice = input("Enter your choice (1-6): ")

    if choice == '1':
        push()
    elif choice == '2':
        pop()
    elif choice == '3':
        peek()
    elif choice == '4':
        display()
    elif choice == '5':
        is_empty()
    elif choice == '6':
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 6.")
