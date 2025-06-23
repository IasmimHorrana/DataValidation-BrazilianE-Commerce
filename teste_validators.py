from datetime import datetime

from src.validate import (  # ajuste conforme sua estrutura de pastas
    Customer,
    Order,
    OrderItem,
)

# Teste Customer
exemplo_customer = {
    "customer_id": "06b8999e2fba1a1fbc88172c00ba8bc7",
    "customer_unique_id": "861eff4711a542e4b93843c6dd7febb0",
    "customer_zip_code_prefix": 14409,
    "customer_city": "franca",
    "customer_state": "SP",
}

cliente = Customer(**exemplo_customer)
print("Customer válido:", cliente)

# Teste Order
exemplo_order = {
    "order_id": "8f8e6f388b28b5b6a5f0e3bb5e5d64cb",
    "customer_id": exemplo_customer["customer_id"],
    "order_status": "delivered",
    "order_purchase_timestamp": datetime(2018, 7, 6, 17, 18, 23),
    "order_approved_at": datetime(2018, 7, 6, 17, 25, 5),
    "order_delivered_carrier_date": datetime(2018, 7, 9, 20, 13, 35),
    "order_delivered_customer_date": datetime(2018, 7, 20, 21, 38, 13),
    "order_estimated_delivery_date": datetime(2018, 7, 29, 0, 0, 0),
}

pedido = Order(**exemplo_order)
print("Order válido:", pedido)

# Teste OrderItem
exemplo_order_item = {
    "order_id": exemplo_order["order_id"],
    "order_item_id": 1,
    "product_id": "product123",
    "seller_id": "seller456",
    "shipping_limit_date": datetime(2018, 7, 8, 0, 0, 0),
    "price": 99.99,
    "freight_value": 15.0,
}

item = OrderItem(**exemplo_order_item)
print("OrderItem válido:", item)
