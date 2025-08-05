queue = []

while True:
    print("\nQueue Operations:")
    print("1. Enqueue (Insert)")
    print("2. Dequeue (Remove)")
    print("3. Display Queue")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        element = input("Enter element to insert: ")
        queue.append(element)
        print(f"{element} added to the queue.")
    
    elif choice == '2':
        if len(queue) == 0:
            print("Queue is empty. Nothing to remove.")
        else:
            removed = queue.pop(0)
            print(f"{removed} removed from the queue.")
    
    elif choice == '3':
        if len(queue) == 0:
            print("Queue is empty.")
        else:
            print("Current Queue:", queue)
    
    elif choice == '4':
        print("Exiting program.")
        break

    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
