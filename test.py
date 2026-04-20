import cv2

img = cv2.imread(r"D:\CODE\Web\Python\Dejango\Web_DDMaQR\1.png")  # đổi thành tên ảnh của bạn

data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)

print("Nội dung QR:", data if data else "Không có QR")