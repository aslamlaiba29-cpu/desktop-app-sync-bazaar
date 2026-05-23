# backend/routes/products.py
from flask import Blueprint, request, jsonify, session
from backend.models import db, Product, User, Review
from backend.sync import broker
import logging

bp = Blueprint('products', __name__)

@bp.route('', methods=['GET'])
def get_products():
    category = request.args.get('category')
    search = request.args.get('search')
    vendor_id = request.args.get('vendor_id')

    query = Product.query

    # Customers only see approved items, vendors/admins can see all
    role = session.get('role')
    if role != 'Admin' and role != 'Vendor':
        query = query.filter_by(status='Approved')

    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.name.like(f"%{search}%") | Product.description.like(f"%{search}%"))
    if vendor_id:
        query = query.filter_by(vendor_id=vendor_id)

    products = query.all()
    results = []
    for p in products:
        results.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "category": p.category,
            "price": p.price,
            "stock": p.stock,
            "image_url": p.image_url,
            "vendor_id": p.vendor_id,
            "vendor_name": p.vendor.username if p.vendor else "Unknown",
            "status": p.status,
            "rating": p.rating
        })

    return jsonify({"status": "success", "products": results})

@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    p = Product.query.get_or_404(product_id)
    reviews = []
    for r in p.reviews:
        reviews.append({
            "id": r.id,
            "username": r.user.username if r.user else "Anonymous",
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({
        "status": "success",
        "product": {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "category": p.category,
            "price": p.price,
            "stock": p.stock,
            "image_url": p.image_url,
            "vendor_id": p.vendor_id,
            "vendor_name": p.vendor.username if p.vendor else "Unknown",
            "status": p.status,
            "rating": p.rating,
            "reviews": reviews
        }
    })

@bp.route('', methods=['POST'])
def create_product():
    if session.get('role') != 'Vendor':
        return jsonify({"status": "error", "message": "Only vendors can create products"}), 403

    data = request.get_json() or {}
    name = data.get('name')
    description = data.get('description')
    category = data.get('category')
    price = data.get('price')
    stock = data.get('stock', 0)
    image_url = data.get('image_url')

    if not name or not category or price is None:
        return jsonify({"status": "error", "message": "Name, category, and price are required"}), 400

    product = Product(
        name=name,
        description=description,
        category=category,
        price=float(price),
        stock=int(stock),
        image_url=image_url,
        vendor_id=session.get('user_id'),
        status='Approved'  # Automatically approved for this simulation/app setup
    )
    db.session.add(product)
    db.session.commit()

    logging.info(f"Vendor {session.get('username')} created product: {name} (Stock: {stock})")
    
    # Real-time synchronization broadcast
    broker.announce("product_added", {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "price": product.price,
        "stock": product.stock,
        "vendor_name": session.get('username')
    })

    return jsonify({"status": "success", "message": "Product created successfully", "product_id": product.id}), 201

@bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Auth check
    if session.get('role') != 'Vendor' or product.vendor_id != session.get('user_id'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    data = request.get_json() or {}
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.category = data.get('category', product.category)
    product.price = float(data.get('price', product.price))
    
    old_stock = product.stock
    new_stock = int(data.get('stock', product.stock))
    product.stock = new_stock
    product.image_url = data.get('image_url', product.image_url)

    db.session.commit()

    logging.info(f"Vendor {session.get('username')} updated product: {product.name} (Stock: {old_stock} -> {new_stock})")

    # Real-time synchronization broadcast if stock changed
    if old_stock != new_stock:
        broker.announce("stock_update", {
            "product_id": product.id,
            "product_name": product.name,
            "new_stock": new_stock
        })

    return jsonify({"status": "success", "message": "Product updated successfully"})

@bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Auth check
    if session.get('role') != 'Vendor' or product.vendor_id != session.get('user_id'):
        if session.get('role') != 'Admin':
            return jsonify({"status": "error", "message": "Unauthorized"}), 403

    product_id_val = product.id
    product_name = product.name
    db.session.delete(product)
    db.session.commit()

    logging.info(f"Product deleted: {product_name} (ID: {product_id_val})")

    # Real-time synchronization broadcast
    broker.announce("product_deleted", {
        "product_id": product_id_val,
        "product_name": product_name
    })

    return jsonify({"status": "success", "message": "Product deleted successfully"})

@bp.route('/<int:product_id>/reviews', methods=['POST'])
def add_review(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Login required to post reviews"}), 401

    product = Product.query.get_or_404(product_id)
    data = request.get_json() or {}
    rating = int(data.get('rating', 5))
    comment = data.get('comment', '')

    review = Review(product_id=product.id, user_id=user_id, rating=rating, comment=comment)
    db.session.add(review)
    
    # Recalculate average product rating
    all_reviews = Review.query.filter_by(product_id=product.id).all()
    total_rating = sum(r.rating for r in all_reviews) + rating
    product.rating = round(total_rating / (len(all_reviews) + 1), 1)

    db.session.commit()

    logging.info(f"Customer {session.get('username')} reviewed {product.name}: {rating} stars")

    return jsonify({"status": "success", "message": "Review added successfully"})

@bp.route('/<int:product_id>/moderate', methods=['POST'])
def moderate_product(product_id):
    if session.get('role') != 'Admin':
        return jsonify({"status": "error", "message": "Admin authorization required"}), 403

    product = Product.query.get_or_404(product_id)
    data = request.get_json() or {}
    status = data.get('status', 'Approved')  # Approved, Rejected

    product.status = status
    db.session.commit()

    logging.info(f"Admin moderated product: {product.name} set status to {status}")

    return jsonify({"status": "success", "message": f"Product status set to {status}"})
