from company import Company

def ensure_defaults(company):
    if not company.users:
        company.add_user("admin", "Administrator", "admin")
        company.add_user("seller1", "Pracownik Jeden", "seller")
        company.add_user("seller2", "Pracownik Dwa", "seller")
    if not company.products:
        company.add_product("produkt_a", 10.0, 20)
        company.add_product("produkt_b", 25.5, 10)
        company.add_product("produkt_c", 5.75, 50)
    if company.finances.get("balance", None) is None:
        company.finances = {"balance": 0.0, "transactions": []}
        company.save_all()

def login_prompt(company):
    print("=== PROSTY SYSTEM FIRMOWY ===")
    print("Dostepne konta:")
    for u in company.list_users():
        print("- " + u.username + " (" + u.role + ")")
    username = input("podaj username by zalogowac: ").strip()
    user = company.find_user_by_username(username)
    if not user:
        print("brak takiego konta")
        return None
    print("witaj " + user.full_name + " (role: " + user.role + ")")
    return user

def admin_menu(company, user):
    while True:
        print("\n--- MENU ADMIN ---")
        print("1. lista uzytkownikow")
        print("2. edytuj uzytkownika")
        print("3. dodaj uzytkownika")
        print("4. lista produktow")
        print("5. dodaj produkt")
        print("6. pokaz finanse")
        print("7. dodaj srodki (finanse)")
        print("8. generuj raport")
        print("9. wyloguj")
        ch = input("wybor: ").strip()
        if ch == "1":
            for u in company.list_users():
                print(u.username + " | " + u.full_name + " | role: " + u.role)
        elif ch == "2":
            uname = input("username do edycji: ").strip()
            newname = input("nowe imie (enter by pominac): ").strip()
            newrole = input("nowa rola (admin/seller/viewer) (enter by pominac): ").strip()
            if newname == "":
                newname = None
            if newrole == "":
                newrole = None
            ok = company.edit_user(uname, new_full_name=newname, new_role=newrole)
            if ok:
                print("ok")
            else:
                print("nie znaleziono uzytkownika")
        elif ch == "3":
            uname = input("username: ").strip()
            fname = input("full name: ").strip()
            role = input("role (admin/seller/viewer): ").strip()
            if role == "":
                role = "viewer"
            ok = company.add_user(uname, fname, role)
            print("dodano" if ok else "istnieje juz")
        elif ch == "4":
            for p in company.list_products():
                print(p.pid + " | " + p.name + " | price: " + str(p.price) + " | stock: " + str(p.stock))
        elif ch == "5":
            name = input("nazwa produktu: ").strip()
            price = input("cena: ").strip()
            stock = input("stock: ").strip()
            try:
                price = float(price)
            except Exception:
                price = 0.0
            try:
                stock = int(stock)
            except Exception:
                stock = 0
            p = company.add_product(name, price, stock)
            print("dodano:", p.to_dict())
        elif ch == "6":
            print("balance:", company.finances.get("balance", 0.0))
            print("transactions:", company.finances.get("transactions", []))
        elif ch == "7":
            added = input("ile dolaczyc do bilansu: ").strip()
            try:
                added = float(added)
            except Exception:
                added = 0.0
            company.finances["balance"] = float(company.finances.get("balance", 0.0)) + added
            if "transactions" not in company.finances:
                company.finances["transactions"] = []
            company.finances["transactions"].append({"type": "manual_add", "amount": added, "by": user.username})
            company.save_all()
            print("dodano srodki")
        elif ch == "8":
            path = company.generate_report()
            print("raport zapisany:", path)
        elif ch == "9":
            break
        else:
            print("nieznana opcja")

def seller_menu(company, user):
    while True:
        print("\n--- MENU SELLER ---")
        print("1. lista produktow")
        print("2. sprzedaj produkt")
        print("3. pokaz bilans")
        print("4. wyloguj")
        ch = input("wybor: ").strip()
        if ch == "1":
            for p in company.list_products():
                print(p.pid + " | " + p.name + " | price: " + str(p.price) + " | stock: " + str(p.stock))
        elif ch == "2":
            pid = input("pid produktu: ").strip()
            qty = input("ilosc: ").strip()
            try:
                qty = int(qty)
            except Exception:
                qty = 0
            ok, msg = company.sell_product(user.username, pid, qty)
            if ok:
                print("OK:", msg)
            else:
                print("BLAD:", msg)
        elif ch == "3":
            print("balance:", company.finances.get("balance", 0.0))
        elif ch == "4":
            break
        else:
            print("nieznana opcja")

def viewer_menu(company, user):
    while True:
        print("\n--- MENU VIEWER ---")
        print("1. lista produktow")
        print("2. wyloguj")
        ch = input("wybor: ").strip()
        if ch == "1":
            for p in company.list_products():
                print(p.pid + " | " + p.name + " | price: " + str(p.price) + " | stock: " + str(p.stock))
        elif ch == "2":
            break
        else:
            print("nieznana opcja")

def main():
    company = Company()
    ensure_defaults(company)
    while True:
        user = login_prompt(company)
        if not user:
            cont = input("sprobuj ponownie? (t/n): ").strip().lower()
            if cont != "t":
                break
            else:
                continue
        if user.role == "admin":
            admin_menu(company, user)
        elif user.role == "seller":
            seller_menu(company, user)
        else:
            viewer_menu(company, user)
        again = input("chcesz sie zalogowac jako inny uzytkownik? (t/n): ").strip().lower()
        if again != "t":
            print("koniec programu")
            break

if __name__ == "__main__":
    main()
