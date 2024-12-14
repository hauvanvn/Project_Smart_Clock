# Project Smart Clock
Đây là đồ án môn Vật lí cho công nghệ thông tin(PHY00007) tạo ra đồng hồ thông minh và đây là trang web quản lí các thiết bị thông minh.

Đồng hồ Thông minh để bàn(Smart Clock) có chức năng: Hiện thị ngày và giờ, thời tiết hiện tại, sự kiện sắp diễn ra; đo nhiệt độ và độ ẩm trong phòng; 
truyền dữ liệu ghi được lên trang web và thống kê theo ngày, tháng, năm; đặt báo thức, event,... Ngoài ra đồng hồ có dải đèn led có thể tùy chính trên trang web và loa kêu khi báo thức
và event chũng có thể điều chỉnh trên trang web. Sản phẩm là sản phẩm giả lập trên Wokwi.

Những framework được sử dụng trong đồ án:
1. Wokwi cho giả lập sản phẩm
2. Bootstrap css framework cho frontend
3. Django framework cho backend
4. mySQL cho database

### Thành viên trong Nhóm:
1. Nguyễn Văn Hậu(22127105), Design và Backend Dev
2. Nguyễn Văn Đức(22127073), Design và Frontend Dev

## Hướng dẫn chạy server
1. `py -m venv .venv` với người lần đầu cài.
2. `. .venv/Scripts/activate` để khởi tạo virtual environment.
3. `git clone https://github.com/hauvanvn/Project_Smart_Clock.git` với người lần đầu tải.
4. `cd Project_Smart_Clock`.
5. `pip install -r requirements.txt` để cài các package cần thiết.
6. Cài đặt Wsl(Windows Subsystem for Linux) để cài redis:
    - `sudo apt update`
    - `sudo apt install redis`
    - `sudo service redis-server start`
    - Để kiểm tra redis-server có hoạt động hay không: `redis-cli ping`. Nếu trả về PONG thì redis đã hoạt động.
7. `daphne -p 8000 IOT_Management.asgi:application` để chạy server(both develop and product).
8. Mở thêm một terminal và thực hiện bước 2, 4. Sau đó chạy lệnh `py manage.py run_mqtt` để chạy mqtt websocket để giao tiếp với thiết bị và server.

Sau khi làm mà có dowload thêm pip mới thì xài lệnh này: `py -m pip freeze > requirements.txt`.

Cảm ơn các bạn đã đọc.
