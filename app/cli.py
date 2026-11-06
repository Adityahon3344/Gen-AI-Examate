
from app.records import load_json_records


def main():
    records = load_json_records()

    if not records:
        print("No scheme records available.")
        return

    while True:
        print("\n===== KrishiYojana =====")
        print("1. Display all schemes")
        print("2. Search schemes")
        print("3. Count schemes by department")
        print("4. Get scheme by ID")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            for scheme in records:
                print(f"\nID: {scheme.id}")
                print(f"Scheme: {scheme.scheme_name}")
                print(f"Department: {scheme.department}")
                print(f"Benefit: {scheme.benefit}")

        elif choice == "2":
            keyword = input("Enter search keyword: ").lower()

            results = [
                scheme for scheme in records
                if keyword in (
                    scheme.scheme_name + " " +
                    scheme.department + " " +
                    scheme.benefit + " " +
                    " ".join(scheme.eligibility)
                ).lower()
            ]

            if results:
                for scheme in results:
                    print(f"{scheme.id}. {scheme.scheme_name}")
            else:
                print("No matching schemes found.")

        elif choice == "3":
            department = input("Enter department name: ").lower()

            count = sum(
                1 for scheme in records
                if scheme.department.lower() == department
            )

            print("Total schemes:", count)

        elif choice == "4":
            try:
                scheme_id = int(input("Enter scheme ID: "))

                found = next(
                    (s for s in records if s.id == scheme_id),
                    None
                )

                if found:
                    print("\nScheme:", found.scheme_name)
                    print("Benefit:", found.benefit)
                    print("Eligibility:", found.eligibility)
                    print("Documents:", found.required_documents)
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
