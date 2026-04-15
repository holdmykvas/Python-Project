import re


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

    def add_expense(self,expense_obj):
        self.expenses.append(expense_obj)
        pass

    def save_data(self):
        self.filename = "data.json"
        with open(self.filename,"w") as f:
            list_of_dict = [{"amount": e.amount,"date": e.date} for e in self.expenses]
        json.dump(list_of_dict,f,indent=4)