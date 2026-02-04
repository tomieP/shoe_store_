import sqlite3 
import os
from pathlib import Path
from datetime import datetime

class Database:
    def __init__(self, db_path =r'data\store.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()

        # #CUSTOMERS TABLE
        #     cursor.execute('''
        #                    CREATE TABLE IF NOT EXISTS customers(
        #                    id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                    customer_code TEXT UNIQUE NOT NULL,
        #                    name TEXT NOT NULL,
        #                    phone TEXT,
        #                    email TEXT,
        #                    total_purchases REAL DEAFAULT 0,
        #                    note TEXT,
        #                    is_active INTEGER DEFAULT 1 CHECK(is_active IN (0,1)),
        #                    point INTEGER DEFAULT 0,
        #                    created_at TEXT NOT NULL,
        #                    updated_at TEXT NOT NULL
        #                    )
        #                    ''')
        #PRODUCTS TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_code TEXT UNIQUE NOT NULL,
                        category TEXT NOT NULL,
                        brand TEXT,
                        cost_price REAL NOT NULL,
                        price REAL NOT NULL,
                        size TEXT NOT NULL,
                        color TEXT,
                        quantity INTEGER NOT NULL CHECK (quantity > 0)),
                        min_quantity INTEGER DEFAULT 5,
                        name TEXT,
                        imagePath TEXT NOT NULL,
                        QRPath TEXT NOT NULL,
                        is_active INTEGER DEFAULT 1 CHECK(is_active IN (0,1)),
                        description TEXT,                         
                        updated_at TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                           
                        UNIQUE(code, size, brand, color)
                        )
                        ''')
        #INVOICE TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoices(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_code TEXT UNIQUE NOT NULL,
                        payment_method TEXT NOT NULL CHECK(payment_method IN (cash, banking)),
                        total_amount REAL NOT NULL,
                        note TEXT,
                        created_at TEXT NOT NULL
                        updated_at TEXT NOT NULL
                        )
                        ''')
        #INVOICE DETAILS TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoice_details(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        product_code TEXT NOT NULL,
                        name TEXT NOT NULL,
                        color TEXT,
                        size TEXT NOT NULL,
                        price REAL NOT NULL,
                        quantity INTEGER NOT NULL CHECK (quantity >= 0),
                        sub_total REAL NOT NULL,
                        note TEXT,
                        FOREIGN KEY (invoice_id) REFERENCES invoices(id),
                        FOREIGN KEY (product_id) REFERENCES products(id),
                        UNIQUE(invoice_id, product_id, size, color))
                        )
                        '''
                        )
        #DAILY_REPORTS TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_reports(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        report_date TEXT NOT NULL UNIQUE,
                        total_units_sold INTEGER DEFAULT 0,
                        total_invoices INTEGER DEFAULT 0,                           
                        total_sales_amount REAL DEFAULT 0,
                        total_inventory_value REAL DEFAULT 0,
                        top_product_json TEXT,
                        note TEXT,
                        created_at TEXT NOT NULL
                        updated_at TEXT NOT NULL
                        )
                        ''')
        #IMPORT ORDERS TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS import_orders(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           import_code TEXT UNIQUE NOT NULL,
                           supplier_name TEXT,
                           status TEXT NOT NULL CHECK (status IN ("CANCELED", "WAITING", "FINISHED")),
                           note TEXT,
                           shipping_fee REAL CHECK (shipping_fee >= 0),
                           received_at TEXT NOT NULL,
                           created_at TEXT NOT NULL
                           )
                           ''')
        #IMPORT ITEMS TABLE 
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS import_items(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        
                        product_code TEXT NOT NULL,
                        product_name TEXT NOT NULL,
                        size TEXT NOT NULL,
                        color TEXT,
                        quantity INTEGER NOT NULL CHECK (quantity > 0),
                        unit_cost REAL NOT NULL CHECK (unit_cost > 0),
                        total_cost REAL NOT NULL CHECK (total_cost > 0),
                        
                        created_at TEXT NOT NULL,

                        FOREIGN KEY (import_order_id) REFERENCES import_orders(id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(id),
                    
                        UNIQUE(import_order_id, product_id, size)
                                            
                        )
                        ''')
            conn.commit()
            conn.close()
            print("Khoi tao database thanh cong!")
        except Exception as e:
            print(f"Loi khoi tao database: {e}")

    def get_connection(self):
        """Tạo và trả về kết nối đến database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn 
    
    def execute_query(self, query, params = (), fetch = True):
        '''
        Docstring for execute_query
        
        :param self: 
        :param query: ca
        :param params: tuple
        :param fetch: quyêt định có lấy kết quả hay không
            true -> tra ve toan bo ket qua (list[tuple])
            false -> tra ve id mới nhất được thêm vào
        '''
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query,params)
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid
            conn.close()
            return result

        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
        
    def backup_database(self, backup_dir = r'.\src\backups\database'):
        source_conn = None
        backup_conn = None
        try:
            Path(backup_dir).mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir,f'backup_{timestamp}.db')

            source_conn = sqlite3.connect(self.db_path)
            backup_conn = sqlite3.connect(backup_file)

            source_conn.backup(backup_conn)

            print(f"Sao luu database thanh cong tai {backup_file}")
            return backup_file
        except Exception as e:
            print(f"Loi sao luu database: {e}")
            return None
        finally:
            source_conn.close()
            backup_conn.close()

db = Database()
