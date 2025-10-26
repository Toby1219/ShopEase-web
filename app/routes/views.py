from flask_classful import FlaskView, route
from flask_login import current_user, login_required
from flask import Response, render_template, request
# from flask_sqlalchemy.query import Query
from sqlalchemy.sql.expression import func
from ..models.model import Product, Category, Tag
from itertools import zip_longest
from .api import ApiRoutes


class Apiview(FlaskView):
    route_base = "/api/doc"
    decorators = [login_required]
    
    def __init__(self):
        super().__init__()
        self.context = {}
    
    def index(self):
        self.load_auth_user()
        return render_template("api/home.html", context=self.context)
    
    @route("/home", methods=["GET"])
    def home(self):
        self.load_auth_user()
        prod = Product.query
        prod_names = prod.all()
        prod_name_value = [" ".join(p.title.split(" ")[0:2]) if len(p.title) > 3 else p.title for p in prod_names]
        prod_name_dataset = [p.title for p in prod_names]
        
        self.context["combined_name"] = list(zip_longest(prod_name_value, prod_name_dataset, fillvalue=" "))
        
        self.context["prod_sku"] = [p.sku for p in prod.all()]
        self.context["categories"] = [c.name.capitalize() for c in Category.query.all()]
        self.context["tags"] = [t.name.capitalize() for t in Tag.query.all()]
        return render_template("api/api_view.html", context=self.context)
    
    def load_auth_user(self):
        if current_user.is_authenticated:
            self.context["current_user"] = current_user.is_authenticated
            self.context["current_username"] = current_user.username
 

class WebView(FlaskView):
    route_base = '/web/'   
    # decorators = [login_required]
    
    def __init__(self):
        super().__init__()
        self.context = {}
        self.api = ApiRoutes()
        
    
    def index(self):
        prod = Product.query
        self.context["current_user"] = current_user.is_authenticated
        self.context["f_products"] = prod.order_by(func.random()).limit(3).all()
        return render_template("landing/index.html", context=self.context)
    
    @route("/products", methods=["GET"])
    def product_listing(self):
        self.context["current_user"] = current_user.is_authenticated
        r_q = request.args.get("s", None, type=str)
        tag = request.args.get(key="tag", default=None, type=str)
        category = request.args.get(key="category", default=None, type=str)
        sort = request.args.get(key="sort", default=None, type=str)
        page = request.args.get(key="page", default=1, type=int)
        if r_q:
            response = self.api.search(sq=r_q, page=page, per_page=6)
        elif tag:
            response = self.api.search(tag=tag, page=page, per_page=6)
        elif category:
            response = self.api.search(category=category,  page=page, per_page=6)
        elif sort:
            response = self.api.search(category=category,  page=page, per_page=6)
        else:
            response: Response = self.api.index(page=page, per_page=6)  
    
        tags = Tag.query.all()
        categories = Category.query.all()
        self.context["tag"] = [tag.name for tag in tags]
        self.context["category"] = [cate.name for cate in categories]
        self.context["products"] = response.json["product"]
        self.context["response_json"] = response.json
        
        return render_template("landing/prod_l.html", context=self.context)
    
    # /product/product-name
    @route("/product/<string:name>", methods=["GET"])
    def product_single(self, name):
        prod = Product.query.filter_by(title=name).first()
        recomend_prod = Product.query.filter(Product.category.has(name=prod.category.name)).order_by(func.random()).limit(4).all()        
        self.context["current_user"] = current_user.is_authenticated
        self.context["product"] = prod
        self.context["category"] = ", ".join([c.name.capitalize() for c in list(prod.category)]) if isinstance(prod.category.name, list) else prod.category.name.capitalize()
        self.context["tags"] = ", ".join([t.name.capitalize() for t in prod.tags])
        self.context["reviews"] = prod.reviews
        self.context["recommended_products"] = recomend_prod
        return render_template("landing/prod_s.html", context=self.context)
        
    @route("/profile", methods=["GET"])
    def profile(self):
        self.context["current_user"] = current_user.is_authenticated 
        self.context["user"] = current_user 
    
        return render_template("landing/profile.html", context=self.context)
    
    # @route("/check-out", methods=["GET"])
    # def check_out(self):
    #     self.context["current_user"] = current_user.is_authenticated
    #     return render_template("landing/checkout.html")   
    
    # @route("/cart", methods=["GET"])
    # def cart_page(self):
    #     self.context["current_user"] = current_user.is_authenticated
    #     return render_template("landing/cart_page.html", context=self.context)   
    