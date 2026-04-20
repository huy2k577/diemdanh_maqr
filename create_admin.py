import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import Admin # Nhớ sửa đúng đường dẫn đến file models của bạn
from django.contrib.auth.hashers import make_password

username = 'admin'
password = '123456'

if not Admin.objects.filter(username=username).exists():
    Admin.objects.create(
        username=username,
        password=make_password(password), # Mã hóa mật khẩu
        full_name='Le Phuoc Huy',
    )
    print("--- Đã tạo tài khoản Admin thành công! ---")
else:
    print("--- Tài khoản đã tồn tại ---")