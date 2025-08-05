class CNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = CNode(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

    def display(self):
        if not self.head:
            print("List is empty.")
            return
        temp = self.head
        while True:
            print(temp.data, end=" -> ")
            temp = temp.next
            if temp == self.head:
                break
        print("(back to head)")

cll = CircularLinkedList()

while True:
    print("\n--- Circular Linked List ---")
    print("1. Insert")
    print("2. Display")
    print("3. Exit")
    ch = input("Enter your choice: ")

    if ch == '1':
        val = input("Enter value to insert: ")
        cll.insert(val)
    elif ch == '2':
        cll.display()
    elif ch == '3':
        break
    else:
        print("Invalid choice.")
