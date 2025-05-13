# **Final Project – Dosa Restaurant REST API**

This project is a RESTful API backend built with **FastAPI** and **SQLite** for managing a dosa restaurant's operations. It provides CRUD functionality for **customers**, **items**, and **orders**, initialized using data from `example_orders.json`.

---

## 📁 Features

- Create, read, update, and delete:
  - Customers
  - Menu Items
  - Orders
- SQLite database with proper relational constraints (Primary & Foreign Keys)
- Swagger UI documentation at `http://127.0.0.1:8000/docs`

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vm675/IS601_Final_Project.git
   cd IS601_Final_Project

   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Mac/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn
   ```

4. **Initialize the database:**
   ```bash
   python db_init.py
   ```

5. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

---

## 🚀 API Endpoints Overview

### Customers
- `POST /customers/` – Add a new customer
- `GET /customers/{id}` – Get a customer by ID
- `PUT /customers/{id}` – Update customer info
- `DELETE /customers/{id}` – Delete a customer

### Items
- `POST /items/` – Add a new item
- `GET /items/{id}` – Get an item by ID
- `PUT /items/{id}` – Update item info
- `DELETE /items/{id}` – Delete an item

### Orders
- `POST /orders/` – Add a new order
- `GET /orders/{id}` – Get an order by ID
- `PUT /orders/{id}` – Update an order
- `DELETE /orders/{id}` – Delete an order

---

## ✅ Testing the API

Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

You’ll find an interactive Swagger UI to test all the endpoints.

---

## 📂 Files Included

- `main.py` – FastAPI server with all endpoints
- `db_init.py` – Initializes SQLite database from `example_orders.json`
- `example_orders.json` – Sample data for customers, items, and orders
- `db.sqlite` – SQLite database file (auto-generated)
