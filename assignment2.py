import random
import uuid
from faker import Faker
import mysql.connector

fake = Faker()

PRODUCT_CATEGORIES = {
    "Electronics": [
    "Smartphone", "Laptop", "Headphones", "Smartwatch", "Camera", "Tablet",
    "Monitor", "Printer", "Router", "Drone", "Powerbank", "VR Headset"
],
"Clothing": [
    "T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress", "Hat",
    "Scarf", "Gloves", "Socks", "Sweater", "Belt"
],

    "Books": ["Novel", "Textbook", "Cookbook", "Biography", "Comics", "Dictionary"],
    "Home": ["Sofa", "Lamp", "Table", "Chair", "Carpet", "Mirror"],
    "Sports": ["Football", "Tennis Racket", "Basketball", "Yoga Mat", "Bicycle", "Helmet"]
}

def generate_customer():
    """Generate a random customer record with realistic email."""
    name = fake.name()
    # convert name into email format
    username = name.lower().replace(" ", ".").replace("'", "")
    email = f"{username}@{random.choice(['gmail.com', 'yahoo.com', 'hotmail.com'])}"
    return (
        str(uuid.uuid4()),
        name,
        email,
        fake.country(),
        fake.city()
    )

def generate_product():
    """Generate a random product based on its category."""
    category = random.choice(list(PRODUCT_CATEGORIES.keys()))
    product_name = random.choice(PRODUCT_CATEGORIES[category])
    # Add a random modifier for realism, e.g., "Pro", "XL", "2025 Edition"
    modifier = random.choice(["", " Pro", " XL", " Mini", " 2025 Edition", " Set"])
    name = f"{product_name}{modifier}".strip()
    price = round(random.uniform(5.0, 2000.0), 2)
    return (str(uuid.uuid4()), name, category, price)

def generate_order(customer_ids, product_ids):
    """Generate a random order linked to existing customers and products."""
    return (
        str(uuid.uuid4()),
        random.choice(customer_ids),
        random.choice(product_ids),
        random.randint(1, 5),
        fake.date_between(start_date="-2y", end_date="today")
    )


def insert_data(host, user, password, database,
                total_customers=1_000_000,
                total_products=1_000_000,
                total_orders=1_000_000,
                batch_size=10_000):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id CHAR(36) PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            country VARCHAR(100),
            city VARCHAR(100)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id CHAR(36) PRIMARY KEY,
            name VARCHAR(100),
            category VARCHAR(50),
            price DECIMAL(10,2)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id CHAR(36) PRIMARY KEY,
            customer_id CHAR(36),
            product_id CHAR(36),
            quantity INT,
            order_date DATE,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    connection.commit()

    print("🧍 Inserting customers...")
    customer_ids = []
    for i in range(0, total_customers, batch_size):
        batch = [generate_customer() for _ in range(batch_size)]
        customer_ids.extend([r[0] for r in batch])
        cursor.executemany("INSERT INTO customers (id, name, email, country, city) VALUES (%s, %s, %s, %s, %s)", batch)
        connection.commit()
        print(f"Inserted {min(i + batch_size, total_customers)} / {total_customers} customers")

    print("📦 Inserting products...")
    product_ids = []
    for i in range(0, total_products, batch_size):
        batch = [generate_product() for _ in range(batch_size)]
        product_ids.extend([r[0] for r in batch])
        cursor.executemany("INSERT INTO products (id, name, category, price) VALUES (%s, %s, %s, %s)", batch)
        connection.commit()
        print(f"Inserted {min(i + batch_size, total_products)} / {total_products} products")

    print("🧾 Inserting orders...")
    for i in range(0, total_orders, batch_size):
        batch = [generate_order(customer_ids, product_ids) for _ in range(batch_size)]
        cursor.executemany("INSERT INTO orders (id, customer_id, product_id, quantity, order_date) VALUES (%s, %s, %s, %s, %s)", batch)
        connection.commit()
        print(f"Inserted {min(i + batch_size, total_orders)} / {total_orders} orders")

    cursor.close()
    connection.close()
    print("✅ All data inserted successfully!")


if __name__ == "__main__":
    insert_data(
        host="localhost",
        user="root",
        password="MySQL_Student123",
        database="hw2",
        total_customers=1_100_000,
        total_products=1_200_000,
        total_orders=1_100_000,
        batch_size=20_000
    )
