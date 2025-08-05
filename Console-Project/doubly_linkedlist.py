class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = DNode(data)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node
            new_node.prev = temp

    def display(self):
        if not self.head:
            print("List is empty.")
            return
        temp = self.head
        while temp:
            print(temp.data, end=" <-> ")
            temp = temp.next
        print("None")

dll = DoublyLinkedList()

while True:
    print("\n--- Doubly Linked List ---")
    print("1. Insert")
    print("2. Display")
    print("3. Exit")
    ch = input("Enter your choice: ")

    if ch == '1':
        val = input("Enter value to insert: ")
        dll.insert(val)
    elif ch == '2':
        dll.display()
    elif ch == '3':
        break
    else:
        print("Invalid choice.")
