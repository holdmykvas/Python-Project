import os

from tracker import Expense, ValidationError, BudgetManager




def handle_add_expense(manager):
    try:
        amount = input("Enter the amount: ").strip()
        if not Expense.is_valid_amount(amount):
            raise ValidationError("Error: Amount is invalid! | Try format : 10.50 or 10")
        print("--Amount accepted!\n")

        category = input("Enter the category: ").strip()
        print("--Category accepted! \n")

        date = input("Enter the date: ").strip()
        if not Expense.is_valid_date(date):
            raise ValidationError("Error: Date is invalid! | Try format : YYYY-MM-DD")
        print("--Date accepted!\n")

        expense = Expense(amount, category, date)
        manager.add_expense(expense)
    except ValidationError as e:
        print(e)

def handle_view_expenses(manager):
    if not manager.expenses:
        print("No expenses added yet!")
    else:
        for exp in manager.expenses:
            print(exp)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    manager = BudgetManager()
    print(" Welcome to the Budget Manager!")
    while True:
        print("\nMenu Options:")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Sort By Date")
        print("4. Filter by Category")
        print("5. View Unique Categories")
        print("6. Run Analytics & Forecast")
        print("7. Exit \n")

        choice = input("Select an option: ").strip()

        if choice == "1":
            handle_add_expense(manager)
            manager.save_data()

        elif choice == "2":
            handle_view_expenses(manager)

        elif choice == "3":
            if not manager.expenses:
                print("No expenses recorded yet.")
            else:
                sorted_expenses = sorted(manager.expenses, key=lambda e: e.date)
                for exp in sorted_expenses:
                    print(exp)

        elif choice == "4":
            cat_search = input("Enter category to search: ").strip()
            results = list(manager.generate_expense_category(cat_search))
            if not results:
                print("No expenses found for that category.")
            else:
                for exp in results:
                    print(exp)

        elif choice == "5":
            if not manager.expenses:
                print("No expenses recorded yet.")
            else:
                unique_categories = {exp.category for exp in manager.expenses}
                print("Categories used:", ", ".join(unique_categories))

        elif choice == "6":
            print(manager.generate_spending_report())

        elif choice == "7":
            manager.save_data()
            print("Data saved to JSON. Exiting...")
            break

        else:
            print("Invalid input! | Try again.")

        if choice != "7":
            input("Press Enter to return to the main menu.")
        clear_screen()

if __name__ == "__main__":
    main()