import os
import csv
from datetime import datetime

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
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['product_id'], data['name'], data['price'], data['stock_quantity'])

class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.total = product.price * quantity

class Sale:
    def __init__(self, items, total_amount, datetime):
        self.items = items
        self.total_amount = total_amount
        self.datetime = datetime

class InventoryManager:
    def __init__(self, data_file='inventory.csv'):
        self.data_file = data_file
        self.products = self.load_data()
    
    def load_data(self):
        products = {}
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        product = Product(
                            row['product_id'],
                            row['name'],
                            float(row['price']),
                            int(row['stock_quantity'])
                        )
                        products[product.product_id] = product
            except Exception as e:
                print(f"Error loading inventory data: {e}")
        return products
    
    def save_data(self):
        try:
            with open(self.data_file, 'w', newline='') as file:
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
            product.price = price
        if stock_quantity is not None:
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
                keyword == product.product_id):
                results.append(product)
        return results
    
    def get_product(self, product_id):
        return self.products.get(product_id)
    
    def view_all_products(self):
        if not self.products:
            print("No products available!")
            return
        
        print("\n=== All Products ===")
        print(f"{'ID':<10} {'Name':<20} {'Price':<10} {'Stock':<10}")
        print("-" * 50)
        for product in self.products.values():
            print(f"{product.product_id:<10} {product.name:<20} ${product.price:<9.2f} {product.stock_quantity:<10}")

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
                with open(self.sales_file, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Parse items from the sales file
                        items = []
                        # This is a simplified approach - in a real system, you'd need a more robust way
                        # to store and retrieve the items in each sale
                        sale = Sale(items, float(row['total_amount']), datetime.fromisoformat(row['datetime']))
                        sales.append(sale)
            except Exception as e:
                print(f"Error loading sales data: {e}")
        return sales
    
    def save_sales(self):
        try:
            with open(self.sales_file, 'w', newline='') as file:
                fieldnames = ['datetime', 'total_amount']  # Simplified for this example
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for sale in self.sales:
                    writer.writerow({
                        'datetime': sale.datetime.isoformat(),
                        'total_amount': sale.total_amount
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
        
        print("\n=== Shopping Cart ===")
        total = 0
        for i, item in enumerate(self.cart, 1):
            print(f"{i}. {item.product.name} - {item.quantity} x ${item.product.price:.2f} = ${item.total:.2f}")
            total += item.total
        
        print(f"\nTotal: ${total:.2f}")
    
    def checkout(self):
        if not self.cart:
            print("Cart is empty!")
            return None
        
        # Calculate total
        total = sum(item.total for item in self.cart)
        
        # Create sale record
        sale = Sale(self.cart.copy(), total, datetime.now())
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
        
        if file_format == 'txt':
            with open(filename, 'w') as file:
                file.write("=== BILL ===\n")
                file.write(f"Date: {sale.datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("Items:\n")
                for item in sale.items:
                    file.write(f"{item.product.name} - {item.quantity} x ${item.product.price:.2f} = ${item.total:.2f}\n")
                file.write(f"Total: ${sale.total_amount:.2f}\n")
        else:  # CSV
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Product', 'Quantity', 'Unit Price', 'Total'])
                for item in sale.items:
                    writer.writerow([item.product.name, item.quantity, f"${item.product.price:.2f}", f"${item.total:.2f}"])
                writer.writerow([])
                writer.writerow(['Grand Total', '', '', f"${sale.total_amount:.2f}"])
        
        print(f"Bill saved as {filename}")
        return True
    
    def get_daily_sales(self, date=None):
        if date is None:
            date = datetime.now().date()
        
        daily_sales = []
        for sale in self.sales:
            if sale.datetime.date() == date:
                daily_sales.append(sale)
        
        return daily_sales
    
    def get_low_stock_products(self, threshold=5):
        low_stock = []
        for product in self.inventory_manager.products.values():
            if product.stock_quantity <= threshold:
                low_stock.append(product)
        return low_stock

def main():
    inventory_manager = InventoryManager()
    billing_system = BillingSystem(inventory_manager)
    
    while True:
        print("\n=== Inventory Management & Billing System ===")
        print("1. Product Management")
        print("2. Billing")
        print("3. Reports")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            product_management_menu(inventory_manager)
        elif choice == '2':
            billing_menu(billing_system)
        elif choice == '3':
            reports_menu(billing_system, inventory_manager)
        elif choice == '4':
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice! Please try again.")

def product_management_menu(inventory_manager):
    while True:
        print("\n=== Product Management ===")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Search Product")
        print("5. View All Products")
        print("6. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            product_id = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            try:
                price = float(input("Enter Price: "))
                stock_quantity = int(input("Enter Stock Quantity: "))
                inventory_manager.add_product(product_id, name, price, stock_quantity)
            except ValueError:
                print("Invalid input! Price must be a number and stock quantity must be an integer.")
        
        elif choice == '2':
            product_id = input("Enter Product ID to update: ")
            if product_id not in inventory_manager.products:
                print("Product not found!")
                continue
                
            current = inventory_manager.products[product_id]
            print(f"Current: Name={current.name}, Price=${current.price}, Stock={current.stock_quantity}")
            
            name = input("Enter new Name (leave blank to keep current): ")
            price_str = input("Enter new Price (leave blank to keep current): ")
            stock_str = input("Enter new Stock Quantity (leave blank to keep current): ")
            
            price = float(price_str) if price_str else None
            stock_quantity = int(stock_str) if stock_str else None
            name = name if name else None
            
            inventory_manager.update_product(product_id, name, price, stock_quantity)
        
        elif choice == '3':
            product_id = input("Enter Product ID to delete: ")
            inventory_manager.delete_product(product_id)
        
        elif choice == '4':
            keyword = input("Enter Product ID or Name to search: ")
            results = inventory_manager.search_product(keyword)
            if results:
                print("\nSearch Results:")
                print(f"{'ID':<10} {'Name':<20} {'Price':<10} {'Stock':<10}")
                print("-" * 50)
                for product in results:
                    print(f"{product.product_id:<10} {product.name:<20} ${product.price:<9.2f} {product.stock_quantity:<10}")
            else:
                print("No products found!")
        
        elif choice == '5':
            inventory_manager.view_all_products()
        
        elif choice == '6':
            break
        
        else:
            print("Invalid choice! Please try again.")

def billing_menu(billing_system):
    while True:
        print("\n=== Billing ===")
        print("1. Add to Cart")
        print("2. Remove from Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            billing_system.inventory_manager.view_all_products()
            product_id = input("Enter Product ID: ")
            try:
                quantity = int(input("Enter Quantity: "))
                billing_system.add_to_cart(product_id, quantity)
            except ValueError:
                print("Quantity must be an integer!")
        
        elif choice == '2':
            if not billing_system.cart:
                print("Cart is empty!")
                continue
                
            billing_system.view_cart()
            product_id = input("Enter Product ID: ")
            quantity_str = input("Enter Quantity to remove (leave blank to remove all): ")
            quantity = int(quantity_str) if quantity_str else None
            billing_system.remove_from_cart(product_id, quantity)
        
        elif choice == '3':
            billing_system.view_cart()
        
        elif choice == '4':
            sale = billing_system.checkout()
            if sale:
                save_bill = input("Do you want to save the bill? (y/n): ")
                if save_bill.lower() == 'y':
                    format_choice = input("Enter format (txt/csv): ")
                    billing_system.generate_bill(sale, format_choice.lower())
        
        elif choice == '5':
            break
        
        else:
            print("Invalid choice! Please try again.")

def reports_menu(billing_system, inventory_manager):
    while True:
        print("\n=== Reports ===")
        print("1. Daily Sales Report")
        print("2. Low Stock Report")
        print("3. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            try:
                if date_str:
                    date = datetime.strptime(date_str, '%Y-%m-%d').date()
                else:
                    date = datetime.now().date()
                
                daily_sales = billing_system.get_daily_sales(date)
                total_sales = sum(sale.total_amount for sale in daily_sales)
                
                print(f"\nSales Report for {date}:")
                print(f"Number of transactions: {len(daily_sales)}")
                print(f"Total sales: ${total_sales:.2f}")
                
                if daily_sales:
                    print("\nTransactions:")
                    for i, sale in enumerate(daily_sales, 1):
                        print(f"{i}. {sale.datetime.strftime('%H:%M:%S')} - ${sale.total_amount:.2f}")
            
            except ValueError:
                print("Invalid date format! Please use YYYY-MM-DD.")
        
        elif choice == '2':
            threshold_str = input("Enter low stock threshold (default 5): ")
            threshold = int(threshold_str) if threshold_str else 5
            
            low_stock = billing_system.get_low_stock_products(threshold)
            
            if low_stock:
                print(f"\nLow Stock Products (threshold: {threshold}):")
                print(f"{'ID':<10} {'Name':<20} {'Stock':<10}")
                print("-" * 40)
                for product in low_stock:
                    print(f"{product.product_id:<10} {product.name:<20} {product.stock_quantity:<10}")
            else:
                print("No low stock products!")
        
        elif choice == '3':
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()