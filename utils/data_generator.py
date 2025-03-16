# utils/data_generator.py
from faker import Faker
import random
import string
import json
import os

fake = Faker()

class DataGenerator:
    @staticmethod
    def generate_user():
        """Generate random user data"""
        return {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(length=10),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number()
        }
    
    # utils/data_generator.py (continued)
    @staticmethod
    def generate_product():
        """Generate random product data"""
        return {
            "name": fake.catch_phrase(),
            "description": fake.text(max_nb_chars=200),
            "price": round(random.uniform(10, 1000), 2),
            "category": random.choice(["Electronics", "Clothing", "Home", "Books", "Toys"]),
            "in_stock": random.choice([True, False]),
            "sku": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        }
    
    @staticmethod
    def generate_address():
        """Generate random address data"""
        return {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip": fake.zipcode(),
            "country": fake.country()
        }
    
    @staticmethod
    def load_test_data(file_path):
        """Load test data from JSON file"""
        with open(os.path.join("data", file_path), "r") as file:
            return json.load(file)
    
    @staticmethod
    def save_test_data(data, file_path):
        """Save test data to JSON file"""
        with open(os.path.join("data", file_path), "w") as file:
            json.dump(data, file, indent=2)