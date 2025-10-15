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
        self.current_discount = 0
        self.sales = self.load_sales()
    
    def load_sales(self):
        sales = []
        if os.path.exists(self.sales_file):
            try:
                with open(self.sales_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            total_amount = float(row['total_amount'])
                            discount = float(row.get('discount', 0))
                            sale_datetime = datetime.fromisoformat(row['datetime'])
                            
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
        
        for item in self.cart:
            if item.product.product_id == product_id:
                item.quantity += quantity
                item.total = item.product.price * item.quantity
                print("Item quantity updated in cart!")
                return True
        
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
        print(f"Subtotal: ${total:.2f}")
        if self.current_discount > 0:
            print(f"Discount: -${self.current_discount:.2f}")
            print(f"Final Total: ${total - self.current_discount:.2f}")
        else:
            print(f"Total: ${total:.2f}")
        print("="*60)
    
    def apply_discount(self, discount_type, value):
        if not self.cart:
            print("Cart is empty!")
            return False
        
        total = sum(item.total for item in self.cart)
        
        if discount_type == "percentage":
            if value < 0 or value > 100:
                print("Discount percentage must be between 0 and 100!")
                return False
            self.current_discount = total * (value / 100)
        elif discount_type == "fixed":
            if value < 0 or value > total:
                print(f"Fixed discount must be between 0 and {total}!")
                return False
            self.current_discount = value
        else:
            print("Invalid discount type! Use 'percentage' or 'fixed'.")
            return False
        
        print(f"Discount applied: ${self.current_discount:.2f}")
        return True
    
    def clear_discount(self):
        self.current_discount = 0
        print("Discount cleared!")
    
    def checkout(self):
        if not self.cart:
            print("Cart is empty!")
            return None
        
        total = sum(item.total for item in self.cart)
        
        if self.current_discount < 0 or self.current_discount > total:
            print("Invalid discount amount!")
            return None
        
        sale = Sale(self.cart.copy(), total, datetime.now(), self.current_discount)
        self.sales.append(sale)
        self.save_sales()
        
        for item in self.cart:
            product = self.inventory_manager.get_product(item.product.product_id)
            product.stock_quantity -= item.quantity
        self.inventory_manager.save_data()
        
        self.cart.clear()
        self.current_discount = 0
        
        print("Checkout completed successfully!")
        return sale
    
    def display_bill(self, sale):
        """Display bill in terminal instead of generating file"""
        print("\n" + "="*50)
        print("BILL")
        print("="*50)
        print(f"Date: {sale.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*50)
        print("Items:")
        for item in sale.items:
            print(f"  {item.product.name} - {item.quantity} x ${item.product.price:.2f} = ${item.total:.2f}")
        print("-"*50)
        print(f"Subtotal: ${sale.total_amount:.2f}")
        if sale.discount > 0:
            print(f"Discount: -${sale.discount:.2f}")
        print(f"Total: ${sale.final_amount:.2f}")
        print("="*50)
        print("Thank you for your purchase!")
    
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
            start_date = datetime.now().date() - timedelta(days=7)
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
        return low_stock
    
    def display_sales_report(self, start_date=None, end_date=None):
        report = self.get_sales_report(start_date, end_date)
        
        print("\n" + "="*60)
        print("SALES REPORT")
        print("="*60)
        print(f"Period: {report['start_date']} to {report['end_date']}")
        print(f"Total Transactions: {report['total_sales']}")
        print(f"Total Revenue: ${report['total_amount']:.2f}")
        
        if report['transactions']:
            print("\nRecent Transactions:")
            print("-"*60)
            for i, sale in enumerate(report['transactions'][-5:], 1):  # Show last 5 transactions
                print(f"{i}. {sale.datetime.strftime('%Y-%m-%d %H:%M')} - ${sale.final_amount:.2f}")
        
        print("="*60)

def main():
    inventory_manager = InventoryManager()
    billing_system = BillingSystem(inventory_manager)
    
    while True:
        print("\n" + "="*60)
        print("STORE MANAGEMENT SYSTEM")
        print("="*60)
        print("1. Inventory Management")
        print("2. Billing & Sales")
        print("3. Reports & Analytics")
        print("4. Exit")
        print("-"*60)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            inventory_menu(inventory_manager)
        elif choice == '2':
            billing_menu(billing_system)
        elif choice == '3':
            reports_menu(billing_system, inventory_manager)
        elif choice == '4':
            print("Thank you for using Store Management System!")
            break
        else:
            print("Invalid choice! Please try again.")

def inventory_menu(inventory_manager):
    while True:
        print("\n" + "="*60)
        print("INVENTORY MANAGEMENT")
        print("="*60)
        print("1. View All Products")
        print("2. Add Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Import Products from CSV")
        print("7. Back to Main Menu")
        print("-"*60)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            inventory_manager.view_all_products()
        elif choice == '2':
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            try:
                price = float(input("Enter price: "))
                stock = int(input("Enter stock quantity: "))
                inventory_manager.add_product(product_id, name, price, stock)
            except ValueError:
                print("Invalid input! Price and stock must be numbers.")
        elif choice == '3':
            product_id = input("Enter product ID to update: ")
            name = input("Enter new name (press Enter to skip): ") or None
            price_input = input("Enter new price (press Enter to skip): ")
            stock_input = input("Enter new stock quantity (press Enter to skip): ")
            
            price = float(price_input) if price_input else None
            stock = int(stock_input) if stock_input else None
            
            inventory_manager.update_product(product_id, name, price, stock)
        elif choice == '4':
            product_id = input("Enter product ID to delete: ")
            inventory_manager.delete_product(product_id)
        elif choice == '5':
            keyword = input("Enter product ID or name to search: ")
            results = inventory_manager.search_product(keyword)
            if results:
                print("\nSearch Results:")
                for product in results:
                    print(product)
            else:
                print("No products found!")
        elif choice == '6':
            filename = input("Enter CSV filename to import: ")
            inventory_manager.import_products(filename)
        elif choice == '7':
            break
        else:
            print("Invalid choice! Please try again.")

def billing_menu(billing_system):
    while True:
        print("\n" + "="*60)
        print("BILLING & SALES")
        print("="*60)
        print("1. View Cart")
        print("2. Add to Cart")
        print("3. Remove from Cart")
        print("4. Apply Discount")
        print("5. Clear Discount")
        print("6. Checkout")
        print("7. Back to Main Menu")
        print("-"*60)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            billing_system.view_cart()
        elif choice == '2':
            product_id = input("Enter product ID: ")
            try:
                quantity = int(input("Enter quantity: "))
                billing_system.add_to_cart(product_id, quantity)
            except ValueError:
                print("Invalid quantity! Please enter a number.")
        elif choice == '3':
            product_id = input("Enter product ID: ")
            quantity_input = input("Enter quantity to remove (press Enter to remove all): ")
            quantity = int(quantity_input) if quantity_input else None
            billing_system.remove_from_cart(product_id, quantity)
        elif choice == '4':
            discount_type = input("Enter discount type (percentage/fixed): ").lower()
            try:
                value = float(input("Enter discount value: "))
                billing_system.apply_discount(discount_type, value)
            except ValueError:
                print("Invalid discount value! Please enter a number.")
        elif choice == '5':
            billing_system.clear_discount()
        elif choice == '6':
            sale = billing_system.checkout()
            if sale:
                print(f"\nSale completed! Final amount: ${sale.final_amount:.2f}")
                billing_system.display_bill(sale)  # Display bill in terminal instead of file
        elif choice == '7':
            break
        else:
            print("Invalid choice! Please try again.")

def reports_menu(billing_system, inventory_manager):
    while True:
        print("\n" + "="*60)
        print("REPORTS & ANALYTICS")
        print("="*60)
        print("1. Sales Report")
        print("2. Daily Sales")
        print("3. Low Stock Alert")
        print("4. Product Statistics")
        print("5. Back to Main Menu")
        print("-"*60)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            try:
                start_input = input("Enter start date (YYYY-MM-DD) or press Enter for last 7 days: ")
                end_input = input("Enter end date (YYYY-MM-DD) or press Enter for today: ")
                
                start_date = datetime.strptime(start_input, '%Y-%m-%d').date() if start_input else None
                end_date = datetime.strptime(end_input, '%Y-%m-%d').date() if end_input else None
                
                billing_system.display_sales_report(start_date, end_date)
            except ValueError:
                print("Invalid date format! Please use YYYY-MM-DD.")
        elif choice == '2':
            try:
                date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
                target_date = datetime.strptime(date_input, '%Y-%m-%d').date() if date_input else datetime.now().date()
                
                daily_sales = billing_system.get_daily_sales(target_date)
                total_amount = sum(sale.final_amount for sale in daily_sales)
                
                print(f"\nDaily Sales for {target_date}:")
                print(f"Total Transactions: {len(daily_sales)}")
                print(f"Total Revenue: ${total_amount:.2f}")
                
                if daily_sales:
                    print("\nTransactions:")
                    print("-"*40)
                    for i, sale in enumerate(daily_sales, 1):
                        print(f"{i}. {sale.datetime.strftime('%H:%M')} - ${sale.final_amount:.2f}")
            except ValueError:
                print("Invalid date format! Please use YYYY-MM-DD.")
        elif choice == '3':
            try:
                threshold = int(input("Enter low stock threshold (default 5): ") or 5)
                low_stock = billing_system.get_low_stock_products(threshold)
                
                if low_stock:
                    print(f"\nLow Stock Products (threshold: {threshold}):")
                    print("-"*50)
                    for product in low_stock:
                        print(f"{product.product_id}: {product.name} - Stock: {product.stock_quantity}")
                else:
                    print("No low stock products found!")
            except ValueError:
                print("Invalid threshold! Please enter a number.")
        elif choice == '4':
            # Product Statistics
            products = inventory_manager.products.values()
            if products:
                total_products = len(products)
                total_stock_value = sum(p.price * p.stock_quantity for p in products)
                low_stock_count = len([p for p in products if p.stock_quantity <= 5])
                
                print("\n" + "="*50)
                print("PRODUCT STATISTICS")
                print("="*50)
                print(f"Total Products: {total_products}")
                print(f"Total Stock Value: ${total_stock_value:.2f}")
                print(f"Low Stock Items: {low_stock_count}")
                print(f"Out of Stock Items: {len([p for p in products if p.stock_quantity == 0])}")
                
                # Top 5 most valuable products by stock value
                valuable_products = sorted(products, key=lambda p: p.price * p.stock_quantity, reverse=True)[:5]
                print("\nTop 5 Most Valuable Products (by stock value):")
                print("-"*50)
                for i, product in enumerate(valuable_products, 1):
                    stock_value = product.price * product.stock_quantity
                    print(f"{i}. {product.name} - ${stock_value:.2f}")
            else:
                print("No products available for statistics!")
        elif choice == '5':
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
