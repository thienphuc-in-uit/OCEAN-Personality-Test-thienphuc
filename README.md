# 🧠 OCEAN Personality Test - Multi-language Hybrid App
🔗 Trải nghiệm ứng dụng tại đây! > https://ocean-personality-test-thienphuc.streamlit.app/

# 📖 Giới thiệu
Đây là ứng dụng trắc nghiệm tính cách theo mô hình Big Five (OCEAN). Sản phẩm được phát triển và nâng cấp mạnh mẽ từ tiền thân là Solo Project của lớp IT003.Q214 (Cấu trúc dữ liệu và Giải thuật).
Dự án hiện tại đã được hiện đại hóa với kiến trúc lai (Hybrid Architecture), kết hợp giữa hiệu năng xử lý dữ liệu của C++ và sự linh hoạt của Python Streamlit để tạo ra trải nghiệm người dùng tối ưu trên môi trường Web.

# 🚀 Tính năng nổi bật
Hybrid Engine: Lõi tính toán được viết bằng C++, xử lý thuật toán so khớp qua thư viện động (.dll cho Windows và .so cho Linux).
Thuật toán Cosine Similarity: Sử dụng đại số tuyến tính để đo lường độ tương đồng giữa vector tính cách người dùng và hệ thống nhân vật trong không gian 5 chiều.
Đa ngôn ngữ (I18n): Hỗ trợ Tiếng Việt, Tiếng Anh và Tiếng Đức (Deutsch) với khả năng chuyển đổi thời gian thực.
Kho dữ liệu đa dạng: Hệ thống 486 câu hỏi và nhiều vũ trụ nhân vật nổi tiếng (Hogwarts, Disney, Star Wars...).

# 🏗️ Kiến trúc hệ thống
Ứng dụng sử dụng ctypes để làm cầu nối giữa Python và C++:
Frontend (Python): Quản lý State, thu thập input và hiển thị giao diện đa ngôn ngữ.
Logic (C++ Engine): Nhận điểm số từ Python, thực hiện tính toán độ tương đồng Cosine trên tập dữ liệu lớn và trả về kết quả ngay lập tức.

# 🛠️ Công nghệ sử dụng
Ngôn ngữ: C++17, Python 3.9+
Trình biên dịch: g++ (GCC cho Linux/Cloud và MinGW cho Windows).
Deployment: Streamlit Community Cloud.

# 📂 Cấu trúc thư mục
Plaintext
.
├── app.py              # File chạy giao diện chính (Streamlit)
├── core_engine.so      # Thư viện động C++ (Linux/Cloud)
├── core_engine.dll     # Thư viện động C++ (Windows)
├── api_wrapper.cpp     # C++ API Wrapper
├── questions_*.txt     # Dữ liệu câu hỏi đa ngôn ngữ
├── *.people            # Data vector nhân vật
└── requirements.txt    # Thư viện Python phụ thuộc

# 👤 Tác giả
Phan Nguyễn Thiên Phúc - Sinh viên Khoa Khoa học Dữ liệu Trường Đại học Công nghệ Thông tin (UIT) - VNU-HCM.
Dự án phát triển dựa trên nền tảng kiến thức môn IT003 - Lớp IT003.Q214.

# 🙏 Lời cảm ơn (Acknowledgements)
Đặc biệt gửi lời cảm ơn chân thành đến ThS. Huỳnh Tân Bối.
Nhờ có sự hướng dẫn tận tình và những kiến thức nền tảng vững chắc từ môn học IT003 của cô, dự án cá nhân này mới có cơ hội được hoàn thiện, tối ưu và phát triển thành một ứng dụng thực tế hoàn chỉnh như hiện tại.
