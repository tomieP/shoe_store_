from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DailyReport:
    id: Optional[int] = None            #mã thống kê
    ngayTK: datetime = None             #ngày thống kê
    tongDoanhThu: float = 0.0           #tổng doanh thu
    tongSPBan: int = 0                  #tổng sản phẩm bán
    tongHD: int = 0                     #tổng hóa đơn
    ghiChu: Optional[str] = None        #ghi chú
    ngayTao: Optional[datetime] = None  #ngày tạo thống kê

    def Tinh_tongDoanhThu(self) -> float:
        '''
        tính tổng doanh thu sau 1 ngày
        '''
    
    def Tinh_tongSPBan(self) -> int:
        '''
        tính tổng sản phẩm bán sau 1 ngày
        '''

    def Tinh_tongHD(self) -> int:
        '''
        tính tổng hóa đơn sau 1 ngày
        '''
    
    def to_dict(self) -> dict:
        '''
        chuyển dailyrp sang dict
        '''
        return{
            'id':self.id,
            'ngayTK':self.ngayTK.isoformat() if self.ngayTK else None,
            'tongDoanhThu':self.tongDoanhThu,
            'tongSPBan':self.tongSPBan,
            'tongHD':self.tongHD,
            'ghiChu':self.ghiChu,
            'ngayTao':self.ngayTao.isoformat() if self.ngayTao else None
        }

@classmethod
def from_dict(cls,data:dict) -> 'DailyReport':
    '''
    tạo dailyrp từ dict
    '''
    ngayTK = None
    if data.get('ngayTK'):
        ngayTK = datetime.fromisoformat(data['ngayTK'])
    if data.get('ngayTao'):
        ngayTao = datetime.fromisoformat(data['ngayTao'])
    return cls(
        id = data.get('id'),
        ngayTK = ngayTK,
        tongDoanhThu = data.get('tongDoanhThu'),
        tongSPBan = data.get('tongSPBan'),
        tongHD = data.get('tongHD'),
        ghiChu = data.get('ghiChu'),
        ngayTao = ngayTao
    )