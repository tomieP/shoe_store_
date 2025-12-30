from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional,List

@dataclass
class ImportItems:
    id: Optional[int] = None                #mã nhập kho
    id_order: Optional[int] = None          #mã đơn hàng
    id_product: Optional[int] = None        #mã sản phẩm
    name: Optional[str] = None              #tên sản phẩm
    size: Optional[int] = None              #size
    quantity: int = 0                       #số lượng nhập vào
    unit_cost: float = 0.0                  #giá gốc
    created_at: Optional[datetime] = None   #ngày tạo
    sub_total:float = 0.0                   #tổng tiền

    def calculate_total_cost(self) -> float:
        '''
        tính tổng chi phí nhập của 1 sản phẩm vào 
        '''
        self.sub_total = self.unit_cost * self.quantity
        return self.sub_total
    
    def to_dict(self) -> dict:
        '''
        chuyen ImportItems sang dict
        '''
        return{
            'id': self.id,
            'id_order': self.id_order,
            'id_product': self.id_product,
            'name': self.name,
            'size': self.size,
            'quantity': self.quantity,
            'unit_cost': self.unit_cost,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sub_total': self.sub_total
        }

@dataclass
class ImportOrder:
    id: Optional[int] = None                                    #mã đơn hàng
    supplier_name: Optional[str] = None                         #tên nhà cung cấp
    received_at: Optional[datetime] = None                      #ngày nhập hàng
    status: Optional[str] = None                                #tình trạng
    note: Optional[str] = None                                  #ghi chú
    shipping_fee: Optional[float] = 0.0                         #tiền vận chuyển
    created_at: Optional[datetime] = None                       #ngày tạo đơn nhập hàng
    items: List[ImportItems] = field(default_factory = list)    #danh sách sản phẩm đơn nhập hàng

    def calculate_total_import_expense(self) -> float:
        """
        Tính tổng chi phí đơn nhập hàng
        """
        import_expens = sum(item.calculate_total_cost for item in self.items)
        import_expens += self.shipping_fee
        return import_expens

    def add_item(self, id_product:int, quantity:int, unit_cost: float):
        """
        thêm sản phẩm vào đơn nhập hàng
        """
        item = ImportItems(
            id_product = id_product,
            quantity = quantity,
            unit_cost = unit_cost,
            sub_total= quantity * unit_cost
            )
        self.items.append(item)
        self.calculate_total_import_expense()

    def get_import_summary(self):
        """
        xem tổng số lượng sản phẩm đơn nhập hàng
        """
        #print list san pham
        count = 0
        for item in self.items:
            count+=1
            print(f"{count}   {item.id_product}_{item.name}_{item.size}       {item.quantity}       {item.unit_cost}        {item.calculate_total_cost()}")

        #print tong so luong san pham ca hoa don
        for item in self.items:
            total_amount = sum(item.quantity)
        print(total_amount)

    def to_dict(self) -> dict:
        '''
        chuyen ImportOrder sang dict
        '''
        return{
            'id': self.id,
            'supplier_name': self.supplier_name,
            'received_at': self.received_at.isoformat() if self.received_at else None,
            'tinhTrang': self.tinhTrang,
            'status':self.status,
            'shipping_fee':self.shipping_fee,
            'created_at':self.created_at.isoformat() if self.created_at else None,
            'items':[item.to_dict() for item in self.items],
            'total_unit':self.get_import_summary(),
            'total_expens':self.calculate_total_import_expense()
        }
    
@classmethod
def from_dict(cls, data:dict) -> 'ImportOrder':
    '''
    tao ImportOrder tu dict
    '''
    items = []
    for item in data.get('items',[]):
        items.append(ImportItems(**item))
    return cls(
        id = data.get('id'),
        supplier_name = data.get('supplier_name'),
        received_at = datetime.fromisoformat(data.get('received_at') if data.get('received_at') else None),
        status = data.get('WAITING',"FINISHED"),
        note = data.get('note'),
        shipping_fee = data.get('shipping_fee',0.0),
        created_at = datetime.fromisoformat(data.get('created_at') if data.get('created_at') else None),
        items = items
    )

    
