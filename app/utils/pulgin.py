import json
import random
from datetime import datetime

from ..settings import BASE_PATH, Path
from ..models.model import (User, Product, ProductMeta, ProdReview, Tag, Category, Brand, db)

def gen_password(name:str):
    num = random.choice([x for x in range(111, 300)])
    return f"{name.lower()}{num}".strip()
 
def create(instance):
    db.session.add(instance)
    db.session.commit()
    db.session.flush()
        
def write_data(file="utils/product.json"):
    json_file = f"{BASE_PATH}/{file}"
    
    if not Path(json_file).exists():
        print("Invalid File database is empty")
        
    with open(json_file) as f:
        j_data = json.load(f)
      
    for data in j_data["products"]:
        product = Product.query.filter_by(title=data["title"]).first()
        if not product:
            product = Product(
                title=data["title"],
                description=data["description"],
                price=data["price"],
                discount_percentage=data["discountPercentage"],
                rating=data["rating"],
                stock=data["stock"],
                sku=data["sku"],
                weight=data["weight"],
                warranty_information=data["warrantyInformation"],
                shipping_information=data["shippingInformation"],
                availability_status=data["availabilityStatus"],
                return_policy=data["returnPolicy"],
                minimum_order_quantity=data["minimumOrderQuantity"],
                thumbnail=data["thumbnail"],
                img_url=json.dumps(data["images"]),
            )
            create(product)
            
            product_meta = ProductMeta(
                    created_at=datetime.fromisoformat(data["meta"]["createdAt"].replace("Z", "")),
                    updated_at=datetime.fromisoformat(data["meta"]["updatedAt"].replace("Z", "")),
                    barcode=data["meta"]["barcode"],
                    qrcode=data["meta"]["qrCode"], product=product
                )
            
            create(product_meta) 
        
        for review in data["reviews"]:

            user = User.query.filter_by(
                    email=review["reviewerEmail"]
                ).first()
            
            if not user:
                user = User(
                    username=review["reviewerName"],
                    email=review["reviewerEmail"],
                    role="user"
                )
                pwrd = gen_password(review["reviewerName"])
                user.pwrd_text = pwrd
                user.set_password(pwrd)
                user.create_user()
            
            rev = ProdReview.query.filter_by(user_id=user.id, product_id=product.id).first()
            if not rev:
                rev = ProdReview(
                        rating=review["rating"],
                        comment=review["comment"],
                        date=datetime.fromisoformat(review["date"].replace("Z", "")),
                        user=user, product=product
                    )
                db.session.add(rev)
                db.session.commit()
                db.session.flush()
            
        # for t in data["tags"]:
        #     tag = Tag.query.filter_by(name=t).first()
        #     print("\n FOUND TAG: ", tag, "\n")
        #     if not tag:
        #         tag = Tag(name=t)
        #         create(tag)
        #         if product not in tag.products:
        #             tag.products.append(product)
        #         print("\n CREATED TAG: ", tag, "\n")
                
                
        # b = data.get("brand", None)
        # if b:
        #     for b in data['brand'].split(","):
        #         brand = Brand.query.filter_by(name=b).first()
        #         if not brand:
        #             brand = Brand(name=b)
        #             product.brand = brand
        #             create(brand)
        
        # c = data.get("category", None)
        # if c:
        #     for c in data["category"].split(","):
        #         cate = Category.query.filter_by(name=c).first()
                
        #         if not cate:
        #             cate = Category(name=c)
        #             product.category = cate
        #             create(cate)
        
        # db.session.commit()
        
        print(f"Saved {product.title} to db")

def run_func():
    write_data()            

            
            
            
            
        
