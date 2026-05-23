from datetime import datetime
from backend.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False, default='Customer')  # Customer, Vendor, Admin
    email = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(256), nullable=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(32), nullable=False, default='Approved')  # Pending, Approved
    rating = db.Column(db.Float, nullable=False, default=5.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vendor = db.relationship('User', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f"<Product {self.name} Price={self.price} Stock={self.stock}>"

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_entries', lazy=True))

    def __repr__(self):
        return f"<CartItem user={self.user_id} product={self.product_id} qty={self.quantity}>"

class WishlistItem(db.Model):
    __tablename__ = 'wishlist_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('wishlist_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('wishlist_entries', lazy=True))

    def __repr__(self):
        return f"<WishlistItem user={self.user_id} product={self.product_id}>"

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(32), nullable=False, default='Pending')  # Pending, Processing, Shipped, Delivered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('User', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f"<Order {self.id} Customer={self.customer_id} Total={self.total_amount}>"

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    order = db.relationship('Order', backref=db.backref('items', lazy=True, cascade="all, delete-orphan"))
    product = db.relationship('Product')

    def __repr__(self):
        return f"<OrderItem order={self.order_id} product={self.product_id} qty={self.quantity}>"

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User')

    def __repr__(self):
        return f"<Review product={self.product_id} user={self.user_id} rating={self.rating}>"

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

    def __repr__(self):
        return f"<Notification user={self.user_id} read={self.is_read}>"

class ProcessModel(db.Model):
    __tablename__ = 'process_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    config_json = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f"<ProcessModel {self.name}>"

class SPIRecord(db.Model):
    __tablename__ = 'spi_record'
    id = db.Column(db.Integer, primary_key=True)
    defect_density = db.Column(db.Float, nullable=False)
    velocity = db.Column(db.Integer, nullable=False)
    maturity_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SPIRecord {self.id} score={self.maturity_score}>"

class GitRepo(db.Model):
    __tablename__ = 'git_repo'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256), nullable=False)
    current_branch = db.Column(db.String(64), nullable=False)
    last_commit_hash = db.Column(db.String(40), nullable=True)
    history_json = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f"<GitRepo {self.path}>"

class CodeSmell(db.Model):
    __tablename__ = 'code_smell'
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(256), nullable=False)
    line_start = db.Column(db.Integer, nullable=False)
    line_end = db.Column(db.Integer, nullable=False)
    smell_type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)
    resolved = db.Column(db.Boolean, default=False)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CodeSmell {self.smell_type} in {self.file_path}>"

class CodeReview(db.Model):
    __tablename__ = 'code_review'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(256), nullable=False)
    code_smells = db.Column(db.Integer, default=0)
    status = db.Column(db.String(64), default='Pending')  # Pending, Approved, Changes Requested
    comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CodeReview {self.file_name} status={self.status}>"

class TestResult(db.Model):
    __tablename__ = 'test_result'
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(16), nullable=False)  # PASSED, FAILED, SKIPPED
    duration = db.Column(db.Float, nullable=True)  # seconds
    output = db.Column(db.Text, nullable=True)
    run_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TestResult {self.test_name} {self.status}>"
