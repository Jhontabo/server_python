import Pyro4

def read_polynomial(prompt):
    print(prompt)
    return [int(x) for x in input("Enter coefficients separated by spaces: ").split()]

def start_client():
    polynomial = Pyro4.Proxy("PYRONAME:polynomial.service")

    while True:
        print("\n********** Menu **********")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "4":
            print("Exiting...")
            break

        polyA = read_polynomial("Enter first polynomial:")
        polyB = read_polynomial("Enter second polynomial:")

        if choice == "1":
            result = polynomial.add(polyA, polyB)
            print("Result of Addition:", result)
        elif choice == "2":
            result = polynomial.subtract(polyA, polyB)
            print("Result of Subtraction:", result)
        elif choice == "3":
            result = polynomial.multiply(polyA, polyB)
            print("Result of Multiplication:", result)
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    start_client()
