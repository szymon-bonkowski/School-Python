import json

def load_json(path, default):
    try:
        f = open(path, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        return data
    except FileNotFoundError:
        return default
    except Exception:
        return default

def save_json(path, data):
    f = open(path, "w", encoding="utf-8")
    json.dump(data, f, indent=4)
    f.close()
