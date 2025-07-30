def add(num1, num2):
    return num1 + num2

def subtraction(num1, num2):
    return num1 - num2

def mul(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 == 0:
        return "Cannot divide by zero"
    return num1 /num2


print("\n\n\t\t---------Calculator---------\n")


print('''Please select an operation:- \n
      1. Add \n
      2. Subtract \n
      3. Multiply \n
      4. Divide \n''')

while True:
    while True:
        try:
            select = int(input("Select an operation (1 to 4):- "))
            if select in [1,2,3,4]:
                break
            else:
                print("Invalid Selection! Please enter a number between (1 to 4)")
        except ValueError:
            print("Invalid Selection! Please enter a number between (1 to 4)")
        
    
    number_1 = int(input("Enter first number:- "))
    number_2 = int(input("Enter second number:- "))

    if select == 1:
        print(number_1, " + ", number_2, " = ", add(number_1, number_2))
    elif select == 2:
        print(number_1, " - ", number_2, " = ", subtraction(number_1, number_2))
    elif select == 3:
        print(number_1, " * ", number_2, " = ", mul(number_1, number_2))
    elif select == 4:
        print(number_1, " / ", number_2, " = ", int(divide(number_1, number_2)))

    while True:
        choice = input("Wanna calculate  more? (Y/N):- ").strip().lower()
        if choice == 'y':
            break
        elif choice == 'n':
            print("GoodBye!")
            exit()
        else:
            print("Select only given pairs (Y/N):- ")