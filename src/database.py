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

        #PRODUCTS TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        code TEXT UNIQUE NOT NULL,
                        name TEXT,
                        description TEXT,
                        brand TEXT,
                           
                        price REAL NOT NULL,
                        size TEXT NOT NULL,
                        quantity INTEGER DEFAULT 0 CHECK (quantity >= 0),
                        
                        is_active INTEGER NOT NULL CHECK(is_active IN (0,1)),
                        imagePath TEXT NOT NULL,
                        QRPath TEXT NOT NULL,
                           
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                        ''')
        #INVOICE TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoices(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        method TEXT NOT NULL,
                        total REAL NOT NULL,
                        note TEXT
                        )
                        ''')
        #INVOICE DETAILS TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoice_details(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_invoice INTEGER NOT NULL,
                        id_product INTEGER NOT NULL,
                           
                        product_name TEXT NOT NULL,
                        size TEXT NOT NULL,
                        price REAL NOT NULL,
                        quantity INTEGER NOT NULL CHECK (quantity >= 0),
                        subTotal REAL NOT NULL,
                        note TEXT,
                        FOREIGN KEY (id_invoice) REFERENCES invoices(id),
                        FOREIGN KEY (id_product) REFERENCES products(id)
                        )
                        '''
                        )
        #DAILY_RP TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_rp(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        dailyRevenue REAL NOT NULL CHECK (dailyRevenue >= 0),
                        total_units_sold INTEGER NOT NULL  CHECK (total_units_sold >= 0),
                        invoice_total INTEGER NOT NULL  CHECK (invoice_total >= 0),
                        note TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                        ''')
        #IMPORT ORDER
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS import_order(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           supplier_name TEXT,
                           received_at TEXT NOT NULL,
                           status TEXT NOT NULL CHECK (status IN ("WAITING", "FINISHED")),
                           note TEXT,
                           shipping_fee REAL NOT NULL CHECK (shipping_fee >= 0),
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           )
                           ''')
        #IMPORT ITEMS TABLE 
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS import_items(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_order INTEGER NOT NULL,
                        id_product INTEGER NOT NULL,
                           
                        name TEXT NOT NULL,
                        size TEXT NOT NULL,
                        quantity INTEGER NOT NULL CHECK (quantity > 0),
                        unit_cost REAL NOT NULL CHECK (unit_cost > 0),
                        
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                        FOREIGN KEY (id_product) REFERENCES products(id),
                        FOREIGN KEY (id_order) REFERENCES import_order(id)
                                            
                        )
                        ''')
            conn.commit()
            conn.close()
            print("Khoi tao database thanh cong!")
        except Exception as e:
            print(f"Loi khoi tao database: {e}")

    def get_connection(self):
        """Tạo và trả về kết nối đến database"""
        return sqlite3.connect(self.db_path)
    
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
        
    def backup_database(self, backup_dir = './src/backups'):
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
