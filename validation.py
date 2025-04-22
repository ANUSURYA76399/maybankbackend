import re
from datetime import datetime

def validate_card_number(card_number):
    return len(card_number) == 16 and card_number.isdigit()

def validate_zip_code(zip_code):
    # Accept 5 or 6 digit zip codes
    return (len(zip_code) == 5 or len(zip_code) == 6) and zip_code.isdigit()

def validate_currency(currency):
    valid_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'MYR', 'SGD', 'INR']
    return currency in valid_currencies

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None

def validate_phone_number(phone):
    return len(phone) == 10 and phone.isdigit() and phone[0] in '6789'

def validate_expiry_date(expiry):
    try:
        month, year = map(int, expiry.split('/'))
        if not (1 <= month <= 12):
            return False
        now = datetime.now()
        year += 2000 if year < 100 else 0
        expiry_date = datetime(year, month, 1)
        return expiry_date > now.replace(day=1)
    except:
        return False

def validate_username(username):
    return username.isalnum() and 3 <= len(username) <= 20

def validate_password(password):
    if len(password) < 8:
        return False
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).+$'
    return re.match(pattern, password) is not None

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False