import sqlite3 
import os
from datetime import datetime

class Database:
    def __init__(self, db_path ='data/store.db'):
        self.db_path = db_path
        self.intit_database()
    
    def init_database(self):
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
                       ngayCapNhat datetime NOT NULL,
                       ngayTao datetime NOT NULL,
                       QRPath TEXT NOT NULL,
                       size INTERGER NOT NULL,
                       soluongTon INTERGER NOT NULL,
                       tenSP TEXT,
                       mota TEXT)
                       ''')
    #INVOICE TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices(
                       maHD INTERGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       ngayBan datetime NOT NULL,
                       phuongthucThanhToan TEXT NOT NULL,
                       tongTien REAL NOT NULLL
                       ghiChu TEXT
                       )
                       ''')
    #INVOICE DETAILS TABLE


    
