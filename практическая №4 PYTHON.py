import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                role TEXT
            )
        ''')
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL
            )
        ''')
        self.conn.commit()

    def register_user(self, username, password, role):
        self.cur.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        self.conn.commit()

    def login_user(self, username, password):
        self.cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = self.cur.fetchone()
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'role': user[3]
            }
        return None

    def add_product(self, name, price):
        self.cur.execute('INSERT INTO products (name, price) VALUES (?, ?)', (name, price))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cur.execute('DELETE FROM products WHERE id = ?', (product_id,))
        self.conn.commit()

    def get_products(self):
        self.cur.execute('SELECT * FROM products')
        return self.cur.fetchall()

    def add_order(self, user_id, product_id, quantity):
        self.cur.execute('INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)', (user_id, product_id, quantity))
        self.conn.commit()

    def delete_order(self, order_id):
        self.cur.execute('DELETE FROM orders WHERE id = ?', (order_id,))
        self.conn.commit()

    def get_orders(self, user_id):
        self.cur.execute('SELECT * FROM orders WHERE user_id = ?', (user_id,))
        return self.cur.fetchall()

    def get_all_orders(self):
        self.cur.execute('SELECT * FROM orders')
        return self.cur.fetchall()
    
class User:
    def __init__(self, db):
        self.db = db

    def view_products(self):
        products = self.db.get_products()
        for product in products:
            print(f"{product[0]}. {product[1]} - {product[2]}")

    def filter_products(self):
        min_price = float(input("Введите минимальную цену: "))
        max_price = float(input("Введите максимальную цену: "))
        products = self.db.get_products()
        filtered_products = [product for product in products if min_price <= product[2] <= max_price]
        for product in filtered_products:
            print(f"{product[0]}. {product[1]} - {product[2]}")

    def add_to_order(self):
        product_id = int(input("Введите ID товара для добавления в заказ: "))
        quantity = int(input("Введите количество: "))
        self.db.add_order(self.user_id, product_id, quantity)
        print("Товар добавлен в заказ")

    def delete_order(self):
        order_id = int(input("Введите ID заказа для удаления: "))
        self.db.delete_order(order_id)
        print("Заказ удален")

    def change_data(self):
        new_username = input("Введите новое имя пользователя: ")
        self.db.cur.execute('UPDATE users SET username = ? WHERE id = ?', (new_username, self.user_id))
        self.db.conn.commit()
        print("Данные обновлены")

class Employee(User):
    def add_product(self):
        name = input("Введите название товара: ")
        price = float(input("Введите цену товара: "))
        self.db.add_product(name, price)
        print("Товар добавлен")

    def delete_product(self):
        product_id = int(input("Введите ID товара для удаления: "))
        self.db.delete_product(product_id)
        print("Товар удален")

    def edit_product(self):
        product_id = int(input("Введите ID товара для изменения: "))
        new_name = input("Введите новое название товара: ")
        new_price = float(input("Введите новую цену товара: "))
        self.db.cur.execute('UPDATE products SET name = ?, price = ? WHERE id = ?', (new_name, new_price, product_id))
        self.db.conn.commit()
        print("Товар изменен")

    def view_all_products(self):
        products = self.db.get_products()
        for product in products:
            print(f"{product[0]}. {product[1]} - {product[2]}")

class Admin(Employee):
    def view_employees(self):
        self.db.cur.execute('SELECT * FROM users WHERE role = ?', ('employee',))
        employees = self.db.cur.fetchall()
        for employee in employees:
            print(f"{employee[0]}. {employee[1]} - {employee[3]}")

    def add_employee(self):
        username = input("Введите имя нового сотрудника: ")
        password = input("Введите пароль нового сотрудника: ")
        self.db.register_user(username, password, 'employee')
        print("Сотрудник добавлен")

    def edit_employee(self):
        employee_id = int(input("Введите ID сотрудника для изменения: "))
        new_username = input("Введите новое имя сотрудника: ")
        self.db.cur.execute('UPDATE users SET username = ? WHERE id = ?', (new_username, employee_id))
        self.db.conn.commit()
        print("Данные сотрудника изменены")

    def delete_employee(self):
        employee_id = int(input("Введите ID сотрудника для удаления: "))
        self.db.cur.execute('DELETE FROM users WHERE id = ?', (employee_id,))
        self.db.conn.commit()
        print("Сотрудник удален")

def main():
    db = Database('shop.db')
    current_user = None
    while True:
        print("=============================")
        print("1. Регистрация")
        print("2. Авторизация")
        print("0. Выход")
        choice = int(input("Выберите действие: "))

        if choice == 1:
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            role = input("Введите роль (admin, employee, client): ")
            db.register_user(username, password, role)

        elif choice == 2:
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            logged_in_user = db.login_user(username, password)
            if logged_in_user:
                current_user = logged_in_user
                print(f"Добро пожаловать, {current_user['username']}!")
                break
            else:
                print("Неверные данные пользователя.")

        elif choice == 0:
            print("До свидания!")
            break

    if current_user['role'] == 'client':
        user = User(db)
        while True:
            print("=============================")
            print("1. Просмотр товаров")
            print("2. Фильтрация товаров по цене")
            print("3. Добавление товаров в заказ")
            print("4. Удаление заказов")
            print("5. Изменение данных")
            print("0. Выход")
            choice = int(input("Выберите действие: "))

            if choice == 1:
                user.view_products()

            elif choice == 2:
                user.filter_products()

            elif choice == 3:
                user.add_to_order()

            elif choice == 4:
                user.delete_order()

            elif choice == 5:
                user.change_data()

            elif choice == 0:
                print("До свидания!")
                break

    elif current_user['role'] == 'employee':
        employee = Employee(db)
        while True:
            print("=============================")
            print("1. Добавление товаров")
            print("2. Удаление товаров")
            print("3. Изменение товаров")
            print("4. Просмотр всех товаров")
            print("5. Изменение данных")
            print("0. Выход")
            choice = int(input("Выберите действие: "))

            if choice == 1:
                employee.add_product()

            elif choice == 2:
                employee.delete_product()

            elif choice == 3:
                employee.edit_product()

            elif choice == 4:
                employee.view_all_products()

            elif choice == 5:
                employee.change_data()

            elif choice == 0:
                print("До свидания!")
                break

    elif current_user['role'] == 'admin':
        admin = Admin(db)
        while True:
            print("=============================")
            print("1. Просмотр сотрудников")
            print("2. Добавление сотрудников")
            print("3. Изменение сотрудников")
            print("4. Удаление сотрудников")
            print("5. Изменение данных")
            print("0. Выход")
            choice = int(input("Выберите действие: "))

            if choice == 1:
                admin.view_employees()

            elif choice == 2:
                admin.add_employee()

            elif choice == 3:
                admin.edit_employee()

            elif choice == 4:
                admin.delete_employee()

            elif choice == 5:
                admin.change_data()

            elif choice == 0:
                print("До свидания!")
                break

if __name__ == '__main__':
    main()
