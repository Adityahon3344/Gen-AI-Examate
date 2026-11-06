
from app.records import load_records, search, count_by, get_by_id


def display_schemes():
    schemes = load_records()

    for scheme in schemes:
        print("\nID:", scheme["id"])
        print("Name:", scheme["scheme_name"])
        print("Department:", scheme["department"])
        print("Benefit:", scheme["benefit"])


def main():
    while True:
        print("\n===== KRISHIYOJANA =====")
        print("1. Display All Schemes")
        print("2. Search Scheme")
        print("3. Count by Department")
        print("4. Get Scheme by ID")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            display_schemes()

        elif choice == "2":
            keyword = input("Enter search keyword: ")
            results = search(keyword)

            if results:
                for scheme in results:
                    print("\n", scheme["id"], "-", scheme["scheme_name"])
            else:
                print("No schemes found.")

        elif choice == "3":
            department = input("Enter department name: ")
            print("Total schemes:", count_by(department))

        elif choice == "4":
            try:
                scheme_id = int(input("Enter scheme ID: "))
                scheme = get_by_id(scheme_id)

                if scheme:
                    print("\nScheme:", scheme["scheme_name"])
                    print("Benefit:", scheme["benefit"])
                    print("Eligibility:")
                    for item in scheme["eligibility"]:
                        print("-", item)
                    print("Required Documents:")
                    for item in scheme["required_documents"]:
                        print("-", item)
                else:
                    print("Scheme not found.")

            except ValueError:
                print("Please enter a valid numeric ID.")

        elif choice == "0":
            print("Thank you for using KrishiYojana!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
