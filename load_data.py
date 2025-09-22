
import os
import pandas as pd
from database import engine
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

FILE_TABLE_MAP = {
    "olist_customers_dataset.csv": "olist_customers",
    "olist_orders_dataset.csv": "olist_orders",
    "olist_order_items_dataset.csv": "olist_order_items",
    "olist_order_payments_dataset.csv": "olist_order_payments",
    "olist_order_reviews_dataset.csv": "olist_order_reviews",
    "olist_products_dataset.csv": "olist_products",
    "olist_sellers_dataset.csv": "olist_sellers",
    "olist_geolocation_dataset.csv": "olist_geolocation",
    "product_category_name_translation.csv": "product_category_name_translation",
}

def load_all(if_exists="replace"):
    for fname, table in FILE_TABLE_MAP.items():
        path = os.path.join(DATA_DIR, fname)
        if not os.path.exists(path):
            print(f"Skip {fname}: not found in data/")
            continue
        print(f"Loading {fname} -> {table} ...")
        df = pd.read_csv(path)
        df.columns = [c.strip() for c in df.columns]
        df.to_sql(table, engine, if_exists=if_exists, index=False, method="multi")
        print("OK")

if __name__ == "__main__":
    load_all()
