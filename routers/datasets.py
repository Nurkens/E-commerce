from fastapi import APIRouter, HTTPException, Query
from database import SessionLocal
from sqlalchemy import text
import pandas as pd
import os

router = APIRouter(prefix="/api", tags=["datasets"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

DATASETS = {
    "customers": {"csv": "olist_customers_dataset.csv", "table": "olist_customers"},
    "orders": {"csv": "olist_orders_dataset.csv", "table": "olist_orders"},
    "order_items": {"csv": "olist_order_items_dataset.csv", "table": "olist_order_items"},
    "order_payments": {"csv": "olist_order_payments_dataset.csv", "table": "olist_order_payments"},
    "order_reviews": {"csv": "olist_order_reviews_dataset.csv", "table": "olist_order_reviews"},
    "products": {"csv": "olist_products_dataset.csv", "table": "olist_products"},
    "sellers": {"csv": "olist_sellers_dataset.csv", "table": "olist_sellers"},
    "geolocation": {"csv": "olist_geolocation_dataset.csv", "table": "olist_geolocation"},
    "category_translation": {"csv": "product_category_name_translation.csv", "table": "product_category_name_translation"},
}

def read_csv_head(file_name, limit):
    path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    return df.head(limit).to_dict(orient="records"), list(df.columns)

@router.get("/datasets")
def list_datasets():
    return list(DATASETS.keys())

@router.get("/{dataset}")
def get_dataset(
    dataset: str,
    limit: int = Query(10, ge=1, le=2000),
    column: str | None = None,
    value: str | None = None,
    source: str = Query("auto", regex="^(auto|csv|db)$")
):
    
    if dataset not in DATASETS:
        raise HTTPException(status_code=404, detail="Dataset not found")
    ds = DATASETS[dataset]
    table = ds["table"]
    csv_file = ds["csv"]

    if source in ("auto", "db"):
        session = SessionLocal()
        try:
            sql = text(f"SELECT * FROM {table} LIMIT :limit")
            rows = session.execute(sql, {"limit": limit}).mappings().all()
            if rows:
                df = pd.DataFrame(rows)
                if column and value:
                    if column not in df.columns:
                        raise HTTPException(status_code=400, detail=f"Column {column} not found in DB table")
                    df = df[df[column].astype(str) == value]
                return {"source": "db", "columns": list(df.columns), "rows": df.head(limit).to_dict(orient="records")}
        except Exception:
            if source == "db":
                raise HTTPException(status_code=500, detail="DB read error or table not found")
        finally:
            session.close()

    try:
        rows, cols = read_csv_head(csv_file, limit=limit)
        if column and value:
            filtered = []
            for r in rows:
                if column in r and str(r[column]) == value:
                    filtered.append(r)
            return {"source": "csv", "columns": cols, "rows": filtered[:limit]}
        return {"source": "csv", "columns": cols, "rows": rows}
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"CSV file {csv_file} not found in data/")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV: {e}")
