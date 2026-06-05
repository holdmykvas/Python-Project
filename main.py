import os

from datetime import datetime
from tracker import Expense, ValidationError, BudgetManager, Colors

def handle_add_expense(manager):
    try:
        amount = input("Enter the amount: ").strip()
        if not Expense.is_valid_amount(amount):
            raise ValidationError(f"{Colors.RED}Error: Amount is invalid! | Try format : 10.50 or 10{Colors.RESET}")
        print(f"{Colors.GREEN}--Amount accepted!{Colors.RESET}")

        category = input("Enter the category: ").strip()
        print(f"{Colors.GREEN}--Category accepted! {Colors.RESET}\n")

        date = input("Enter the date: ").strip()
        if date.lower() == "today":
            date = datetime.now().strftime("%Y-%m-%d")
        if not Expense.is_valid_date(date):
            raise ValidationError(f"{Colors.RED}Error: Date is invalid! | Try format : YYYY-MM-DD{Colors.RESET}")
        print(f"{Colors.GREEN}--Date accepted! {Colors.RESET}\n")

        expense = Expense(amount, category, date)
        manager.add_expense(expense)
    except ValidationError as e:
        print(e)

def handle_view_expenses(manager):
    if not manager.expenses:
        print(f"{Colors.RED} No expenses added yet! {Colors.RESET}")
        return
    else:
        print(f"\n{Colors.CYAN}How would you like to view your expenses?{Colors.RESET}")
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
            print(f"{Colors.RED}Invalid input! Defaulting{Colors.RESET}")
            expenses = manager.expenses

        print(f"\n{Colors.CYAN}Expenses List:{Colors.RESET}")
        for expense in expenses:
            print(expense)

def handle_filter_expenses(manager):
    handle_unique_category(manager)
    cat_search = input("Enter category to search: ").strip()
    results = list(manager.generate_expense_category(cat_search))

    if not results:
        print(f"{Colors.RED}No expenses found for that category.{Colors.RESET}")
    else:
        for exp in results:
            print(exp)

def handle_unique_category(manager):
    if not manager.expenses:
        print(f"{Colors.RED}No expenses recorded yet.{Colors.RESET}")
    else:
        unique_categories = {exp.category for exp in manager.expenses}
        print("Categories used: \n*", "\n* ".join(unique_categories))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    manager = BudgetManager()
    print(" Welcome to the Budget Manager!")
    while True:
        print(f"\n{Colors.CYAN}Menu Options:{Colors.RESET}")
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
        #TODO make entering of numbers look the same.if it's 200.00 it must stay this way if it's 200 it must become 200.00
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
            print(f"{Colors.RED}Invalid input! | Try again.{Colors.RESET}")

        if choice != "7":
            input("\nPress Enter to return to the main menu.")
        clear_screen()

if __name__ == "__main__":
    main()