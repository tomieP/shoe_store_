"""
test_models.py - Kiểm tra các models đã viết
"""

from datetime import datetime, date
from models import Product, DailyReport, Invoice, ImportOrder
from models.invoice import InvoiceDetail
from models.import_items import ImportItems

def test_product():
    print("=== TEST PRODUCT ===")
    
    # Tạo sản phẩm
    product = Product(
        id = 1,
        tenSP= "Giày Nike Air Max",
        brand= "Nike",
        donGia= 500000,
        soLuong= 10,
        conKinhDoanh= 1,
        imagePath="giayHTH-asia.png",
        QRPath="giayHTH-asia.png",
        ngayCapNhat= datetime.now(),
        ngayTao= datetime.now()

    )
    
    print(f"Product: {product}")
    print(f"Total value: {product.TongGiaTriTonKho():,.0f} VNĐ")
    
    # Giảm giá 20k
    dong = 20
    new_price = product.GiamGia(dong)
    print(f"Price after a {dong} VNĐ discount:{new_price:,.0f} VNĐ")
    
    return product

def test_invoice():
    print("\n=== TEST INVOICE ===")
    
    # Tạo hóa đơn
    invoice = Invoice(
        id=1,
        ngayBan=date.today(),
        phuongThucThanhToan="Tiền mặt",
    )
    
    # Tạo sản phẩm test
    product1 = Product(id=1, tenSP="Giày A", donGia=300000)
    product2 = Product(id=2, tenSP="Giày B", donGia=400000)
    
    # Thêm sản phẩm vào hóa đơn
    invoice.ThemSanPham(product1, 2)  # 2 đôi Giày A
    invoice.ThemSanPham(product2, 1)  # 1 đôi Giày B
    
    # Thêm giảm giá
    invoice.giamGia = 100000
    
    # Tính toán
    invoice.Tinh_thanhTien()
    
    print(f"Total items: {invoice.DemSoLuongSanPham()}")
    print(f"Final amount: {invoice.Tinh_thanhTien():,.0f} VNĐ")
    print(f"Discount: {invoice.giamGia:,.0f} VNĐ")
    print(f"Price after discount: {invoice.GiamGiaTrenTongHoaDon(dong=invoice.giamGia)}")
    
    return invoice

def test_daily_stat():
    print("\n=== TEST DAILY STAT ===")
    
    # Tạo thống kê ngày
    daily_rp = DailyReport(
        id = 1,
        ngayTK = date.today(),
        tongDoanhThu = 10000000,
        tongSPBan = 10,
        tongHD = 10,
        ngayTao = datetime.now()

    )
    
    print(f"Date: {daily_rp.ngayTK}")
    print(f"Revenue: {daily_rp.tongDoanhThu:,.0f} VNĐ")
        
    return daily_rp

def test_to_from_dict():
    print("\n=== TEST TO/FROM DICT ===")
    
    # Tạo Product
    product = Product(
        id = 1,
        tenSP= "Giày Nike Air Max",
        brand= "Nike",
        donGia= 500000,
        soLuong= 10,
        conKinhDoanh= 1,
        imagePath="giayHTH-asia.png",
        QRPath="giayHTH-asia.png",
        ngayCapNhat= datetime.now(),
        ngayTao= datetime.now()

    )
    
    # Chuyển thành dict
    product_dict = product.to_dict()
    print(f"Product to dict: {product_dict}")
    
    # Tạo lại từ dict
    product2 = Product.from_dict(product_dict)
    print(f"Product from dict: {product2}")
    
    # So sánh
    print(f"Are they equal? {product == product2}")

if __name__ == "__main__":
    print("🧪 Testing models...\n")
    
    test_product()
    test_invoice()
    test_daily_stat()
    test_to_from_dict()
    
    print("\n✅ All tests completed!")


