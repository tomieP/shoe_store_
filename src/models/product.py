from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Product:
    id:Optional[int] = None                    #mã sản phẩm
    tenSP: Optional[str] = None                #tên sản phẩm    
    mota: Optional[str] = None                 #mô tả sản phẩm
    brand: Optional[str] = None                #brand sản phẩm
    donGia: float = 0.0                        #đơn giá 
    size: Optional[int] = None                 #size sản phẩm
    soLuong: int = 0                        #số lượng tồn kho
    conKinhDoanh: int = 1                      #1: con kinh doanh, 0: ngung kinh doanh
    imagePath: Optional[str] = None            #đường đẫn ảnh
    QRPath: Optional[str] = None               #đường dẫn mã QR
    ngayCapNhat: Optional[datetime] = None     #ngày cập nhật sản phẩm
    ngayTao: Optional[datetime] = None         #ngày tạo sản phẩm

    def TongGiaTriTonKho(self) ->float:
        '''
        tính tổng giá trị tồn kho của từng sản phẩm
        '''
        return self.donGia * self.soLuong
    def TonKho(self) -> str:
        '''
        trả về số lượng tồn kho của sản phẩm
        '''
        return f"Số lượng tồn kho của sản phẩm {self.id}_{self.tenSP}: {self.soLuong}."
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
            'tenSP':self.tenSP,
            'mota':self.mota,
            'brand':self.brand,
            'donGia':self.donGia,
            'size':self.size,
            'soLuong':self.soLuong,
            'conKinhDoanh':self.conKinhDoanh,
            'imagePath':self.imagePath,
            'QRPath':self.QRPath,
            'ngayCapNhat':self.ngayCapNhat.isoformat() if self.ngayCapNhat else None,
            'ngayTao':self.ngayTao.isoformat() if self.ngayTao else None
        }
    
    @classmethod
    def from_dict(cls,data:dict) -> 'Product':
        '''
        Docstring for from_dict
        
        chuyển từ dict sang class Product
        để chuyền dữ liệu từ db sang object
        '''
        ngayTao = None
        if data.get('ngayTao'):
            ngayTao = datetime.fromisoformat(data['ngayTao'])
        ngayCapNhat = None
        if data.get('ngayCapNhat'):
            ngayCapNhat = datetime.fromisoformat(data['ngayCapNhat'])
        return cls(
            id = data.get('id'),
            tenSP = data.get('tenSP'),
            mota = data.get('mota'),
            brand = data.get('brand'),
            donGia = data.get('donGia'),
            size = data.get('size'),
            soLuong = data.get('soLuong'),
            conKinhDoanh = data.get('conKinhDoanh'),
            imagePath = data.get('imagePath'),
            QRPath = data.get('QRPath'),
            ngayCapNhat = ngayCapNhat,
            ngayTao = ngayTao
        )