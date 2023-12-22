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

