import random
import string

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_test_user():
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
