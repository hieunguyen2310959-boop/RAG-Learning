"""
Bài tập 2: Lưu trữ API keys an toàn với .env và python-dotenv
Mục tiêu: Học cách quản lý API keys mà không public lên GitHub
"""

import os
from dotenv import load_dotenv
import requests

# Load biến môi trường từ file .env
load_dotenv()


# ============================================
# BÀI TẬP 2.1: Tải biến môi trường từ .env
# ============================================
def exercise_2_1():
    """
    Tải và sử dụng biến từ .env file
    """
    print("=" * 50)
    print("BÀI TẬP 2.1: Load .env Variables")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo file .env với nội dung:
    #    GITHUB_API_URL=https://api.github.com
    #    REQUEST_TIMEOUT=10
    # 2. Sử dụng os.getenv() để lấy các biến
    # 3. In ra các giá trị lấy được
    # 4. In ra "NOT FOUND" nếu biến không tồn tại
    
    # Gợi ý: os.getenv("VARIABLE_NAME", "default_value")
    
    pass


# ============================================
# BÀI TẬP 2.2: Xử lý API keys an toàn
# ============================================
def exercise_2_2():
    """
    Sử dụng API key từ .env để gọi API
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 2.2: Sử Dụng API Key An Toàn")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo file .env với API key (có thể fake):
    #    OPENWEATHER_API_KEY=abc123xyz789
    # 2. Lấy API key từ .env bằng os.getenv()
    # 3. Kiểm tra xem API key có tồn tại không
    # 4. Nếu không tồn tại, in ra "⚠️ API Key chưa được cấu hình"
    # 5. Nếu tồn tại, in ra "✓ API Key được tải thành công"
    #    (KHÔNG in ra giá trị thực của key!)
    
    pass


# ============================================
# BÀI TẬP 2.3: Xây dựng helper function
# ============================================
def get_api_base_url(service_name):
    """
    Helper function để lấy base URL của các service từ .env
    
    Args:
        service_name: tên service (github, openweather, etc.)
    
    Returns:
        URL hoặc None nếu không tìm thấy
    """
    # TODO: Implement function này
    # 1. Chuyển service_name thành chữ hoa
    # 2. Tạo key như: "{SERVICE_NAME}_URL"
    # 3. Lấy giá trị từ os.getenv()
    # 4. Return URL hoặc None
    
    pass


def exercise_2_3():
    """
    Sử dụng helper function để quản lý URLs
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 2.3: Helper Function cho URLs")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo file .env với:
    #    GITHUB_URL=https://api.github.com
    #    JSONPLACEHOLDER_URL=https://jsonplaceholder.typicode.com
    # 2. Gọi get_api_base_url("github") - nên trả về URL
    # 3. Gọi get_api_base_url("unknown") - nên trả về None
    # 4. In ra kết quả
    
    pass


# ============================================
# BÀI TẬP 2.4: Xây dựng API Client Class
# ============================================
class APIClient:
    """
    Lớp để quản lý API requests với keys từ .env
    """
    
    def __init__(self, service_name, api_key_name=None):
        """
        TODO: Implement __init__
        1. Lưu service_name
        2. Lấy base_url từ .env (hoặc sử dụng get_api_base_url)
        3. Lấy API key từ .env nếu api_key_name được cung cấp
        4. Kiểm tra xem base_url có tồn tại không
        """
        pass
    
    def get(self, endpoint, timeout=10):
        """
        TODO: Implement GET method
        1. Kết hợp base_url + endpoint
        2. Gọi requests.get() với timeout
        3. Trả về response object hoặc raise exception
        4. Xử lý connection errors
        """
        pass


def exercise_2_4():
    """
    Sử dụng APIClient class
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 2.4: API Client Class")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo instance của APIClient cho github service
    # 2. Gọi .get("/users/torvalds") để lấy thông tin Linus Torvalds
    # 3. In ra name, bio, followers
    # 4. Xử lý các lỗi có thể xảy ra
    
    pass


# ============================================
# BƯỚC KIỂM TRA KẾT QUẢ
# ============================================
if __name__ == "__main__":
    print("\n🔐 QUẢN LÝ API KEYS AN TOÀN\n")
    
    exercise_2_1()
    exercise_2_2()
    exercise_2_3()
    exercise_2_4()
    
    print("\n" + "=" * 50)
    print("✅ Hoàn thành tất cả bài tập!")
    print("=" * 50)
