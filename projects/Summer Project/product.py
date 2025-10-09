import uuid

class Product:
    def __init__(self, name, price, stock, pid=None):
        if pid:
            self.pid = pid
        else:
            self.pid = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            "pid": self.pid,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

    @staticmethod
    def from_dict(d):
        name = d.get("name", "")
        price = d.get("price", 0)
        stock = d.get("stock", 0)
        pid = d.get("pid")
        try:
            price = float(price)
        except Exception:
            price = 0.0
        try:
            stock = int(stock)
        except Exception:
            stock = 0
        return Product(name, price, stock, pid)
