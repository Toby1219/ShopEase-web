from flask import Response, jsonify, request
from flask_login import current_user
from flask_sqlalchemy.query import Query
from flask_classful import FlaskView, route
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jti, decode_token

from sqlalchemy import or_, func
from ..models.model import Product, Category, Tag, Brand, product_tags, User
from ..schemas.schema import ProductSchema
from ..settings import PER_PAGE
from collections import OrderedDict

blacklist = set()

class AuthMixin:
    def check_auth(self):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Missing token"}), 401
      
class ApiAuth(AuthMixin, MethodView):
    def __init__(self):
        super().__init__()
        self.context = OrderedDict()

    @jwt_required()
    def get(self):
        if current_user:
            self.context["Username"] = current_user.username
            self.context["Email"] = current_user.email
            self.context['Message'] = f"Welcome {current_user.username}! This is your profile."
        else:
            current_user_ = get_jwt_identity()
            self.context['Message'] = f"Welcome {current_user_}! This is your profile."
            self.context["Current User"] = current_user_
        return jsonify(self.context)
#  Note use mongo db to store data needed around 
    def post(self):
        """ Login """
        email = None
        if current_user:
            email = current_user.email
            user:User = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({"msg": "Invalid credentials"}), 401
        else:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")
            user:User = User.query.filter_by(email=email).first()
            if not user and user.check_password(password):
                return jsonify({"msg": "Invalid credentials"}), 401
            
        access = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        access_decoded = decode_token(access)
        refresh_decoded = decode_token(refresh_token)
        # session["access_decoded"] = access_decoded
        self.context["Message"] = "Login sucessfull"
        self.context["email"] = email
        self.context["access_token"] = access
        self.context["refresh_token"] = refresh_token
        self.context["access_token_exp"] = access_decoded["exp"]
        self.context["refresh_token_exp"] = refresh_decoded["exp"]
        return jsonify(self.context)
        
    @jwt_required(refresh=True)
    def put(self) -> Response:
        """ Refresh """
        current_user_ = get_jwt_identity()
        new_token = create_access_token(identity=current_user_)
        token = request.headers.get("Authorization")
        self.context["Message"] = "Token Refreshed"
        self.context["access_token"] = new_token
        self.context["refresh_token"] = token.replace("Bearer", "").strip()
        return jsonify(self.context)
    
    @jwt_required()
    def delete(self):
        """Logout (invalidate access token)"""
        token = request.headers.get("Authorization")
        
        jti = get_jti(token.replace("Bearer", "").strip())
        blacklist.add(jti)
        return jsonify({"Message":"Token have been blacklisted"})
        

class ApiRoutes(FlaskView):
    route_base = "/api/"
    decorators = [jwt_required()]
    
    def __init__(self):
        super().__init__()
        self.product_schema = ProductSchema(many=True)
        self.context = {}
    
    def index(self,  page=None, per_page=None):
        if not page:
            page = request.args.get("page", 1, type=int)
        p = Product.query.paginate(page=page, per_page=per_page if per_page else PER_PAGE, error_out=False)

        self.context["page"] = p.page
        self.context["per_page"] = p.per_page
        self.context["total_items"] = p.total
        self.context["total_pages"] = p.pages
        self.context["product"] = self.product_schema.dump(p.items)
        return jsonify(self.context)

    @route("/search", methods=["GET"])
    def search(self, sq=None, tag=None, category=None, sort=None, page=None, per_page=None):
        if not sq:
            sq = request.args.get("query", None, type=str)
        name = request.args.get("name", None, type=str)
        min_price = request.args.get("from", None, type=float)
        max_price = request.args.get("to", None, type=float)
        if not sort:
            sort = request.args.get("sort", "asc", type=str).lower()
        if not tag:
            tag = request.args.get("tag", None, type=str)
        if not category:
            category = request.args.get("category", None, type=str)            
        brand = request.args.get("brand", None, type=str)
        sku = request.args.get("sku", None, type=str)
        query: Query = Product.query
        q, arg = None, None
       
        if sq:
            print(f"\n Found: {sq} \n")
            q, arg =self.any_search_handler(query, sq)
            
        if name:
            q, arg = self.name_handler(name, query)
        
        if max_price or min_price:
            q, arg =  self.price_handler(query, min_price, max_price)
        
        if sku:
            q, arg = self.sku_handler(query, sku)
            
        if brand:
            q, arg = self.others_handler(query, brand, Brand.name, Brand)
        
        if tag:
            q, arg = self.others_handler(query, tag, Tag.name, product_tags, Tag)
            
        if category:
            q, arg = self.others_handler(query, category, Category.name, Category)
        
        if not q and not arg:
            s = "Highest to Lowest" if sort == "desc" else "Lowest to Highest"
            q, arg = query, f"All product price sorted from ({s})"    
    
        if sort == "desc":
            q = q.order_by(Product.price.desc())
        else:
            q = q.order_by(Product.price.asc())
        if not page:
            page = request.args.get("page", 1, type=int)
        p = q.paginate(page=page, per_page=per_page if per_page else PER_PAGE, error_out=False)
        self.context["page"] = p.page
        self.context["per_page"] = p.per_page
        self.context["total_items"] = p.total
        self.context["total_pages"] = p.pages
        self.context["Query"] = arg
        self.context["product"] = self.product_schema.dump(p.items)
    
        return jsonify(self.context)
        
    def name_handler(self, name, query:Query):
        prod = query.filter(func.lower(Product.title) == name.lower())
        return prod, name 

    def price_handler(self, query:Query, min_price=None, max_price=None):
        if min_price and max_price:
            q = query.filter(Product.price.between(min_price, max_price))
        elif min_price:
            q = query.filter(Product.price >= min_price)
        elif max_price:
            q = query.filter(Product.price <= max_price)
        
        return q, f"price range from {min_price if min_price else ''} - {max_price if max_price else ""}"

    def sku_handler(self, query:Query, sku:str):
        prod = query.filter(func.lower(Product.sku) == sku.lower())
        return prod, sku

    def others_handler(self, query:Query, pram:str, obj:Product, rel:object, rel2:object=None) -> tuple[Query, list[str]]:
        q = query.join(rel)
        if rel2:
            q = query.join(rel).join(rel2)
        
        prams = [b.strip().lower() for b in pram.split(",")]
        
        filters = [obj.ilike(f"%{b}") for b in prams]
        q = q.filter(or_(*filters))

        return q, prams
    
    def any_search_handler(self, query:Query, param):
        q = query.join(Brand, isouter=True).join(Category, isouter=True).join(product_tags, isouter=True).join(Tag, isouter=True)
        search_term = f"%{param.lower()}%"
        q = q.filter(
            or_(
                func.lower(Product.title).like(search_term),
                func.lower(Product.sku).like(search_term),
                func.lower(Brand.name).like(search_term),
                func.lower(Category.name).like(search_term),
                func.lower(Tag.name).like(search_term),
            )
        )
        return q, param
       