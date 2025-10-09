import uuid

class User:
    def __init__(self, username, full_name, role="viewer", uid=None):
        if uid:
            self.uid = uid
        else:
            self.uid = str(uuid.uuid4())
        self.username = username
        self.full_name = full_name
        self.role = role

    def to_dict(self):
        return {
            "class": self.__class__.__name__,
            "uid": self.uid,
            "username": self.username,
            "full_name": self.full_name,
            "role": self.role
        }

    @staticmethod
    def from_dict(d):
        cls = d.get("class", "User")
        username = d.get("username", "")
        full_name = d.get("full_name", "")
        role = d.get("role", "viewer")
        uid = d.get("uid")
        if cls == "Admin":
            return Admin(username, full_name, role, uid)
        elif cls == "Seller":
            return Seller(username, full_name, role, uid)
        else:
            return User(username, full_name, role, uid)

class Employee(User):
    pass

class Admin(Employee):
    pass

class Seller(Employee):
    pass
