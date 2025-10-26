from app.settings import db, BASE_PATH
from ..models.model import Product, Brand, Category, Tag, ProductMeta
import json
from datetime import datetime

def write_db(file="utils/product.json"):
    json_file = f"{BASE_PATH}/{file}"
    
    # Load JSON
    with open(json_file, "r") as f:
        data = json.load(f)

    for p in data["products"]:
        # --- BRAND ---
        brand_name = p.get("brand")
        if brand_name:
            brand = db.session.execute(
                db.text("SELECT id FROM brands WHERE name = :name"),
                {"name": brand_name}
            ).fetchone()
            if not brand:
                db.session.execute(
                    db.text("INSERT INTO brands (name) VALUES (:name)"),
                    {"name": brand_name}
                )
                db.session.commit()
                brand = db.session.execute(
                    db.text("SELECT id FROM brands WHERE name = :name"),
                    {"name": brand_name}
                ).fetchone()
            brand_id = brand.id
        else:
            brand_id = None

        # --- CATEGORY ---
        cat_name = p.get("category")
        if cat_name:
            category = db.session.execute(
                db.text("SELECT id FROM categories WHERE name = :name"),
                {"name": cat_name}
            ).fetchone()
            if not category:
                db.session.execute(
                    db.text("INSERT INTO categories (name) VALUES (:name)"),
                    {"name": cat_name}
                )
                db.session.commit()
                category = db.session.execute(
                    db.text("SELECT id FROM categories WHERE name = :name"),
                    {"name": cat_name}
                ).fetchone()
            category_id = category.id
        else:
            category_id = None

        # --- PRODUCT ---
        db.session.execute(
            db.text("""
                INSERT INTO products 
                    (id, title, description, price, discount_percentage, rating, stock, sku, weight, 
                    warranty_information, shipping_information, availability_status, 
                    return_policy, minimum_order_quantity, thumbnail, img_url, brand_id, category_id)
                VALUES 
                    (:id, :title, :description, :price, :discount, :rating, :stock, :sku, :weight,
                    :warranty, :shipping, :availability, :return_policy, :min_qty, :thumb, :img, 
                    :brand_id, :category_id)
            """),
            {
                "id": p["id"],
                "title": p["title"],
                "description": p.get("description"),
                "price": p["price"],
                "discount": p.get("discountPercentage", 0.0),
                "rating": p.get("rating", 0.0),
                "stock": p.get("stock", 0),
                "sku": p.get("sku"),
                "weight": p.get("weight"),
                "warranty": p.get("warrantyInformation"),
                "shipping": p.get("shippingInformation"),
                "availability": p.get("availabilityStatus"),
                "return_policy": p.get("returnPolicy"),
                "min_qty": p.get("minimumOrderQuantity"),
                "thumb": p.get("thumbnail"),
                "img": ",".join(p.get("images", [])),
                "brand_id": brand_id,
                "category_id": category_id
            }
        )
        db.session.commit()

        # --- TAGS ---
        for t in p.get("tags", []):
            tag = db.session.execute(
                db.text("SELECT id FROM tags WHERE name = :name"),
                {"name": t}
            ).fetchone()
            if not tag:
                db.session.execute(db.text("INSERT INTO tags (name) VALUES (:name)"), {"name": t})
                db.session.commit()
                tag = db.session.execute(
                    db.text("SELECT id FROM tags WHERE name = :name"),
                    {"name": t}
                ).fetchone()
            db.session.execute(
                db.text("INSERT INTO product_tags (product_id, tag_id) VALUES (:pid, :tid)"),
                {"pid": p["id"], "tid": tag.id}
            )
            db.session.commit()

        # --- META ---
        meta = p.get("meta", {})
        db.session.execute(
            db.text("""
                INSERT INTO product_meta (created_at, updated_at, barcode, qrcode, product_id)
                VALUES (:created, :updated, :barcode, :qrcode, :pid)
            """),
            {
                "created": meta.get("createdAt", datetime.utcnow().isoformat()),
                "updated": meta.get("updatedAt", datetime.utcnow().isoformat()),
                "barcode": meta.get("barcode"),
                "qrcode": meta.get("qrCode"),
                "pid": p["id"]
            }
        )
        db.session.commit()
