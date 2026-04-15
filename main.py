from turtledemo.round_dance import stop

from tracker import Expense, ValidationError

flag = True
while flag:
    amount = input("Enter the amount: ").strip()
    try:
        if not Expense.is_valid_amount(amount):
            raise ValidationError("Amount is invalid! | Try format : 10.50 or 10")
        print("Amount accepted!")
    except ValidationError as ve:
        print(f"Error: {ve}")

    date = input("Enter the date: ").strip()
    try:
        if not Expense.is_valid_date(date):
            raise ValidationError("Date is invalid! | Try format : YYYY-MM-DD")
        print("Date accepted!")
    except ValidationError as ve:
        print(f"Error: {ve}")

    if amount == "" or date == "":
        flag = False

