import json
from storage import load_json, save_json
from user import User
from product import Product

class Company:
    def __init__(self, users_file="users.json", products_file="products.json", finances_file="finances.json"):
        self.users_file = users_file
        self.products_file = products_file
        self.finances_file = finances_file

        self.users = []
        self.products = []
        self.finances = {"balance": 0.0, "transactions": []}

        self.load_all()

    def load_all(self):
        users_data = load_json(self.users_file, [])
        self.users = []
        for d in users_data:
            self.users.append(User.from_dict(d))

        products_data = load_json(self.products_file, [])
        self.products = []
        for d in products_data:
            self.products.append(Product.from_dict(d))

        finances_data = load_json(self.finances_file, {"balance": 0.0, "transactions": []})
        self.finances = finances_data

    def save_all(self):
        users_list = []
        for u in self.users:
            users_list.append(u.to_dict())
        save_json(self.users_file, users_list)

        products_list = []
        for p in self.products:
            products_list.append(p.to_dict())
        save_json(self.products_file, products_list)

        save_json(self.finances_file, self.finances)

    def find_user_by_username(self, username):
        for u in self.users:
            if u.username == username:
                return u
        return None

    def add_user(self, username, full_name, role="viewer"):
        if self.find_user_by_username(username):
            return False
        new = User(username, full_name, role)
        self.users.append(new)
        self.save_all()
        return True

    def edit_user(self, username, new_full_name=None, new_role=None):
        u = self.find_user_by_username(username)
        if not u:
            return False
        if new_full_name is not None:
            u.full_name = new_full_name
        if new_role is not None:
            u.role = new_role
        self.save_all()
        return True

    def list_users(self):
        return self.users

    def add_product(self, name, price, stock):
        p = Product(name, price, stock)
        self.products.append(p)
        self.save_all()
        return p

    def find_product_by_pid(self, pid):
        for p in self.products:
            if p.pid == pid:
                return p
        return None

    def list_products(self):
        return self.products

    def sell_product(self, seller_username, pid, qty):
        seller = self.find_user_by_username(seller_username)
        if not seller:
            return False, "seller_not_found"
        if seller.role not in ("seller", "admin"):
            return False, "no_permission"
        product = self.find_product_by_pid(pid)
        if not product:
            return False, "product_not_found"
        try:
            qty = int(qty)
        except Exception:
            return False, "bad_qty"
        if qty <= 0:
            return False, "bad_qty"
        if product.stock < qty:
            return False, "not_enough_stock"

        product.stock = product.stock - qty
        amount = product.price * qty
        bal = self.finances.get("balance", 0.0)
        try:
            bal = float(bal)
        except Exception:
            bal = 0.0
        self.finances["balance"] = bal + amount
        trans = {"seller": seller_username, "pid": pid, "product_name": product.name, "qty": qty, "amount": amount}
        if "transactions" not in self.finances:
            self.finances["transactions"] = []
        self.finances["transactions"].append(trans)
        self.save_all()
        return True, "sprzedano"

    def generate_report(self, path="report.txt"):
        f = open(path, "w", encoding="utf-8")
        f.write("=== RAPORT FIRMY ===\n\n")
        f.write("Uzytkownicy:\n")
        for u in self.users:
            f.write("- " + u.username + " | " + u.full_name + " | role: " + u.role + " | id: " + u.uid + "\n")
        f.write("\nProdukty:\n")
        for p in self.products:
            f.write("- " + p.name + " | price: " + str(p.price) + " | stock: " + str(p.stock) + " | pid: " + p.pid + "\n")
        f.write("\nFinanse:\n")
        f.write("Balance: " + str(self.finances.get("balance", 0.0)) + "\n")
        f.write("Transakcje:\n")
        for t in self.finances.get("transactions", []):
            f.write("  - seller: " + t.get("seller", "") + " product: " + t.get("product_name", "") + " qty: " + str(t.get("qty", "")) + " amount: " + str(t.get("amount", "")) + "\n")
        f.close()
        return path
