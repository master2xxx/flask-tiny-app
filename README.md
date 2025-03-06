# Flask Tiny App

- **Họ và tên:** Lê Quang Đỉnh
- **Mã sinh viên:** 22632311

## Mô tả project
Flask Tiny App là một ứng dụng web nhỏ được xây dựng bằng Flask framework. Ứng dụng này cho phép người dùng đăng ký, đăng nhập và quản lý bài viết của họ. Ngoài ra, ứng dụng còn có trang quản trị để quản lý người dùng, bao gồm các chức năng như khóa tài khoản người dùng và đặt lại mật khẩu.

### Chức năng chính:
- Đăng ký, đăng nhập người dùng
- Tạo, chỉnh sửa, xóa bài viết
- Quản lý người dùng (admin)
- Phân trang cho danh sách bài viết
- Xóa nhiều bài viết cùng lúc

## Hướng dẫn cài đặt và chạy

### Cài đặt thủ công
1. Clone repository:
```bash
git clone https://github.com/[username]/flask-tiny-app.git
cd flask-tiny-app
```

2. Tạo và kích hoạt môi trường ảo:
```bash

venv\Scripts\activate  # Trên Windows
```

3. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

4. Chạy ứng dụng:
```bash
python main.py
```

5. Truy cập ứng dụng tại [http://localhost:5000](http://localhost:5000)

### Cài đặt bằng script
```bash
./setup.sh
```

### Chạy với Docker
```bash
docker build -t flask-tiny-app .
docker run -p 5000:5000 flask-tiny-app
```

## Link project đã triển khai
[https://flask-tiny-app.example.com](https://flask-tiny-app.example.com)

## Các phiên bản
- **v1**: Project cơ bản
- **v2**: Thêm chức năng đăng nhập/đăng ký
- **v3**: Thêm trang admin quản lý user
- **v4**: Thêm chức năng xóa nhiều bài viết cùng lúc
- **v5**: Thêm chức năng phân trang

## Công nghệ sử dụng
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- Bootstrap
- Docker
