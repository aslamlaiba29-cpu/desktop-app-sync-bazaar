# tests/test_cart.py
import json
from backend.models import Product, User

def test_cart_calculations(client, db):
    """Test cart math: subtotal, 8% tax, $10 shipping, grand total."""
    # 1. Create a Vendor and register a Product
    vendor = User(username="cartvendor", password_hash="hash", role="Vendor")
    db.session.add(vendor)
    db.session.commit()

    product = Product(
        name="Cart Widget",
        category="Electronics",
        price=100.0,
        stock=10,
        vendor_id=vendor.id
    )
    db.session.add(product)
    db.session.commit()

    # 2. Register & Login Customer
    client.post('/api/auth/register', json={
        "username": "cartcustomer",
        "password": "customerpass",
        "role": "Customer"
    })
    client.post('/api/auth/login', json={
        "username": "cartcustomer",
        "password": "customerpass"
    })

    # 3. Add 2 units of Product to Cart (Total subtotal = $200.0)
    client.post('/api/cart', json={
        "product_id": product.id,
        "quantity": 2
    })

    # 4. Fetch Cart and Verify calculations
    res = client.get('/api/cart')
    assert res.status_code == 200
    data = json.loads(res.data)
    
    assert data["status"] == "success"
    assert len(data["cart"]) == 1
    assert data["cart"][0]["quantity"] == 2
    assert data["cart"][0]["subtotal"] == 200.0

    calcs = data["calculations"]
    assert calcs["subtotal"] == 200.0
    assert calcs["tax"] == 16.0       # 8% of 200
    assert calcs["shipping"] == 10.0  # Flat shipping rate
    assert calcs["grand_total"] == 226.0  # 200 + 16 + 10
