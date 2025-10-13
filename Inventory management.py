import os
import csv
from datetime import datetime, date, timedelta

class Product:
    def __init__(self, product_id, name, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'stock_quantity': self.stock_quantity
        }
    
    def __str__(self):
        return f"{self.product_id}: {self.name} - ${self.price:.2f} (Stock: {self.stock_quantity})"

class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.total = product.price * quantity
    
    def to_dict(self):
        return {
            'product_id': self.product.product_id,
            'name': self.product.name,
            'price': self.product.price,
            'quantity': self.quantity,
            'total': self.total
        }

class Sale:
    def __init__(self, items, total_amount, sale_datetime, discount=0):
        self.items = items
        self.total_amount = total_amount
        self.datetime = sale_datetime
        self.discount = discount
        self.final_amount = total_amount - discount
    
    def to_dict(self):
        return {
            'datetime': self.datetime.isoformat(),
            'items': [item.to_dict() for item in self.items],
            'total_amount': self.total_amount,
            'discount': self.discount,
            'final_amount': self.final_amount
        }

class InventoryManager:
    def __init__(self, data_file='inventory.csv'):
        self.data_file = data_file
        self.products = self.load_data()
    
    def load_data(self):
        products = {}
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            product = Product(
                                row['product_id'],
                                row['name'],
                                float(row['price']),
                                int(row['stock_quantity'])
                            )
                            products[product.product_id] = product
                        except (ValueError, KeyError) as e:
                            print(f"Error parsing product data: {e}")
                            continue
                print(f"Loaded {len(products)} products from {self.data_file}")
            except Exception as e:
                print(f"Error loading inventory data: {e}")
        else:
            print("No existing inventory file found. Starting with empty inventory.")
        return products
    
    def save_data(self):
        try:
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['product_id', 'name', 'price', 'stock_quantity']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for product in self.products.values():
                    writer.writerow(product.to_dict())
            return True
        except Exception as e:
            print(f"Error saving inventory data: {e}")
            return False
    
    def add_product(self, product_id, name, price, stock_quantity):
        if product_id in self.products:
            print("Product ID already exists!")
            return False
        
        if price <= 0:
            print("Price must be greater than zero!")
            return False
        
        if stock_quantity < 0:
            print("Stock quantity cannot be negative!")
            return False
        
        self.products[product_id] = Product(product_id, name, price, stock_quantity)
        if self.save_data():
            print("Product added successfully!")
            return True
        return False
    
    def update_product(self, product_id, name=None, price=None, stock_quantity=None):
        if product_id not in self.products:
            print("Product not found!")
            return False
        
        product = self.products[product_id]
        if name is not None:
            product.name = name
        if price is not None:
            if price <= 0:
                print("Price must be greater than zero!")
                return False
            product.price = price
        if stock_quantity is not None:
            if stock_quantity < 0:
                print("Stock quantity cannot be negative!")
                return False
            product.stock_quantity = stock_quantity
        
        if self.save_data():
            print("Product updated successfully!")
            return True
        return False
    
    def delete_product(self, product_id):
        if product_id not in self.products:
            print("Product not found!")
            return False
        
        del self.products[product_id]
        if self.save_data():
            print("Product deleted successfully!")
            return True
        return False
    
    def search_product(self, keyword):
        results = []
        for product in self.products.values():
            if (keyword.lower() in product.name.lower() or 
                keyword.lower() == product.product_id.lower()):
                results.append(product)
        return results
    
    def get_product(self, product_id):
        return self.products.get(product_id)
    
    def view_all_products(self):
        if not self.products:
            print("No products available!")
            return
        
        print("\n" + "="*60)
        print("ALL PRODUCTS")
        print("="*60)
        print(f"{'ID':<10} {'Name':<20} {'Price':<10} {'Stock':<10}")
        print("-"*60)
        for product in self.products.values():
            print(f"{product.product_id:<10} {product.name:<20} ${product.price:<9.2f} {product.stock_quantity:<10}")
        print("="*60)
    
    def import_products(self, import_file):
        if not os.path.exists(import_file):
            print(f"Import file {import_file} not found!")
            return False
        
        try:
            imported_count = 0
            with open(import_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        product_id = row['product_id']
                        name = row['name']
                        price = float(row['price'])
                        stock_quantity = int(row['stock_quantity'])
                        
                        if product_id in self.products:
                            print(f"Product {product_id} already exists. Skipping.")
                            continue
                        
                        if price <= 0:
                            print(f"Invalid price for product {product_id}. Skipping.")
                            continue
                        
                        if stock_quantity < 0:
                            print(f"Invalid stock quantity for product {product_id}. Skipping.")
                            continue
                        
                        self.products[product_id] = Product(product_id, name, price, stock_quantity)
                        imported_count += 1
                    except (ValueError, KeyError) as e:
                        print(f"Error parsing product data: {e}. Skipping row.")
                        continue
            
            if self.save_data():
                print(f"Successfully imported {imported_count} products from {import_file}")
                return True
            return False
        except Exception as e:
            print(f"Error importing products: {e}")
            return False

class BillingSystem:
    def __init__(self, inventory_manager, sales_file='sales.csv'):
        self.inventory_manager = inventory_manager
        self.sales_file = sales_file
        self.cart = []
        self.sales = self.load_sales()
    
    def load_sales(self):
        sales = []
        if os.path.exists(self.sales_file):
            try:
                with open(self.sales_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            # For simplicity, we're just storing basic sale info
                            total_amount = float(row['total_amount'])
                            discount = float(row.get('discount', 0))
                            sale_datetime = datetime.fromisoformat(row['datetime'])
                            
                            # Create a sale with empty items (we don't store them in this simplified version)
                            sale = Sale([], total_amount, sale_datetime, discount)
                            sales.append(sale)
                        except (ValueError, KeyError) as e:
                            print(f"Error parsing sale data: {e}")
                            continue
                print(f"Loaded {len(sales)} sales records from {self.sales_file}")
            except Exception as e:
                print(f"Error loading sales data: {e}")
        else:
            print("No existing sales file found. Starting with empty sales history.")
        return sales
    
    def save_sales(self):
        try:
            with open(self.sales_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['datetime', 'total_amount', 'discount', 'final_amount']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for sale in self.sales:
                    writer.writerow({
                        'datetime': sale.datetime.isoformat(),
                        'total_amount': sale.total_amount,
                        'discount': sale.discount,
                        'final_amount': sale.final_amount
                    })
            return True
        except Exception as e:
            print(f"Error saving sales data: {e}")
            return False
    
    def add_to_cart(self, product_id, quantity):
        product = self.inventory_manager.get_product(product_id)
        if not product:
            print("Product not found!")
            return False
        
        if quantity <= 0:
            print("Quantity must be greater than zero!")
            return False
        
        if product.stock_quantity < quantity:
            print(f"Insufficient stock! Only {product.stock_quantity} available.")
            return False
        
        # Check if product already in cart
        for item in self.cart:
            if item.product.product_id == product_id:
                item.quantity += quantity
                item.total = item.product.price * item.quantity
                print("Item quantity updated in cart!")
                return True
        
        # Add new item to cart
        self.cart.append(OrderItem(product, quantity))
        print("Item added to cart!")
        return True
    
    def remove_from_cart(self, product_id, quantity=None):
        for i, item in enumerate(self.cart):
            if item.product.product_id == product_id:
                if quantity is None or quantity >= item.quantity:
                    self.cart.pop(i)
                    print("Item removed from cart!")
                else:
                    item.quantity -= quantity
                    item.total = item.product.price * item.quantity
                    print("Item quantity updated in cart!")
                return True
        print("Item not found in cart!")
        return False
    
    def view_cart(self):
        if not self.cart:
            print("Cart is empty!")
            return
        
        print("\n" + "="*60)
        print("SHOPPING CART")
        print("="*60)
        total = 0
        for i, item in enumerate(self.cart, 1):
            print(f"{i}. {item.product.name} - {item.quantity} x ${item.product.price:.2f} = ${item.total:.2f}")
            total += item.total
        
        print("-"*60)
        print(f"Total: ${total:.2f}")
        print("="*60)
    
    def apply_discount(self, discount_type, value):
        if not self.cart:
            print("Cart is empty!")
            return 0
        
        total = sum(item.total for item in self.cart)
        
        if discount_type == "percentage":
            if value < 0 or value > 100:
                print("Discount percentage must be between 0 and 100!")
                return 0
            discount = total * (value / 100)
        elif discount_type == "fixed":
            if value < 0 or value > total:
                print(f"Fixed discount must be between 0 and {total}!")
                return 0
            discount = value
        else:
            print("Invalid discount type! Use 'percentage' or 'fixed'.")
            return 0
        
        print(f"Discount applied: ${discount:.2f}")
        return discount
    
    def checkout(self, discount=0):
        if not self.cart:
            print("Cart is empty!")
            return None
        
        # Calculate total
        total = sum(item.total for item in self.cart)
        
        if discount < 0 or discount > total:
            print("Invalid discount amount!")
            return None
        
        # Create sale record
        sale = Sale(self.cart.copy(), total, datetime.now(), discount)
        self.sales.append(sale)
        self.save_sales()
        
        # Update inventory
        for item in self.cart:
            product = self.inventory_manager.get_product(item.product.product_id)
            product.stock_quantity -= item.quantity
        self.inventory_manager.save_data()
        
        # Clear cart
        self.cart.clear()
        
        print("Checkout completed successfully!")
        return sale
    
    def generate_bill(self, sale, file_format='txt'):
        if file_format not in ['txt', 'csv']:
            print("Invalid file format! Choose 'txt' or 'csv'.")
            return False
        
        filename = f"bill_{sale.datetime.strftime('%Y%m%d_%H%M%S')}.{file_format}"
        
        try:
            if file_format == 'txt':
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("="*50 + "\n")
                    file.write("BILL\n")
                    file.write("="*50 + "\n")
                    file.write(f"Date: {sale.datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write("-"*50 + "\n")
                    file.write("Items:\n")
                    for item in sale.items:
                        file.write(f"  {item.product.name} - {item.quantity} x ${item.product.price:.2f} = ${item.total:.2f}\n")
                    file.write("-"*50 + "\n")
                    file.write(f"Subtotal: ${sale.total_amount:.2f}\n")
                    if sale.discount > 0:
                        file.write(f"Discount: -${sale.discount:.2f}\n")
                    file.write(f"Total: ${sale.final_amount:.2f}\n")
                    file.write("="*50 + "\n")
            else:  # CSV
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['BILL'])
                    writer.writerow(['Date', sale.datetime.strftime('%Y-%m-%d %H:%M:%S')])
                    writer.writerow([])
                    writer.writerow(['Product', 'Quantity', 'Unit Price', 'Total'])
                    for item in sale.items:
                        writer.writerow([item.product.name, item.quantity, f"${item.product.price:.2f}", f"${item.total:.2f}"])
                    writer.writerow([])
                    writer.writerow(['Subtotal', '', '', f"${sale.total_amount:.2f}"])
                    if sale.discount > 0:
                        writer.writerow(['Discount', '', '', f"-${sale.discount:.2f}"])
                    writer.writerow(['Total', '', '', f"${sale.final_amount:.2f}"])
            
            print(f"Bill saved as {filename}")
            return True
        except Exception as e:
            print(f"Error generating bill: {e}")
            return False
    
    def get_daily_sales(self, target_date=None):
        if target_date is None:
            target_date = datetime.now().date()
        
        daily_sales = []
        for sale in self.sales:
            if sale.datetime.date() == target_date:
                daily_sales.append(sale)
        
        return daily_sales
    
    def get_sales_report(self, start_date=None, end_date=None):
        if start_date is None:
            start_date = datetime.now().date() - timedelta(days=7)  # Default to last 7 days
        if end_date is None:
            end_date = datetime.now().date()
        
        report = {
            'start_date': start_date,
            'end_date': end_date,
            'total_sales': 0,
            'total_amount': 0,
            'transactions': []
        }
        
        for sale in self.sales:
            if start_date <= sale.datetime.date() <= end_date:
                report['transactions'].append(sale)
                report['total_sales'] += 1
                report['total_amount'] += sale.final_amount
        
        return report
    
    def get_low_stock_products(self, threshold=5):
        low_stock = []
        for product in self.inventory_manager.products.values():
            if product.stock_quantity <= threshold:
                low_stock.append(product)
        return low_st