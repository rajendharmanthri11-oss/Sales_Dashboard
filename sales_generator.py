import pandas as pd
import random
import time
from datetime import datetime

products = ["Laptop", "Mobile", "Tablet", "Headphones"]
cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad"]

file = "sales_data.csv"

# Create file if not exists
try:
    df = pd.read_csv(file)
except:
    df = pd.DataFrame(columns=["Time", "Product", "Price", "City"])

while True:
    new_sale = {
        "Time": datetime.now(),
        "Product": random.choice(products),
        "Price": random.randint(1000, 50000),
        "City": random.choice(cities)
    }

    df = pd.concat([df, pd.DataFrame([new_sale])])
    df.to_csv(file, index=False)

    print("New Sale Added:", new_sale)

    time.sleep(30)  # every 30 seconds