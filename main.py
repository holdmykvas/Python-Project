from tracker import Expense, ValidationError, BudgetManager

#BUGS:
# doesn't see data.json to load from

#ideas:
#add expense
#


def main():
    manager = BudgetManager()

    while True:

        print("Welcome to the Budget Manager!")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Sort By Date")
        print("4. Filter by Category")
        print("5. View Unique Categories")
        print("6. Run Analytics & Forecast")
        print("7. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":

            amount = input("Enter the amount: ").strip()
            if not Expense.is_valid_amount(amount):
                raise ValidationError("Error: Amount is invalid! | Try format : 10.50 or 10")
                continue
            print("--Amount accepted!")

            category = input("Enter the category: ").strip()
            print("--Category accepted!")

            date = input("Enter the date: ").strip()
            if not Expense.is_valid_date(date):
                raise ValidationError("Error: Date is invalid! | Try format : YYYY-MM-DD")
            print("--Date accepted!")

            expense = Expense(amount, category, date)
            manager.add_expense(expense)
            print("--Expense added!")

        elif choice == "2":
            if not manager.expenses:
                print("No expenses added yet!")
            else:
                for exp in manager.expenses:
                    print(exp)

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

if __name__ == "__main__":
    main()