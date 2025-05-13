from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3
import time

app = FastAPI()

# Models
class Customer(BaseModel):
    cust_id: Optional[int] = None
    name: str
    phone: str

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    price: float

class Order(BaseModel):
    order_id: Optional[int] = None
    notes: str
    cust_id: int
    timestamp: Optional[int] = None

# DB connection setup with foreign keys enabled
def get_db_connection():
    conn = sqlite3.connect("db.sqlite")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Customers Endpoints
@app.post("/customers/")
def create_customer(customer: Customer):
    if customer.cust_id is not None:
        raise HTTPException(status_code=400, detail="cust_id cannot be set on POST request")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (customer.name, customer.phone))
    customer.cust_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return customer

@app.get("/customers/{cust_id}")
def read_customer(cust_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM customers WHERE id=?", (cust_id,))
    customer = cursor.fetchone()
    conn.close()
    if customer:
        return Customer(cust_id=customer[0], name=customer[1], phone=customer[2])
    raise HTTPException(status_code=404, detail="Customer not found")

@app.put("/customers/{cust_id}")
def update_customer(cust_id: int, customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM customers WHERE id = ?;", (cust_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer ID not found")

    update_query = "UPDATE customers SET "
    update_data = []
    if customer.name:
        update_query += "name=?, "
        update_data.append(customer.name)
    if customer.phone:
        update_query += "phone=? "
        update_data.append(customer.phone)

    update_query = update_query.rstrip(", ") + " WHERE id=?;"
    update_data.append(cust_id)

    cursor.execute(update_query, update_data)
    conn.commit()
    cursor.execute("SELECT id, name, phone FROM customers WHERE id=?", (cust_id,))
    updated = cursor.fetchone()
    conn.close()
    return Customer(cust_id=updated[0], name=updated[1], phone=updated[2])

@app.delete("/customers/{cust_id}")
def delete_customer(cust_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=?;", (cust_id,))
    conn.commit()
    conn.close()
    return {"message": "Customer deleted successfully"}

# Items Endpoints
@app.post("/items/")
def create_item(item: Item):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("SELECT id FROM items WHERE name = ?", (item.name,))
    if curr.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Item already exists")
    curr.execute("INSERT INTO items (name, price) VALUES (?, ?);", (item.name, item.price))
    conn.commit()
    item.id = curr.lastrowid
    conn.close()
    return item

@app.get("/items/{item_id}")
def read_item(item_id: int):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("SELECT id, name, price FROM items WHERE id=?", (item_id,))
    item = curr.fetchone()
    conn.close()
    if item:
        return Item(id=item[0], name=item[1], price=item[2])
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    if not curr.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")

    update_query = "UPDATE items SET "
    update_data = []
    if item.name:
        update_query += "name=?, "
        update_data.append(item.name)
    if item.price:
        update_query += "price=? "
        update_data.append(item.price)
    update_query = update_query.rstrip(", ") + " WHERE id=?;"
    update_data.append(item_id)
    curr.execute(update_query, update_data)
    conn.commit()
    conn.close()
    return {"message": "Item updated successfully"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("DELETE FROM items WHERE id=?;", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Item deleted successfully"}

# Orders Endpoints
@app.post("/orders/")
def create_order(order: Order):
    if order.order_id is not None:
        raise HTTPException(status_code=400, detail="order_id should not be set")

    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("SELECT id FROM customers WHERE id=?", (order.cust_id,))
    if not curr.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    timestamp = int(time.time())
    curr.execute("INSERT INTO orders (notes, cust_id, timestamp) VALUES (?, ?, ?);", (order.notes, order.cust_id, timestamp))
    order.order_id = curr.lastrowid
    order.timestamp = timestamp
    conn.commit()
    conn.close()
    return order

@app.get("/orders/{order_id}")
def read_order(order_id: int):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("SELECT id, notes, cust_id, timestamp FROM orders WHERE id=?", (order_id,))
    order = curr.fetchone()
    conn.close()
    if order:
        return Order(order_id=order[0], notes=order[1], cust_id=order[2], timestamp=order[3])
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("SELECT id FROM orders WHERE id=?", (order_id,))
    if not curr.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")

    update_query = "UPDATE orders SET "
    update_data = []
    if order.notes:
        update_query += "notes=?, "
        update_data.append(order.notes)
    update_query = update_query.rstrip(", ") + " WHERE id=?;"
    update_data.append(order_id)
    curr.execute(update_query, update_data)
    conn.commit()
    conn.close()
    return {"message": "Order updated successfully"}

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("DELETE FROM orders WHERE id=?;", (order_id,))
    conn.commit()
    conn.close()
    return {"message": "Order deleted successfully"}
