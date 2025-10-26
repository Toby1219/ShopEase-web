from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.model import User, Product, ProdReview, ProductMeta
from marshmallow import fields 


class UserAccSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True 
        include_fk = False
        include_relationship = True
        exclude = ["id", "password_hash", "pwrd_text"]

class ProductMetaSchemas(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductMeta
        load_instance = True

class ProductReviewSchemas(SQLAlchemyAutoSchema):
    class Meta:
        model = ProdReview
        load_instance = True

class ProductSchema(SQLAlchemyAutoSchema):
    meta = fields.Nested(ProductMetaSchemas(exclude=["id"])) 
    reviews  = fields.List(fields.Nested(ProductReviewSchemas(exclude=["id"])))
    tags = fields.Method("get_tag")
    brand = fields.Method("get_brand")
    category = fields.Method("get_category")
    
    class Meta:
        model = Product
        load_instance = True
        # include_fk = True
        # include_relationship = True
        exclude = ["weight"]
    
    def get_tag(self, obj:Product):
        # many to many schema
        return [t.name for t in obj.tags]
    
    def get_brand(self, obj:Product):
        # one to many schema
        b = obj.brand
        return b.name if b else None
    
    def get_category(self, obj:Product):
        c = obj.category
        return c.name if c else None
    
    
    

