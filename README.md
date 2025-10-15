## Inventory Management & Billing System -- Python Console Application

## Project Overview

This is a command-line Python application built to enable small businesses to track their inventory, process sales, and generate receipts. The system maintains product information, stock quantities, and sales data, providing fundamental reporting capabilities.

------------------------------------------------------------------------
## Project Structure

INVENTORY MANAGEMENT/
│
├── Main.py
├── inventory.csv
└── sales.csv
------------------------------------------------------------------------

## Features
Product Management: Add, update, delete, and search products

CSV Import/Export: Bulk import products from CSV files

Real-time Stock Tracking: Automatic stock updates during sales

Product Search: Find products by ID or name

------------------------------------------------------------------------
## Data Storage
File Formats
inventory.csv: Stores product information

Columns: product_id, name, price, stock_quantity

sales.csv: Stores transaction history

Columns: datetime, total_amount, discount, final_amount

Bill Files: Individual transaction receipts

Format: bill_YYYYMMDD_HHMMSS.[txt|csv]

------------------------------------------------------------------------
## Billing System
Shopping Cart: Add/remove items with quantity management

Discount System: Apply percentage or fixed amount discounts

Checkout Process: Complete sales with automatic stock deduction

Bill Generation: Display detailed receipts in terminal

--------------------------------------------------------------------------
## Reports & Analytics

Sales Reports: Generate reports for custom date ranges

Daily Sales: View daily transaction summaries

Low Stock Alerts: Identify products needing restocking

Product Statistics: View inventory value and stock levels

--------------------------------------------------------------------------
## Main Menu Options
1. Inventory Management
View All Products: Display complete product catalog

Add Product: Add new products with ID, name, price, and stock

Update Product: Modify existing product details

Delete Product: Remove products from inventory

Search Product: Find products by ID or name

Import Products: Bulk import from CSV file

2. Billing & Sales
View Cart: Display current shopping cart

Add to Cart: Add products to cart with quantities

Remove from Cart: Remove or reduce item quantities

Apply Discount: Add percentage or fixed discounts

Clear Discount: Remove applied discounts

Checkout: Complete sale and generate bill

3. Reports & Analytics
Generating Reports
Select Option 3 from main menu

Daily Sales: View transactions for specific date

Low Stock: Identify products needing restock

------------------------------------------------------------------------

