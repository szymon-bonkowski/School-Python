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
            "uid": self.uid,
            "username": self.username,
            "full_name": self.full_name,
            "role": self.role
        }

    @staticmethod
    def from_dict(d):
        return User(d.get("username", ""), d.get("full_name", ""), d.get("role", "viewer"), d.get("uid"))
