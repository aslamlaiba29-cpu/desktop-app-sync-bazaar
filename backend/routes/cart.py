# backend/routes/cart.py
from flask import Blueprint, request, jsonify, session
from backend.models import db, CartItem, WishlistItem, Product
import logging

bp = Blueprint('cart', __name__)

@bp.route('/cart', methods=['GET'])
def get_cart():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Login required"}), 401

    items = CartItem.query.filter_by(user_id=user_id).all()
    results = []
    total = 0.0
    for item in items:
        prod = item.product
        if not prod:
            continue
        subtotal = prod.price * item.quantity
        total += subtotal
        results.append({
            "id": item.id,
            "product_id": prod.id,
            "product_name": prod.name,
            "price": prod.price,
            "stock": prod.stock,
            "quantity": item.quantity,
            "subtotal": subtotal,
            "image_url": prod.image_url
        })

    # Core Software Engineering Requirement: Cart Calculations
    tax = round(total * 0.08, 2)       # 8% Tax
    shipping = 10.0 if total > 0 else 0.0
    grand_total = round(total + tax + shipping, 2)

    return jsonify({
        "status": "success",
        "cart": results,
        "calculations": {
            "subtotal": round(total, 2),
            "tax": tax,
            "shipping": shipping,
            "grand_total": grand_total
        }
    })

@bp.route('/cart', methods=['POST'])
def add_to_cart():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Login required"}), 401

    data = request.get_json() or {}
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return jsonify({"status": "error", "message": "Product ID is required"}), 400

    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        return jsonify({"status": "error", "message": f"Only {product.stock} units left in stock"}), 400

    # Check if already in cart
    item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        if product.stock < (item.quantity + quantity):
            return jsonify({"status": "error", "message": f"Cannot add more items. Only {product.stock} units available"}), 400
        item.quantity += quantity
    else:
        item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(item)

    db.session.commit()
    logging.info(f"User {session.get('username')} added product {product.name} (Qty: {quantity}) to cart")
    return jsonify({"status": "success", "message": "Item added to cart successfully"})

@bp.route('/cart/<int:item_id>', methods=['PUT'])
def update_cart_quantity(item_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Login required"}), 401

    item = CartItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()
    data = request.get_json() or {}
    quantity = int(data.get('quantity', 1))

    if quantity <= 0:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"status": "success", "message": "Item removed from cart"})

    if item.product.stock < quantity:
        return jsonify({"status": "error", "message": f"Only {item.product.stock} units available in stock"}), 400

    item.quantity = quantity
    db.session.commit()
    return jsonify({"status": "success", "message": "Cart updated successfully"})

@bp.route('/cart/<int:item_id>', methods=['DELETE'])
def delete_cart_item(item_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Login required"}), 401

    item = CartItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({"status": "success", "message": "Item removed from cart"})


# Wishlist Endpoints

@bp.route('/wishlist', methods=['GET'])
def get_wishlist():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Login required"}), 401

    items = WishlistItem.query.filter_by(user_id=user_id).all()
    results = []
    for item in items:
        p = item.product
        if not p:
            continue
        results.append({
            "id": item.id,
            "product_id": p.id,
            "product_name": p.name,
            "price": p.price,
            "stock": p.stock,
            "image_url": p.image_url
        })
    return jsonify({"status": "success", "wishlist": results})

@bp.route('/wishlist', methods=['POST'])
def toggle_wishlist():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Login required"}), 401

    data = request.get_json() or {}
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({"status": "error", "message": "Product ID is required"}), 400

    item = WishlistItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"status": "success", "message": "Removed from wishlist", "in_wishlist": False})
    else:
        item = WishlistItem(user_id=user_id, product_id=product_id)
        db.session.add(item)
        db.session.commit()
        return jsonify({"status": "success", "message": "Added to wishlist", "in_wishlist": True})
