import random
import string
import os
import re
from dotenv import load_dotenv

def generate_random_string(length=8) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_test_user() -> dict:
    random_string = generate_random_string()
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": f"{random_string}@test.com",
        "telephone": "1234567890",
        "address": "123 Test St",
        "city": "Test City",
        "region": "3513",
        "postcode": "12345",
        "login_name": random_string,
        "password": random_string
    }

def get_existing_user() -> dict:
    load_dotenv()
    return {
        "login_name": os.getenv("LOGIN_NAME"),
        "password": os.getenv("PASSWORD")
    }

def clean_price_text(price_text: str) -> float:
    # Remove any currency symbols and commas
    cleaned_text = re.sub(r'[£$€,]', '', price_text)

    return float(cleaned_text.strip())