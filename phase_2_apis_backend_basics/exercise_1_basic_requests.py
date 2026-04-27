"""
Bài tập 1: Gọi API cơ bản với requests library
Mục tiêu: Hiểu về GET requests, JSON responses, và status codes
"""

import requests
import json

# ============================================
# BÀI TẬP 1.1: GET request cơ bản
# ============================================
def exercise_1_1():
    """
    Gọi API công khai JSONPlaceholder để lấy thông tin bài viết
    URL: https://jsonplaceholder.typicode.com/posts/1
    """
    print("=" * 50)
    print("BÀI TẬP 1.1: GET Request Cơ Bản")
    print("=" * 50)
    
    # TODO: 
    # 1. Gọi GET request đến https://jsonplaceholder.typicode.com/posts/1
    # 2. In ra status code
    # 3. In ra JSON response
    # 4. Trích xuất và in ra userId, title
    path = "https://jsonplaceholder.typicode.com/posts/1"
    respone = requests.get(path)
    print(respone.status_code)
    print(respone.json())
    data = respone.json()
    print(f"userId:", data["userId"], f"title:", data["title"])

    # Gợi ý: sử dụng requests.get()
    


# ============================================
# BÀI TẬP 1.2: Xử lý lỗi và status codes
# ============================================
def exercise_1_2():
    """
    Thử gọi API với URL không tồn tại, xử lý các status codes
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 1.2: Xử Lý Status Codes")
    print("=" * 50)
    
    # TODO:
    # 1. Gọi GET request đến https://jsonplaceholder.typicode.com/posts/999999 (không tồn tại)
    # 2. Kiểm tra status code
    # 3. Xử lý trường hợp:
    #    - 200: OK - In ra dữ liệu
    #    - 404: Not Found - In ra "Bài viết không tồn tại"
    #    - Các status khác - In ra thông báo lỗi
    
    path = "https://jsonplaceholder.typicode.com/posts/999999"
    response = requests.get(path)
    if response.status_code == 200:
        print(response.json())
    elif response.status_code == 404:
        print("Bài viết không tồn tại")
    else:
        print("Lỗi không xác định:", response.status_code)





# ============================================
# BÀI TẬP 1.3: Timeout và Exception Handling
# ============================================
def exercise_1_3():
    """
    Thực hành xử lý timeout và các ngoại lệ
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 1.3: Timeout & Exception Handling")
    print("=" * 50)
    
    # TODO:
    # 1. Gọi GET request với timeout = 0.001 giây (quá ngắn, sẽ timeout)
    # 2. Bắt và xử lý requests.Timeout exception
    # 3. Bắt và xử lý requests.ConnectionError exception
    # 4. Bắt và xử lý exception chung Exception
    # 5. In ra thông báo lỗi chi tiết
    path = "https://jsonplaceholder.typicode.com/posts/1"
    try:
        response = requests.get(path, timeout=0.001)
    except requests.Timeout:
        print("TimeOut")
    except requests.ConnectionError:
        print("Connection Error")
    except Exception as e:
        print(print(str(e)))

# ============================================
# BÀI TẬP 1.4: Query Parameters
# ============================================
def exercise_1_4():
    """
    Gọi API với query parameters
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 1.4: Query Parameters")
    print("=" * 50)
    
    # TODO:
    # 1. Gọi GET request để lấy danh sách posts của user_id = 2
    #    URL: https://jsonplaceholder.typicode.com/posts
    #    Query param: userId=2
    # 2. In ra số lượng posts
    # 3. In ra 2 posts đầu tiên
    
    # Gợi ý: dùng params={"userId": 2} trong requests.get()
    URL = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(URL, params={"userId": 2})
    data = response.json()
    print(len(data))
    print(data[0:2])




# ============================================
# BÀI TẬP 1.5: Headers
# ============================================
def exercise_1_5():
    """
    Gọi API công khai GitHub với headers
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 1.5: Headers & User-Agent")
    print("=" * 50)
    
    # TODO:
    # 1. Gọi GitHub API để lấy thông tin user "torvalds" (Linus Torvalds)
    #    URL: https://api.github.com/users/torvalds
    # 2. Thêm User-Agent header (GitHub API yêu cầu)
    #    headers = {"User-Agent": "MyApp/1.0"}
    # 3. In ra thông tin: name, bio, public_repos, followers
    URL = "https://api.github.com/users/torvalds"
    headers = {"User-Agent": "MyApp/1.0"}
    response = requests.get(URL, headers=headers)
    data = response.json()
    
    print(f"Name: {data['name']}")
    print(f"Bio: {data['bio']}")
    print(f"Public Repos: {data['public_repos']}")
    print(f"Followers: {data['followers']}")



# ============================================
# BÀI TẬP 1.6: POST Request
# ============================================
def exercise_1_6():
    """
    Gửi POST request tạo dữ liệu mới
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 1.6: POST Request")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo một JSON object với fields:
    #    - title: "Bài viết của tôi"
    #    - body: "Nội dung bài viết"
    #    - userId: 1
    # 2. Gửi POST request đến:
    #    https://jsonplaceholder.typicode.com/posts
    # 3. In ra response JSON (nên có id được tạo tự động)
    # 4. Kiểm tra status code (nên là 201 Created)
    
    # Gợi ý: sử dụng requests.post() với json=data
    URL = "https://jsonplaceholder.typicode.com/posts"
    json = {
        "title": "Bài viết của tôi",
        "body": "Nội dung bài viết",
        "userId":1
    }
    data = requests.post(URL,json)
    print(data.status_code)


# ============================================
# BƯỚC KIỂM TRA KẾT QUẢ
# ============================================
if __name__ == "__main__":
    print("\n🚀 KHÁM PHÁ GỌIAPI VỚI REQUESTS\n")
    
    # Chạy các bài tập
    exercise_1_1()
    exercise_1_2()
    exercise_1_3()
    exercise_1_4()
    exercise_1_5()
    exercise_1_6()
    
    print("\n" + "=" * 50)
    print("✅ Hoàn thành tất cả bài tập!")
    print("=" * 50)
