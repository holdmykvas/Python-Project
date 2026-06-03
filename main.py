import os

from tracker import Expense, ValidationError, BudgetManager

#implement entering category as today

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
        return
    else:
        print("\nHow would you like to view your expenses?")
        print("1. Default (Order Added)")
        print("2. Sorted by Date")
        print("3. Sorted by Amount (Highest to Lowest)")

        view_choice = input("Select a sort option: ").strip()

        if view_choice == "1":
            expenses = manager.expenses
        elif view_choice == "2":
            expenses = sorted(manager.expenses, key=lambda e: e.date)
        elif view_choice == "3":
            expenses = sorted(manager.expenses, key=lambda e: float(e.amount), reverse=True)
        else:
            print("Invalid input!")
            expenses = manager.expenses

        print("\nExpenses List:")
        for expense in expenses:
            print(expense)

def handle_filter_expenses(manager):
    handle_unique_category(manager)
    cat_search = input("Enter category to search: ").strip()
    results = list(manager.generate_expense_category(cat_search))
    if not results:
        print("No expenses found for that category.")
    else:
        for exp in results:
            print(exp)

def handle_unique_category(manager):
    if not manager.expenses:
        print("No expenses recorded yet.")
    else:
        unique_categories = {exp.category for exp in manager.expenses}
        print("Categories used: \n*", "\n* ".join(unique_categories))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    manager = BudgetManager()
    print(" Welcome to the Budget Manager!")
    while True:
        print("\nMenu Options:")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter by Category")
        print("4. View Unique Categories")
        print("5. Run Analytics & Forecast")
        print("6. Exit \n")

        choice = input("Select an option: ").strip()

        if choice == "1":
            handle_add_expense(manager)
            manager.save_data()

        elif choice == "2":
            handle_view_expenses(manager)

        elif choice == "3":
            handle_filter_expenses(manager)

        elif choice == "4":
            handle_unique_category(manager)

        elif choice == "5":
            print(manager.generate_spending_report())

        elif choice == "6":
            manager.save_data()
            print("Data saved to JSON. Exiting...")
            break

        else:
            print("Invalid input! | Try again.")

        if choice != "7":
            input("\nPress Enter to return to the main menu.")
        clear_screen()

if __name__ == "__main__":
    main()