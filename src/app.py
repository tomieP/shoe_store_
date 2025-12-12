from services.QR_service import generate_qr_code

if __name__ == "__main__":
    data = input("Nhập dữ liệu để tạo QR code: ")
    filename = input("Nhập tên sản phẩm: ")
    generate_qr_code(data, filename)