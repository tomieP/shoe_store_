from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Product:
    id:Optional[int] = None                       #mã sản phẩm (hệ thống sinh)
    code: Optional[str] = None                      #tên mã sản phẩm (người dùng nhập)
    name: Optional[str] = None                      #tên sản phẩm    
    description: Optional[str] = None               #mô tả sản phẩm
    brand: Optional[str] = None                     #brand sản phẩm
    price: float = 0.0                              #đơn giá 
    size: Optional[str] = None                      #size sản phẩm
    quantity: int = 0                               #số lượng tồn kho
    is_active: int = 1                              #1: con kinh doanh, 0: ngung kinh doanh
    imagePath: Optional[str] = None                 #đường đẫn ảnh
    QRPath: Optional[str] = None                    #đường dẫn mã QR
    updated_at: Optional[datetime] = None           #ngày cập nhật sản phẩm
    created_at: Optional[datetime] = None           #ngày tạo sản phẩm

    def inventory_value(self) ->float:
        """
        tính tổng giá trị tồn kho của từng sản phẩm
        """
        return self.price * self.quantity
   
    def getQuantity(self) -> str:
        """
        trả về số lượng tồn kho của sản phẩm
        """
        return f"Số lượng còn lại của sản phẩm {self.id}_{self.code}_{self.name}: {self.quantity}."
    
    def fix_discount(self,dong:float) -> float:
        '''
        Docstring for GiamGia
        Áp dụng giảm giá cho sản phẩm
        dong: số tiền giảm
        (ví dụ: dong = 5 => giam 5k trên sp)
        return giá sau khi giảm
        '''
        if 0 <= dong <= self.price:
            new_price = self.price
            new_price -= dong
        return new_price

    def to_dict(self) ->dict:
        '''        
        chuyển đổi dữ liệu sang dict
        để lưu vào db
        '''
        return{
            'maSP':self.id,
            'codeSP':self.code,
            'tenSP':self.name,
            'mota':self.description,
            'brand':self.brand,
            'donGia':self.price,
            'size':self.size,
            'soLuong':self.quantity,
            'conKinhDoanh':self.is_active,
            'imagePath':self.imagePath,
            'QRPath':self.QRPath,
            'updated_at':self.updated_at.isoformat() if self.updated_at else None,
            'created_at':self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls,data:dict) -> 'Product':
        '''
        chuyển từ dict sang class Product
        để chuyền dữ liệu từ db sang object
        '''
        return cls(
            id = data.get('id'),
            code = data.get('code'),
            name = data.get('name'),
            description = data.get('description'),
            brand = data.get('brand'),
            price = data.get('price'),
            size = data.get('size'),
            quantity = data.get('quantity'),
            is_active = data.get('is_active'),
            imagePath = data.get('imagePath'),
            QRPath = data.get('QRPath'),
            updated_at = datetime.fromisoformat(data.get('updated_at')) if data.get('updated_at') else None,
            created_at = datetime.fromisoformat(data.get('created_at')) if data.get('created_at') else None
        )