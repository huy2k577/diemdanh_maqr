import qrcode

masv = "DH52300672"
ten = "DUONGTHITHANHTHAO"
ngaysinh = "22.10.2005"

# bỏ khoảng trắng trong tên, viết IN HOA
ten = ten.upper().replace(" ", "")

noi_dung = f"{masv}_{ten}_{ngaysinh}"

img = qrcode.make(noi_dung)
img.save("ma_qr.png")

print("Đã tạo QR với nội dung:")
print(noi_dung)