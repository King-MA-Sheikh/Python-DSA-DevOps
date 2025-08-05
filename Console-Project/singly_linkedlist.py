class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def display(self):
        if not self.head:
            print("List is empty.")
            return
        temp = self.head
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")

sll = SinglyLinkedList()

while True:
    print("\n--- Singly Linked List ---")
    print("1. Insert")
    print("2. Display")
    print("3. Exit")
    ch = input("Enter your choice: ")

    if ch == '1':
        val = input("Enter value to insert: ")
        sll.insert(val)
    elif ch == '2':
        sll.display()
    elif ch == '3':
        break
    else:
        print("Invalid choice.")
