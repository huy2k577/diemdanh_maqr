import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Thay thông tin bạn muốn vào đây
username = 'admin_huy'
email = 'huy@example.com'
password = 'Matkhau_123@'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"--- Đã tạo xong tài khoản: {username} ---")
else:
    print("--- Tài khoản đã tồn tại ---")