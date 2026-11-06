
# KrishiYojana - Menu Program

while True:
    print("\n===== KRISHIYOJANA MENU =====")
    print("1. About KrishiYojana")
    print("2. Sample Questions")
    print("3. Farmer Category Rule Check")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\nKrishiYojana helps farmers discover")
        print("information about agricultural schemes.")

    elif choice == "2":
        print("\nSample Questions:")
        print("1. What is PM-KISAN?")
        print("2. Which schemes support small farmers?")
        print("3. What documents are needed for schemes?")

    elif choice == "3":
        acres = float(input("Enter your land area in acres: "))

        if acres <= 0:
            print("Invalid land area.")
        elif acres <= 2:
            print("Category: Small/Marginal farmer (demo rule)")
        elif acres <= 5:
            print("Category: Medium landholding (demo rule)")
        else:
            print("Category: Large landholding (demo rule)")

        print("Note: This is an educational example, not an official eligibility check.")

    elif choice == "0":
        print("Thank you for using KrishiYojana!")
        break

    else:
        print("Invalid choice. Please try again.")
