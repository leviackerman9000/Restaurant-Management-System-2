from abc import ABC

class User(ABC):
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address


class Customer(User):
    def __init__(self, name, email, address):
        super().__init__(name, email, address)
        self.balance = 0
        self.past_orders = []

    def view_menu(self, restaurant):
        restaurant.show_menu()

    def place_order(self, restaurant, item_name, quantity):
        item = restaurant.find_menu_item(item_name)
        if item:
            total_cost = item['price'] * quantity
            if total_cost > self.balance:
                print("Not enough balance. Please add funds.")
            elif quantity > item['quantity']:
                print("That much quantity is not in stock.")
            else:
                self.balance -= total_cost
                item['quantity'] -= quantity
                self.past_orders.append((item_name, quantity, total_cost))
                print(f"Order placed for {item_name}, portion- {quantity}. Total cost: {total_cost}")
        else:
            print("Invalid Item.")

    def check_balance(self):
        print(f"Available balance: {self.balance}")

    def add_funds(self, amount):
        self.balance += amount
        print(f"Added {amount}. New balance: {self.balance}")

    def view_past_orders(self):
        print("Past Orders:")
        for order in self.past_orders:
            print(f"Item: {order[0]}, Quantity: {order[1]}, Cost: {order[2]}")


class Admin(User):
    def __init__(self, name, email, address):
        super().__init__(name, email, address)

    def add_menu_item(self, restaurant, item_name, price, quantity):
        restaurant.add_menu_item(item_name, price, quantity)

    def remove_menu_item(self, restaurant, item_name):
        restaurant.remove_menu_item(item_name)

    def update_menu_item(self, restaurant, item_name, new_price, new_quantity):
        self.new_price = None
        self.new_quantity = None
        restaurant.update_menu_item(item_name, new_price, new_quantity)

    def add_customer(self, restaurant, name, email, address):
        restaurant.add_customer(name, email, address)

    def remove_customer(self, restaurant, email):
        restaurant.remove_customer(email)

    def view_customers(self, restaurant):
        restaurant.view_customers()

    def view_menu(self, restaurant):
        restaurant.show_menu()


class Restaurant:
    def __init__(self, name):
        self.name = name
        self.menu = []
        self.customers = []

    def add_menu_item(self, item_name, price, quantity):
        self.menu.append({'name': item_name, 'price': price, 'quantity': quantity})
        print(f"Added {item_name} to menu.")

    def remove_menu_item(self, item_name):
        for item in self.menu:
            if item['name'].lower() == item_name.lower():
                self.menu.remove(item)
                print(f"Removed {item_name} from menu.")
                return
        print("Item to remove is not available in the menu.")

    def update_menu_item(self, item_name, new_price, new_quantity):
        self.new_price = None
        self.new_quantity = None
        for item in self.menu:
            if item['name'].lower() == item_name.lower():
                if new_price is not None:
                    item['price'] = new_price
                if new_quantity is not None:
                    item['quantity'] = new_quantity
                print(f"Updated {item_name} in menu.")
                return
        print("Item to update is not available in the menu.")

    def show_menu(self):
        print("   ****MENU****")
        print("Name\tPrice\tQuantity")
        for item in self.menu:
            print(f"{item['name']}\t{item['price']}\t{item['quantity']}")

    def find_menu_item(self, item_name):
        for item in self.menu:
            if item['name'].lower() == item_name.lower():
                return item
        return None

    def add_customer(self, name, email, address):
        self.customers.append(Customer(name, email, address))
        print(f"Registered customer: {name}")

    def remove_customer(self, email):
        for customer in self.customers:
            if customer.email.lower() == email.lower():
                self.customers.remove(customer)
                print(f"Removed customer: {customer.name}")
                return
        print("Customer not found.")

    def view_customers(self):
        print("****Customers****")
        for customer in self.customers:
            print(f"Name: {customer.name}, Email: {customer.email}, Address: {customer.address}")



restaurant = Restaurant("KHANA PINA")
admin = Admin("Administrator", "admin@yahoo.com", "Shahi Eidgah")

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Add Menu Item")
        print("2. Remove Menu Item")
        print("3. Update Menu Item")
        print("4. Add Customer")
        print("5. Remove Customer")
        print("6. View Customers")
        print("7. View Menu")
        print("8. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            item_name = input("Enter food item name: ")
            price = int(input("Enter the price: "))
            quantity = int(input("Enter quantity: "))
            admin.add_menu_item(restaurant, item_name, price, quantity)
        elif choice == 2:
            item_name = input("Enter food item to remove: ")
            admin.remove_menu_item(restaurant, item_name)
        elif choice == 3:
            item_name = input("Enter food item to update: ")
            new_price = int(input("Enter new price: "))
            new_quantity = int(input("Enter new quantity: "))
            admin.update_menu_item(restaurant, item_name, new_price, new_quantity) 
        elif choice == 4:
            name = input("Enter customer name: ")
            email = input("Enter customer email: ")
            address = input("Enter customer address: ")
            admin.add_customer(restaurant, name, email, address)
        elif choice == 5:
            email = input("Enter email of the customer that you want to remove: ")
            admin.remove_customer(restaurant, email)
        elif choice == 6:
            admin.view_customers(restaurant)
        elif choice == 7:
            admin.view_menu(restaurant)
        elif choice == 8:
            break
        else:
            print("Invalid option! Try again.")


def customer_menu():
    if not restaurant.customers:
        print("No customers available. Admin needs to add customers.")
    else:
        print("Select Customer:")
        for i in range(len(restaurant.customers)):
            customer = restaurant.customers[i]
            print(f"{i+1}.{customer.name}")
    
        customer_choice = int(input("Enter customer number: "))
        if customer_choice >= 1 and customer_choice <= len(restaurant.customers):
            customer = restaurant.customers[customer_choice - 1]

            while True:
                print("\nCustomer Menu:")
                print("1. View Menu")
                print("2. Place Order")
                print("3. Check Balance")
                print("4. Add Funds")
                print("5. View Past Orders")
                print("6. Exit")
                
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    customer.view_menu(restaurant)
                elif choice == 2:
                    item_name = input("Enter food item: ")
                    quantity = int(input("Enter quantity: "))
                    customer.place_order(restaurant, item_name, quantity)
                elif choice == 3:
                    customer.check_balance()
                elif choice == 4:
                    amount = int(input("Enter amount to add to balance: "))
                    customer.add_funds(amount)
                elif choice == 5:
                    customer.view_past_orders()
                elif choice == 6:
                    break
                else:
                    print("Invalid option! Try again.")
        else:
            print("Invalid customer number, try again")


while True:
    print("WELCOME TO OUR RESTAURANT")
    print("1. Customer")
    print("2. Admin")
    print("3. Exit")
    
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        customer_menu()
    elif choice == 2:
        admin_menu()
    elif choice == 3:
        break
    else:
        print("Invalid option! Try again.")
        
        
        
