import re


class Expense:

    def __init__(self,amount,category,date):
        self.amount = amount
        self.category = category
        self.date = date

    @staticmethod
    def is_valid_date(date):
        pattern = "^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$" #  YYYY-MM-DD
        if re.match(pattern, date):
            return True
        return False

    @staticmethod
    def is_valid_amount(amount):
        pattern = "^\d+(\.\d{1,2})?$" #  12.50 | 12
        if re.match(pattern, amount):
            return True
        return False

    def __str__(self):
        return f"[{self.date}] {self.category}: {self.amount}"
