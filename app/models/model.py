from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app.settings import db


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="guest")
    pwrd_text = db.Column(db.String(100))
    
    # Relationships
    history = db.relationship("UserHistory", back_populates="user", cascade="all, delete-orphan")
    token = db.relationship("UserToken", back_populates="user", uselist=False)
    reviews = db.relationship("ProdReview", back_populates="user", cascade="all, delete-orphan")

    # Password helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def create_user(self):
        db.session.add(self)
        db.session.commit()
        db.session.flush()
        
class UserHistory(db.Model):
    __tablename__ = "user_history"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    bought = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    user = db.relationship("User", back_populates="history")
    product = db.relationship("Product", back_populates="history")

class UserToken(db.Model):
    __tablename__ = "user_token"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    refresh_token = db.Column(db.String(255), unique=True, nullable=False)
    token_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    token_exp_at = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="token")

# Association table (no model class)
product_tags = db.Table(
    "product_tags",
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount_percentage = db.Column(db.Float, default=0.0)
    rating = db.Column(db.Float, default=0.0)
    stock = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(50))
    weight = db.Column(db.Float)
    warranty_information = db.Column(db.String(200))
    shipping_information = db.Column(db.String(200))
    availability_status = db.Column(db.String(50))
    return_policy = db.Column(db.Text)
    minimum_order_quantity = db.Column(db.Integer, default=1)
    thumbnail = db.Column(db.String(255))
    img_url = db.Column(db.Text)
    
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"))
    brand = db.relationship('Brand', back_populates='products')

    # tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    tags = db.relationship(
        "Tag",
        secondary=product_tags,
        back_populates="products"
    )
    
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship('Category', back_populates='products')
    
    reviews = db.relationship("ProdReview", back_populates="product", cascade="all, delete-orphan")
    meta = db.relationship("ProductMeta", back_populates="product", cascade="all, delete-orphan", uselist=False)

    history = db.relationship("UserHistory", back_populates="product", cascade="all, delete-orphan")

    def create_product(self):
        db.session.add(self)
        db.session.commit()

class ProdReview(db.Model):
    __tablename__ = "prod_review"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    edited = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    product = db.relationship("Product", back_populates="reviews")

    __table_args__ = (db.UniqueConstraint("user_id", "product_id", name="uq_user_product_review"),)


class ProductMeta(db.Model):
    __tablename__ = "product_meta"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    barcode = db.Column(db.String(150), unique=False)
    qrcode = db.Column(db.Text)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product", back_populates="meta")

class Brand(db.Model):
    __tablename__ = "brands"
    
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(150), unique=True)
    
    products = db.relationship("Product", back_populates="brand")

class Tag(db.Model):
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(150), unique=True)
    products = db.relationship(
        "Product",
        secondary=product_tags,
        back_populates="tags"
    )

class Category(db.Model):
    __tablename__ = "categories"
    
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(150), unique=True)
    products = db.relationship("Product", back_populates="category")
    