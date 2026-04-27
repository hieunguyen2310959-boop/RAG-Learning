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
    data1 = os.getenv("GITHUB_API_URL")
    data2 = os.getenv("REQUEST_TIMEOUT")
    
    # In ra GITHUB_API_URL
    print("GITHUB_API_URL:", data1 if data1 else "NOT FOUND")
    
    # In ra REQUEST_TIMEOUT
    print("REQUEST_TIMEOUT:", data2 if data2 else "NOT FOUND")



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
    
    data1 = os.getenv("OPENWEATHER_API_KEY")
    print ("✓ API Key được tải thành công") if data1 else print("⚠️ API Key chưa được cấu hình")


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
    name = (service_name).upper()
    key = f"{name}_URL"
    return os.getenv(key)





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
    print(get_api_base_url("github"))
    print(get_api_base_url("unknown"))


# ============================================
# BÀI TẬP 2.4: Xây dựng API Client Class
# ============================================
class APIClient:
    def __init__(self, service_name, api_key_name=None):
        self.service_name = service_name
        self.base_url = get_api_base_url(service_name)
        self.api_key = os.getenv(api_key_name) if api_key_name else None
        
        if not self.base_url:
            raise ValueError(f"❌ Không tìm thấy base URL cho {service_name}")

    def get(self, endpoint, timeout=10):
        url = self.base_url + endpoint
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi kết nối: {e}")
            raise


def exercise_2_4():
    try:
        client = APIClient("github")
        response = client.get("/users/torvalds")
        data = response.json()  # ← Convert to dict!
        
        print(f"Name: {data.get('name', 'N/A')}")
        print(f"Bio: {data.get('bio', 'N/A')}")
        print(f"Followers: {data.get('followers', 'N/A')}")
    except ValueError as e:
        print(f"❌ Lỗi cấu hình: {e}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")


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
