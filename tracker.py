import json
import re

def log_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[LOG] Executing: {action_name}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

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
        pass

    @log_action("Adding new expense")
    def add_expense(self,expense_obj):
        self.expenses.append(expense_obj)

    def save_data(self):
        with open(self.filename,"w") as f:
            list_of_dict = [{"amount": e.amount, "category": e.category ,"date": e.date} for e in self.expenses]
            json.dump(list_of_dict,f,indent=4)

    def generate_expense_category(self,category):
        for exp in self.expenses:
            if exp.category.lower() == category.lower():
                yield exp