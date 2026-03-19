#BÀI TẬP LỚN MÔN TRÍ TUỆ NHÂN TẠO & HỌC MÁY

🛠 Hướng dẫn cài đặt
1. Yêu cầu hệ thống
Python 3.9 trở lên.

Đã cài đặt môi trường ảo (Virtual Environment).

2. Cài đặt thư viện
Mở Terminal tại thư mục dự án và chạy lệnh sau để cài đặt các thư viện cần thiết:
pip install tensorflow flask streamlit pillow numpy requests

🚀 Cách chạy chương trình
Để khởi chạy ứng dụng, bạn cần vận hành song song cả Backend và Frontend theo thứ tự sau:

Bước 1: Khởi chạy Backend (AI Server)
Mở một cửa sổ Terminal mới và chạy lệnh:
python processor.py

Đợi cho đến khi hệ thống báo >>> Đã nạp trọng số thành công! và * Running on http://127.0.0.1:5000.

Bước 2: Khởi chạy Frontend (Giao diện Web)
Mở thêm một cửa sổ Terminal thứ hai và chạy lệnh:
streamlit run app.py
Trình duyệt sẽ tự động mở trang web giao diện tại địa chỉ http://localhost:8501.
📸 Hướng dẫn sử dụng
Truy cập giao diện Web qua trình duyệt.

Nhấn vào nút Browse files để tải lên ảnh món ăn (hỗ trợ JPG, PNG, JPEG).

Nhấn nút Phân tích món ăn.

Hệ thống sẽ hiển thị tên món ăn dự đoán và độ tin cậy (%) tương ứng.
