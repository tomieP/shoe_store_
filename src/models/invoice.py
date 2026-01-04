from dataclasses import dataclass, field
from datetime import datetime,date
from typing import Optional

from models.product import Product

@dataclass
class InvoiceDetail:
    id: Optional[int] = None                    #mã hóa đơn chi tiết
    id_invoice: Optional[int] = None            #mã hóa đơn
    id_product: Optional[int] = None            #mã sản phẩm
    name: Optional[str] = None                  #tên sản phẩm
    size: Optional[int] = None                  #size sản phẩm
    price: float = 0.0                          #đơn giá    
    quantity: int = 0                           #số lượng
    sub_total: float = 0.0                      #tổng giá tiền của 1 sản phẩm
    note: Optional[str] = None                  #ghi chú

    def calsubTotal(self) -> float:
        """
        tính tiền cho hóa đơn chi tiết
        """
        self.sub_total = self.quantity * self.price
        return self.sub_total
    
    def to_dict(self) -> dict:
        """
        chuyển InvoiceDetail sang dict
        """
        return{
            'id': self.id,
            'id_invoice': self.id_invoice,
            'id_product': self.id_product,
            'name': self.name,
            'size': self.size,
            'price': self.price,
            'quantity': self.quantity,
            'sub_total': self.sub_total,
            'note': self.note
        }
    
@dataclass
class Invoice: 
    id: Optional[int] = None                    #mã hóa đơn
    method: Optional[str] = None                #phương thức thanh toán
    total_amount: float = 0.0                   #tổng tiền
    sub_total: float = 0.0                      #tổng phụ
    note: Optional[str] = None                  #ghi chú
    created_at: Optional[datetime] = None       #ngày tạo hóa đơn
    items: list[InvoiceDetail] = field(default_factory = list) #danh sách hóa đơn chi tiết
    
    def calculate_total_amount(self) -> float:
        """
        tính tổng tiền của 1 hóa đơn dựa trên subtotal của từng sản phẩm
        """
        #tổng phụ = tổng tiền của từng sản phẩm
        self.total_amount = self.sub_total = sum(item.calsubTotal() for item in self.items)
        return self.total_amount
    
    def add_item(self, product: Product, quantity: int = 1):
        """
        thêm 1 sản phẩm vào hóa đơn
        """
        item = InvoiceDetail(
            id_product= product.id,
            name= product.name,
            size= product.size,
            price= product.price,
            quantity= quantity,
            sub_total= product.price * quantity
        )
        self.items.append(item)
        self.calculate_total_amount()

    def delete_item(self, x: int):
        """
        xóa 1 sản phẩm ra khỏi hóa đơn
        """
        self.items = [item for item in self.items if item.id != x]
        self.calculate_total_amount()

    def count_items(self) -> int:
        """
        đếm số lượng của sản phẩm có trong hóa đơn
        """
        return sum(item.quantity for item in self.items)
    
    def apply_fixed_discount(self, dong: float) -> float:
        """
        giảm giá trên tổng hóa đơn
            nếu số tiền giảm giá lớn hơn tổng tiền hóa đơn hoặc âm thì sẽ = 0
        """
        if 0.0 <= dong <= self.total_amount:
            self.total_amount -= dong
            return self.total_amount
        return 0.0

    def to_dict(self) -> dict:
        """
        chuyển Invoice sang dict 
        """
        return{
            'id': self.id,
            'method': self.method,
            'total_amount': self.total_amount,
            'note': self.note,
            'sub_total': self.sub_total,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.to_dict() for item in self.items],
        }
    
    def to_dict_for_db(self) -> dict:
        """
        chuyen Invoice sang dict de luu vao db,
        khong bao gom items vi items khong co trong db cua Invoice
        """
        return{
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'method': self.method,
            'total_amount': self.total_amount,
            'note': self.note
        }
    
@classmethod
def from_dict(cls, data:dict) -> 'Invoice':
    """
    tao Invoice tu dict
    """   
    items = []
    for item in data.get('items',[]):
        items.append(InvoiceDetail(**item))

    return cls(
        id = data.get('id'),
        method = data.get('method'),
        total_amount = data.get('total_amount'),
        note = data.get('note'),
        sub_total = data.get('sub_total'),
        created_at = datetime.fromisoformat(data.get('created_at')) if data.get('created_at') else None,
        items = items
    
    )