from database import db
print("thu nghiem db")
import os
if os.path.exists('data/store.db'):
    print("db ton tai")
else:
    print("khong tim thay db")