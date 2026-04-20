# Sử dụng bản đầy đủ nhưng ổn định, không có dấu chấm ở cuối nhé
FROM python:3.10-buster

# Ngăn Python tạo file rác và giúp hiện log ngay lập tức
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Cài đặt pip và dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
# Bước này sẽ cài OpenCV-headless rất nhanh và không cần apt-get
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào
COPY . .

# Gom file tĩnh
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Nhớ thay "ten_du_an" bằng tên thư mục chứa file wsgi.py của bạn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]