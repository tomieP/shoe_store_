from dataclasses import dataclass, field
from datetime import datetime,date
from typing import Optional

from models.product import Product

@dataclass
class InvoiceDetail:
    id: Optional[int] = None                    #mã hóa đơn chi tiết
    id_invoice: Optional[int] = None            #mã hóa đơn
    id_product: Optional[int] = None            #mã sản phẩm
    tenSP: Optional[str] = None                 #tên sản phẩm
    size: Optional[int] = None                  #size sản phẩm
    donGia: float = 0.0                         #đơn giá    
    soLuong: int = 0                            #số lượng
    Tong: float = 0.0                           #thành tiền
    ghiChu: Optional[str] = None                #ghi chú

    def Tinh_Tong(self) -> float:
        '''
        thành tiền của hóa đơn chi tiết
        '''
        self.Tong = self.soLuong * self.donGia
        return self.Tong
    
    def to_dict(self) -> dict:
        '''
        chuyen InvoiceDetail sang dict
        '''
        return{
            'id': self.id,
            'id_invoice': self.id_invoice,
            'id_product': self.id_product,
            'tenSP': self.tenSP,
            'size': self.size,
            'donGia': self.donGia,
            'soLuong': self.soLuong,
            'Tong': self.Tong,
            'ghiChu': self.ghiChu
        }
    
@dataclass
class Invoice: 
    id: Optional[int] = None                    #mã hóa đơn
    ngayBan: date = None                        #ngày bán
    phuongThucThanhToan: Optional[str] = None   #phương thức thanh toán
    tongTien: float = 0.0                       #tổng tiền
    ghiChu: Optional[str] = None                #ghi chú
    giamGia: float = 0.0                        #giảm giá
    thanhTien: float = 0.0                      #thành tiền
    ngayTao: Optional[datetime] = None          #ngày tạo hóa đơn
    DSsanpham: list[InvoiceDetail] = field(default_factory = list) #danh sách hóa đơn chi tiết
    
    def Tinh_thanhTien(self) -> float:
        '''
        thành tiền của hóa đơn
        '''
        #tổng tiền của từng sản phẩm
        self.tongTien = sum(sanpham.Tinh_Tong() for sanpham in self.DSsanpham)

        #thành tiền
        self.thanhTien = self.tongTien - self.giamGia
        if self.thanhTien < 0:
            self.thanhTien = 0
        return self.thanhTien
    
    def ThemSanPham(self,sanpham:Product,soluong:int = 1):
        '''
        thêm sản phẩm vào hóa đơn
        '''
        item = InvoiceDetail(
            id_product= sanpham.id,
            tenSP= sanpham.tenSP,
            size= sanpham.size,
            donGia= sanpham.donGia,
            soLuong= soluong,
            Tong= sanpham.donGia * soluong
        )
        self.DSsanpham.append(item)
        self.Tinh_thanhTien()

    def XoaSanPham(self, x: int):
        '''
        xóa sản phẩm ra khỏi hóa đơn bằng id
        '''
        self.DSsanpham = [sanpham for sanpham in self.sanpham if sanpham.id != x]
        self.Tinh_thanhTien()

    def DemSoLuongSanPham(self) -> int:
        '''
        đếm số lượng sản phẩm có trong hóa đơn
        '''
        return sum(sanpham.soLuong for sanpham in self.DSsanpham)
    
    def GiamGiaTrenTongHoaDon(self, dong: float) -> float:
        '''
        giảm giá trên tổng hóa đơn
        '''
        if 0 <= dong <= self.tongTien:
            self.giamGia = dong
            self.thanhTien = self.thanhTien - self.giamGia
            return self.thanhTien
        return f"Giam gia khong hop le, giu nguyen hoa don la: {self.thanhTien}"

    def to_dict(self) -> dict:
        '''
        chuyen Invoice sang dict 
        '''
        return{
            'id': self.id,
            'ngayBan': self.ngayBan.isoformat() if self.ngayBan else None,
            'phuongThucThanhToan': self.phuongThucThanhToan,
            'tongTien': self.tongTien,
            'ghiChu': self.ghiChu,
            'giamGia': self.giamGia,
            'thanhTien': self.thanhTien,
            'ngayTao': self.ngayTao.isoformat() if self.ngayTao else None,
            'DSsanpham': [sanpham.to_dict() for sanpham in self.DSsanpham],
        }
    
    def to_dict_for_db(self) -> dict:
        '''
        chuyen Invoice sang dict de luu vao db
        khong bao gom DSsanpham vi DSsanpham khong co trong db cua Invoice
        '''
        return{
            'id': self.id,
            'ngayBan':self.ngayBan.isoformat() if self.ngayBan else None,
            'phuongThucThanhToan': self.phuongThucThanhToan,
            'tongTien': self.tongTien,
            'ghiChu': self.ghiChu
        }
    
@classmethod
def from_dict(cls, data:dict) -> 'Invoice':
    '''
    tao Invoice tu dict
    '''
    ngayBan = None
    if data.get(ngayBan):
        ngayBan = date.fromisoformat(data['ngayBan'])
    DSsanpham = []
    for sanpham in data.get('DSsanpham',[]):
        DSsanpham.append(InvoiceDetail(**sanpham))

    return cls(
        id = data.get('id'),
        ngayBan = ngayBan,
        phuongThucThanhToan = data.get('phuongThucThanhToan'),
        tongTien = data.get('tongTien'),
        ghiChu = data.get('ghiChu'),
        giamGia = data.get('giamGia'),
        thanhTien = data.get('thanhTien'),
        ngayTao = datetime.fromisoformat(data['ngayTao']) if data.get('ngayTao') else None,
        DSsanpham = DSsanpham
    
    )