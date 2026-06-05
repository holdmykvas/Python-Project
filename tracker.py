from datetime import datetime
import json
import re

def log_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[LOG] Executing: {action_name}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class Expense:
    def __init__(self,amount,category,date):
        self.amount = amount
        self.category = category
        self.date = date

    @staticmethod
    def is_valid_date(date):
        pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"  #  YYYY-MM-DD
        if re.match(pattern, date):
            return True
        return False

    @staticmethod
    def is_valid_amount(amount):
        pattern = r"^\d+(\.\d{1,2})?$" #  12.50 | 12
        if re.match(pattern, amount):
            return True
        return False

    def __str__(self):
        return f"[{self.date}] {self.category}: {self.amount}"

class ValidationError(Exception):
    pass


class BudgetManager:
    def __init__(self,filename = "data.json"):
        self.expenses = []
        self.filename = filename
        self.load_data()

    @log_action(f"{Colors.GREEN}Adding new expense{Colors.RESET}")
    def add_expense(self,expense_obj):
        self.expenses.append(expense_obj)

    def load_data(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                for item in data:
                    loaded_expense = Expense(item["amount"], item["category"], item["date"])
                    self.expenses.append(loaded_expense)
            print(f"{Colors.GREEN}[LOG] Successfully loaded {len(self.expenses)} expenses from {self.filename}{Colors.RESET}")
        except FileNotFoundError:
            print(f"{Colors.RED}[LOG] No existing data file found. Starting fresh.{Colors.RESET}")
        except json.JSONDecodeError:
            print(f"{Colors.RED}[LOG] Error reading the data file. Starting fresh.{Colors.RESET}")


    def save_data(self):
        with open(self.filename,"w") as f:
            list_of_dict = [{"amount": e.amount, "category": e.category ,"date": e.date} for e in self.expenses]
            json.dump(list_of_dict,f,indent=4)

    def generate_expense_category(self,category):
        for exp in self.expenses:
            if exp.category.lower() == category.lower():
                yield exp

    def generate_spending_report(self):
        if not self.expenses:
            return f"{Colors.RED}Not enough data to generate a report!{Colors.RESET}"

        categories = {exp.category for exp in self.expenses}

        category_totals = {
            cat: sum(float(exp.amount) for exp in self.expenses if exp.category == cat)
            for cat in categories
        }

        total_spent = sum(category_totals.values())

        most_expensive_cat = max(category_totals, key=lambda k: category_totals[k])

        dates = [datetime.strptime(exp.date, "%Y-%m-%d") for exp in self.expenses]
        days_diff = (max(dates) - min(dates)).days + 1
        daily_average = total_spent / days_diff
        forecast_30_days = daily_average * 30
#TODO SORTING OF BREAKDOWN
        report = f"\n{Colors.CYAN}=== SPENDING & ANALYTICS REPORT ==={Colors.RESET}\n"
        report += f"Total Expenses Logged: {len(self.expenses)}\n"
        report += f"Total Amount Spent: {total_spent:.2f}\n"
        report += f"Most Expensive Category: '{most_expensive_cat}' ({category_totals[most_expensive_cat]:.2f})\n"
        report += "-----------------------------------\n"
        report += "Category Breakdown:\n"
        for cat, total in category_totals.items():
            percentage = (total / total_spent) * 100
            report += f"  - {cat}: {total:.2f} ({percentage:.1f}%)\n"
        report += "-----------------------------------\n"
        report += f"{Colors.BOLD}Daily Average Spend:{Colors.RESET} {daily_average:.2f}\n"
        report += f"{Colors.BOLD}Projected 30-Day Spend:{Colors.RESET}  {forecast_30_days:.2f} \n"
        report += "==================================="
        return report