import sqlite3 
import os
from datetime import datetime

class Database:
    def __init__(self, db_path ='data/store.db'):
        self.db_path = db_path
        self.intit_database()
    
    def init_database(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

        #PRODICTS TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products(
                        maSP INTERGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        conKinhDoanh BOOLEAN NOT NULL,
                        donGia REAL NOT NULL,
                        brand TEXT,
                        imagePath TEXT NOT NULL,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        taoNgay TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        QRPath TEXT NOT NULL,
                        size INTERGER NOT NULL,
                        soluongTon INTERGER 0,
                        tenSP TEXT,
                        mota TEXT)
                        ''')
        #INVOICE TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoices(
                        maHD INTERGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        ngayBan DATE NOT NULL,
                        phuongthucThanhToan TEXT NOT NULL,
                        tongTien REAL NOT NULLL,
                        ghiChu TEXT
                        )
                        ''')
        #INVOICE DETAILS TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoice_details(
                        tenSP TEXT NOT NULL,
                        size INTERGER NOT NULL,
                        donGia REAL NOT NULL,
                        soLuong int NOT NULL,
                        thanhTien REAL NOT NULL,
                        maCTHD INTERGER PRMARY KEY AUTOINCREAMENT NOT NULL,
                        maHD INTERGER FOREIGN KEY REFERENCES invoices(maHD),
                        maSP INTERGER FOREIGN KEY REFERENCES products(maSP)
                        )
                        '''
                        )
        #DAILY_RP TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_rp(
                        maTK INTERGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        ngayTK datime NOT NULL,
                        tongDoanhThu REAL NOT NULL,
                        tongSPBan INTERGER NOT NULL,
                        tongHD NTERGER NOT NULL,
                        ghiChu TEXT     
                        taoNgay TIMESTAMP DEFAULT CURRENT_TIMESTAMP                  
                        )
                        ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS import_items(
                        maNH INTERGER PRiMARY KEY AUTOINREAMENT NOT NULL,
                        tenSP TEXT NOT NULL,
                        size INTERGER NOT NULL
                        maSP INTERGER FOREIGN KEY REFERENCES products(maSP),
                        soLuong INTERGER NOT NULL,
                        giaGoc REAL NOT NULL,
                        ngayTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP                                               
                        )
                        ''')
            conn.commit()
            conn.close()
            print("Khoi tao database thanh cong!")
        except Exception as e:
            print(f"Loi khoi tao database: {e}")
    
