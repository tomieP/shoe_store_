from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DailyReport:
    id: Optional[int] = None                #mã thống kê
    daily_revenue: float = 0.0              #tổng doanh thu
    total_units_sold: int = 0               #tổng sản phẩm bán
    invoice_total_amount: int = 0           #tổng hóa đơn
    note: Optional[str] = None              #ghi chú
    created_at: Optional[datetime] = None   #ngày tạo thống kê

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
            'daily_revenue':self.daily_revenue,
            'total_units_sold':self.total_units_sold,
            'invoice_total_amount':self.invoice_total_amount,
            'note':self.note,
            'created_at':self.created_at.isoformat() if self.ngayTao else None
        }

@classmethod
def from_dict(cls,data:dict) -> 'DailyReport':
    '''
    tạo dailyrp từ dict
    '''
    return cls(
        id = data.get('id'),
        daily_revenue = data.get('daily_revenue'),
        total_units_sold = data.get('total_units_sold'),
        invoice_total_amount = data.get('invoice_total_amount'),
        note = data.get('note'),
        created_at = datetime.fromisoformat(data.get('created_at')) if data.get('created_at') else None
    )