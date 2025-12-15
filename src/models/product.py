from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Product:
    id:Optional[int] = None
    tenSP: Optional[str] = None
    mota: Optional[str] = None
    brand: Optional[str] = None
    donGia: float = 0.0
    size: Optional[int] = None
    soluongTon: int = 0
    conKinhDoanh: int = 1 #1: con kinh doanh, 0: ngung kinh doanh
    imagePath: Optional[str] = None
    QRPath: Optional[str] = None
    ngayCapNhat: Optional[datetime] = None
    taoNgay: Optional[datetime] = None

    def TongGiaTriTonKho(self) ->float:
        '''
        tính tổng giá trị tồn kho của từng sản phẩm
        '''
        return self.donGia * self.soluongTon
    def TonKho(self) -> str:
        '''
        trả về số lượng tồn kho của sản phẩm
        '''
        return f"Số lượng tồn kho của sản phẩm {self.id}_{self.tenSP}: {self.soluongTon}."
    def GiamGia(self,dong:float) -> float:
        '''
        Docstring for GiamGia
        Áp dụng giảm giá cho sản phẩm
        dong: số tiền giảm
        (ví dụ: dong = 5 => giam 5k trên sp)
        return giá sau khi giảm
        '''
        if 0 <= dong <= self.donGia:
            self.donGia -= dong
        return self.donGia
    def to_dict(self) ->dict:
        '''
        Docstring for to_dict
        
        chuyển đổi dữ liệu sang dict
        để lưu vào db
        '''
        return{
            'id':self.id,
            'tenSp':self.tenSP,
            'mota':self.mota,
            'brand':self.brand,
            'donGia':self.donGia,
            'size':self.size,
            'soluongTon':self.soluongTon,
            'conKinhDoanh':self.conKinhDoanh,
            'imagePath':self.imagePath,
            'QrPath':self.QrPath,
            'ngayCapNhat':self.ngayCapNhat.isoformat() if self.ngayCapNhat else None,
            'taoNgay':self.taoNgay.isoformat() if self.taoNgay else None
        }
    
@classmethod
def from_dict(cls,data:dict) -> 'Product':
    ngayTao = None
    if data.get('ngayTao'):
        ngayTao = datetime.fromisoformat(data['ngayTao'])
    ngayCapNhat = None
    if data.get('ngayCapNhat'):
        ngayCapNhat = datetime.fromisoformat(data['ngayCapNhat'])
    return cls(
        id = data.get('id'),
        tenSp = data.get('tenSP'),
        mota = data.get('mota'),
        brand = data.get('brand'),
        donGia = data.get('donGia'),
        size = data.get('size'),
        soluongTon = data.get('soluongTon'),
        conKinhDoanh = data.get('conKinhDoanh'),
        imagePath = data.get('imagePath'),
        QRPath = data.get('QRPath'),
        ngayCapNhat = ngayCapNhat,
        ngayTao = ngayTao
    )