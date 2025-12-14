import qrcode
from pathlib import Path

def SaveAt(filename):
    path = r'./src/qrcodes/products'
# Source - https://stackoverflow.com/a
# Posted by wim, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-05, License - CC BY-SA 4.0
#tao folder neu chua co
    Path(path).mkdir(parents=True, exist_ok=True)

    return path + '/' + filename
    


def generate_qr_code(data, filename):

    filename += ".png"
    qr = qrcode.make(data)
    filepath = SaveAt(filename)
    qr.save(filepath)
    print(f"QR code saved as {filename} at {filepath}")
    return qr

if __name__ == "__main__":
    data = input("Nhập dữ liệu để tạo QR code: ")
    filename = input("Nhập tên sản phẩm: ")
    generate_qr_code(data, filename)
