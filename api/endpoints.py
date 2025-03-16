# api/endpoints.py
class Endpoints:
    """API endpoints constants"""
    # User endpoints
    LOGIN = "/api/login"
    USERS = "/api/users"
    USER_DETAIL = "/api/users/{user_id}"
    
    # Product endpoints
    PRODUCTS = "/api/products"
    PRODUCT_DETAIL = "/api/products/{product_id}"
    
    # Order endpoints
    ORDERS = "/api/orders"
    ORDER_DETAIL = "/api/orders/{order_id}"