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
                        maSP INTEGER PRIMARY KEY AUTOINCREMENT, --he thong sinh ma san pham
                        codeSP TEXT UNIQUE NOT NULL, --nguoi dung tu nhap
                        tenSP TEXT,
                        mota TEXT,
                        brand TEXT,
                           
                        donGia REAL NOT NULL,
                        size TEXT NOT NULL,
                        soLuong INTEGER DEFAULT 0 CHECK (soLuong >= 0),
                        
                        conKinhDoanh INTEGER NOT NULL CHECK(conKinhDoanh IN (0,1)), --1: con kinh doanh 0: ngung kinh doanh
                        imagePath TEXT NOT NULL,
                        QRPath TEXT NOT NULL,
                           
                        ngayCapNhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ngayTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                        ''')
        #INVOICE TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoices(
                        maHD INTEGER PRIMARY KEY AUTOINCREMENT,
                        ngayBan TEXT NOT NULL,
                        phuongthucThanhToan TEXT NOT NULL,
                        tongTien REAL NOT NULL,
                        ghiChu TEXT
                        )
                        ''')
        #INVOICE DETAILS TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoice_details(
                        maCTHD INTEGER PRIMARY KEY AUTOINCREMENT,
                        maHD INTEGER NOT NULL,
                        maSP INTEGER NOT NULL,
                           
                        tenSP TEXT NOT NULL,
                        size TEXT NOT NULL,
                        donGia REAL NOT NULL,
                        soLuong INTEGER NOT NULL CHECK (soLuong >= 0),
                        thanhTien REAL NOT NULL CHECK (thanhTien = donGia * soLuong),
                        ghiChu TEXT,
                        FOREIGN KEY (maHD) REFERENCES invoices(maHD),
                        FOREIGN KEY (maSP) REFERENCES products(maSP)
                        )
                        '''
                        )
        #DAILY_RP TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_rp(
                        maTK INTEGER PRIMARY KEY AUTOINCREMENT,
                        ngayTK TEXT NOT NULL,
                        tongDoanhThu REAL NOT NULL CHECK (tongDoanhThu >= 0),
                        tongSPBan INTEGER NOT NULL  CHECK (tongSPBan >= 0),
                        tongHD INTEGER NOT NULL  CHECK (tongHD >= 0),
                        ghiChu TEXT,
                        ngayTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  

                        UNIQUE(ngayTK)
                        )
                        ''')
        #IMPORT ORDER
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS import_order(
                           maDH INTEGER PRIMARY KEY AUTOINCREMENT,
                           tenNhaCungCap TEXT,
                           ngayNhapHang TEXT NOT NULL,
                           tinhTrang TEXT NOT NULL CHECK (tinhTrang IN ("DANG CHO", "HOAN THANH")),--"DANG CHO" "HOAN THANH"
                           ghiChu TEXT,
                           tienVanChuyen REAL NOT NULL CHECK (tienVanChuyen >= 0),
                           ngayTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           )
                           ''')
        #IMPORT ITEMS TABLE 
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS import_items(
                        maNH INTEGER PRIMARY KEY AUTOINCREMENT,
                        maDH INTEGER NOT NULL,
                        maSP INTEGER NOT NULL,
                           
                        tenSP TEXT NOT NULL,
                        size TEXT NOT NULL,
                        soLuong INTEGER NOT NULL CHECK (soLuong > 0),
                        giaGoc REAL NOT NULL CHECK (giaGoc > 0),
                        
                        ngayTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                        FOREIGN KEY (maSP) REFERENCES products(maSP),
                        FOREIGN KEY (maDH) REFERENCES import_order(maDH)
                                            
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
        :param query: 
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
