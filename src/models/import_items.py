from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional,List

@dataclass
class ImportItems:
    id: Optional[int] = None            #mã nhập kho
    id_order: Optional[int] = None      #mã đơn hàng
    id_product: Optional[int] = None    #mã sản phẩm
    tenSP: Optional[str] = None         #tên sản phẩm
    size: Optional[int] = None          #size
    soLuong: int = 0                    #số lượng
    giaGoc: float = 0.0                 #giá gốc
    ngayTao: Optional[datetime] = None  #ngày tạo
    tongTien:float = 0.0                #tổng tiền

    def Tinh_tongTien(self) -> float:
        '''
        tính tổng tiền nhập kho cho 1 sản phẩm
        '''
        self.tongTien = self.giaGoc * self.soLuong
        return self.tongTien
    
    def to_dict(self) -> dict:
        '''
        chuyen ImportItems sang dict
        '''
        return{
            'id': self.id,
            'id_order': self.id_order,
            'id_product': self.id_product,
            'tenSP': self.tenSP,
            'size': self.size,
            'soLuong': self.soLuong,
            'giaGoc': self.giaGoc,
            'ngayTao': self.ngayTao.isoformat() if self.ngayTao else None,
            'tongTien': self.tongTien
        }

@dataclass
class ImportOrder:
    id: Optional[int] = None                #mã đơn hàng
    tenNhaCungCap: Optional[str] = None     #tên nhà cung cấp
    ngayNhapHang: Optional[datetime] = None #ngày nhập hàng
    tinhTrang: Optional[str] = None         #tình trạng
    ghiChu: Optional[str] = None            #ghi chú
    tienVanChuyen: Optional[float] = 0.0    #tiền vận chuyển
    ngayTao: Optional[datetime] = None      #ngày tạo đơn nhập hàng
    DSsanpham: List[ImportItems] = field(default_factory = list) #danh sách sản phẩm đơn nhập hàng

    def Tinh_TongChiPhi(self) -> float:
        '''
        Tính tổng chi phí đơn nhập hàng
        '''
        tongChiPhi = sum(sanpham.Tinh_tongTien() for sanpham in self.DSsanpham)
        tongChiPhi += self.tienVanChuyen
        return tongChiPhi

    def ThemSanPham(self, id_product:int, soLuong:int, giaGoc: float):
        '''
        thêm sản phẩm vào đơn nhập hàng
        '''
        sanpham = ImportItems(
            id_product = id_product,
            soLuong = soLuong,
            giaGoc = giaGoc,
            tongtien = soLuong * giaGoc
            )
        self.DSsanpham.append(sanpham)
        self.Tinh_TongChiPhi()

    def TongSoLuong(self) -> int:
        '''
        Tính tổng số lượng sản phẩm đơn nhập hàng
        '''
        return sum(sanpham.soLuong for sanpham in self.DSsanpham)
    
    def to_dict(self) -> dict:
        '''
        chuyen ImportOrder sang dict
        '''
        return{
            'id': self.id,
            'tenNhaCungCap': self.tenNhaCungCap,
            'ngayNhapHang': self.ngayNhapHang.isoformat() if self.ngayNhapHang else None,
            'tinhTrang': self.tinhTrang,
            'ghiChu':self.ghiChu,
            'tienVanChuyen':self.tienVanChuyen,
            'ngayTao':self.ngayTao.isoformat() if self.ngayTao else None,
            'DSsanpham':[sanpham.to_dict() for sanpham in self.DSsanpham],
            'tongSoLuong':self.TongSoLuong(),
            'tongChiPhi':self.Tinh_TongChiPhi()
        }
    
@classmethod
def from_dict(cls, data:dict) -> 'ImportOrder':
    '''
    tao ImportOrder tu dict
    '''
    ngayTao = None
    ngayNhapHang = None
    DSsanpham = []
    if data.get('ngayTao'):
        ngayTao = datetime.fromisoformat(data['ngayTao'])
    if data.get('ngayNhapHang'):
        ngayNhapHang = datetime.fromisoformat(data['ngayNhapHang'])
    for sanpham in data.get('DSsanpham',[]):
        DSsanpham.append(ImportItems(**sanpham))
    return cls(
        id = data.get('id'),
        tenNhaCungCap = data.get('tenNhaCungCap'),
        ngayNhapHang = ngayNhapHang,
        tinhTrang = data.get('tinhTrang',"HOAN TAT"),
        ghiChu = data.get('ghiChu'),
        tienVanChuyen = data.get('tienVanChuyen',0.0),
        ngayTao = ngayTao,
        DSsanpham = DSsanpham
    )

    
