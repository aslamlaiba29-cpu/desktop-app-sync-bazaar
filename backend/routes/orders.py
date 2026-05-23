# backend/routes/orders.py
from flask import Blueprint, request, jsonify, session
from backend.models import db, CartItem, Order, OrderItem, Product, Notification
from backend.sync import broker
from datetime import datetime
import logging

bp = Blueprint('orders', __name__)

@bp.route('', methods=['GET'])
def get_orders():
    user_id = session.get('user_id')
    role = session.get('role')
    if not user_id:
        return jsonify({"status": "error", "message": "Login required"}), 401

    if role == 'Admin':
        orders = Order.query.order_by(Order.created_at.desc()).all()
    elif role == 'Vendor':
        # Find orders that contain products owned by this vendor
        order_items = OrderItem.query.join(Product).filter(Product.vendor_id == user_id).all()
        order_ids = list(set(item.order_id for item in order_items))
        orders = Order.query.filter(Order.id.in_(order_ids)).order_by(Order.created_at.desc()).all()
    else:
        # Customer orders
        orders = Order.query.filter_by(customer_id=user_id).order_by(Order.created_at.desc()).all()

    results = []
    for order in orders:
        items = []
        for item in order.items:
            # For vendors, only show their products in the order description
            if role == 'Vendor' and item.product.vendor_id != user_id:
                continue
            items.append({
                "product_id": item.product_id,
                "product_name": item.product.name if item.product else "Unknown Product",
                "quantity": item.quantity,
                "price": item.price,
                "vendor_name": item.product.vendor.username if item.product and item.product.vendor else "Unknown"
            })
        results.append({
            "id": order.id,
            "customer_name": order.customer.username if order.customer else "Anonymous",
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "items": items
        })

    return jsonify({"status": "success", "orders": results})

@bp.route('/checkout', methods=['POST'])
def checkout():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Login required"}), 401

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"status": "error", "message": "Shopping cart is empty"}), 400

    # 1. Validation & Stock check
    subtotal = 0.0
    for item in cart_items:
        prod = item.product
        if not prod:
            return jsonify({"status": "error", "message": "Product in cart no longer exists"}), 404
        if prod.stock < item.quantity:
            # Exception Handling: Out of stock
            return jsonify({
                "status": "error",
                "message": f"Sync Conflict: Product '{prod.name}' is out of stock! Only {prod.stock} left."
            }), 400
        subtotal += prod.price * item.quantity

    # Calculations
    tax = round(subtotal * 0.08, 2)
    shipping = 10.0
    total_amount = round(subtotal + tax + shipping, 2)

    # 2. Process Transaction
    order = Order(customer_id=user_id, total_amount=total_amount, status='Pending')
    db.session.add(order)
    db.session.flush()  # gets order.id

    for item in cart_items:
        prod = item.product
        # Decrement stock
        old_stock = prod.stock
        prod.stock -= item.quantity
        
        # Save order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=prod.id,
            quantity=item.quantity,
            price=prod.price
        )
        db.session.add(order_item)

        # Notify vendor
        vendor_notification = Notification(
            user_id=prod.vendor_id,
            message=f"New Order placed for '{prod.name}' (Qty: {item.quantity}) by {session.get('username')}"
        )
        db.session.add(vendor_notification)

        # Clear item from cart
        db.session.delete(item)

        # Real-time stock sync announcement
        broker.announce("stock_update", {
            "product_id": prod.id,
            "product_name": prod.name,
            "new_stock": prod.stock
        })

    # Notify customer
    customer_notification = Notification(
        user_id=user_id,
        message=f"Your order #{order.id} has been placed successfully for a total of ${total_amount}."
    )
    db.session.add(customer_notification)
    
    db.session.commit()
    logging.info(f"Order #{order.id} placed by Customer {session.get('username')} total: ${total_amount}")

    # Real-time order sync announcement for vendors/admins
    broker.announce("order_placed", {
        "order_id": order.id,
        "customer_name": session.get('username'),
        "total_amount": total_amount,
        "status": "Pending"
    })

    return jsonify({
        "status": "success",
        "message": "Order checkout processed successfully!",
        "order_id": order.id
    }), 201

@bp.route('/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    role = session.get('role')
    user_id = session.get('user_id')
    if role != 'Vendor' and role != 'Admin':
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    order = Order.query.get_or_404(order_id)
    data = request.get_json() or {}
    new_status = data.get('status')  # Processing, Shipped, Delivered

    if new_status not in ['Pending', 'Processing', 'Shipped', 'Delivered']:
        return jsonify({"status": "error", "message": "Invalid order status value"}), 400

    order.status = new_status
    
    # Send notification to customer
    cust_notification = Notification(
        user_id=order.customer_id,
        message=f"Your Order #{order.id} status has been updated to '{new_status}'."
    )
    db.session.add(cust_notification)
    db.session.commit()

    logging.info(f"Order #{order.id} status updated to {new_status}")

    # Real-time status sync announcement
    broker.announce("order_status", {
        "order_id": order.id,
        "status": new_status
    })

    return jsonify({"status": "success", "message": f"Order status updated to '{new_status}'"})
