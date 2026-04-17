"""
Bài tập 3: Gọi API bất đồng bộ với httpx và aiohttp
Mục tiêu: Học cách gọi multiple API calls cùng lúc một cách hiệu quả
"""

import asyncio
import httpx
import aiohttp
import time


# ============================================
# BÀI TẬP 3.1: httpx synchronous client
# ============================================
def exercise_3_1():
    """
    So sánh requests vs httpx (cùng synchronous)
    """
    print("=" * 50)
    print("BÀI TẬP 3.1: httpx Library")
    print("=" * 50)
    
    # TODO:
    # 1. Sử dụng httpx.Client() để tạo client
    # 2. Gọi GET request đến https://jsonplaceholder.typicode.com/posts/1
    # 3. In ra status code và title
    # 4. Đóng client connection
    # 5. So sánh với requests library
    
    # Gợi ý: 
    # with httpx.Client() as client:
    #     response = client.get(url)
    
    pass


# ============================================
# BÀI TẬP 3.2: httpx AsyncClient cơ bản
# ============================================
async def exercise_3_2():
    """
    Gọi single API request một cách asynchronous
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 3.2: httpx AsyncClient - Single Call")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo AsyncClient
    # 2. Gọi async GET request đến https://jsonplaceholder.typicode.com/posts/1
    # 3. In ra response
    # 4. Đóng client
    
    # Gợi ý:
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(url)
    
    pass


# ============================================
# BÀI TẬP 3.3: Multiple calls synchronously (tính giờ)
# ============================================
def exercise_3_3():
    """
    Gọi 3 API requests tuần tự (synchronous) và đo thời gian
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 3.3: Sequential Requests (Synchronous)")
    print("=" * 50)
    
    # TODO:
    # 1. Ghi lại thời gian bắt đầu
    # 2. Gọi 3 GET requests tuần tự:
    #    - https://jsonplaceholder.typicode.com/posts/1
    #    - https://jsonplaceholder.typicode.com/posts/2
    #    - https://jsonplaceholder.typicode.com/posts/3
    # 3. In ra 3 titles
    # 4. Tính thời gian tổng cộng
    # 5. In ra "Sequential time: X seconds"
    
    pass


# ============================================
# BÀI TẬP 3.4: Multiple calls concurrently (tính giờ)
# ============================================
async def exercise_3_4():
    """
    Gọi 3 API requests cùng lúc (concurrent) và đo thời gian
    So sánh với bài 3.3
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 3.4: Concurrent Requests (Asynchronous)")
    print("=" * 50)
    
    # TODO:
    # 1. Ghi lại thời gian bắt đầu
    # 2. Tạo list 3 URLs:
    #    - https://jsonplaceholder.typicode.com/posts/1
    #    - https://jsonplaceholder.typicode.com/posts/2
    #    - https://jsonplaceholder.typicode.com/posts/3
    # 3. Sử dụng asyncio.gather() để gọi cùng lúc
    # 4. In ra 3 titles
    # 5. Tính thời gian tổng cộng
    # 6. In ra "Concurrent time: X seconds"
    # 7. So sánh với thời gian từ bài 3.3
    
    # Gợi ý:
    # async def fetch_one(client, url):
    #     response = await client.get(url)
    #     return response
    # 
    # tasks = [fetch_one(client, url) for url in urls]
    # responses = await asyncio.gather(*tasks)
    
    pass


# ============================================
# BÀI TẬP 3.5: Error handling with asyncio
# ============================================
async def exercise_3_5():
    """
    Xử lý lỗi trong concurrent requests
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 3.5: Error Handling - Async")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo list URLs, bao gồm cả URL không tồn tại:
    #    - https://jsonplaceholder.typicode.com/posts/1
    #    - https://jsonplaceholder.typicode.com/posts/999999 (không tồn tại)
    #    - https://invalid-domain-12345.com/posts (domain không hợp lệ)
    # 2. Gọi concurrent requests
    # 3. Xử lý từng response:
    #    - Nếu status 200: in ra title
    #    - Nếu status 404: in ra "Not found"
    #    - Nếu connection error: in ra "Connection error"
    # 4. Tiếp tục xử lý các URL khác dù có lỗi
    
    # Gợi ý: Sử dụng try-except trong function fetch_one
    
    pass


# ============================================
# BÀI TẬP 3.6: aiohttp alternative
# ============================================
async def exercise_3_6():
    """
    Sử dụng aiohttp thay vì httpx
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 3.6: aiohttp Library")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo aiohttp.ClientSession()
    # 2. Gọi GET request đến https://jsonplaceholder.typicode.com/posts/1
    # 3. Parse JSON response
    # 4. In ra title
    # 5. Đóng session
    
    # Gợi ý:
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as resp:
    #         data = await resp.json()
    
    pass


# ============================================
# BƯỚC KIỂM TRA KẾT QUẢ
# ============================================
if __name__ == "__main__":
    print("\n⚡ GỌIAPI BẤT ĐỒNG BỘ VỚI HTTPX VÀ AIOHTTP\n")
    
    # Bài tập 3.1 - synchronous
    exercise_3_1()
    
    # Bài tập 3.2 - async single call
    asyncio.run(exercise_3_2())
    
    # Bài tập 3.3 - sequential (đo thời gian)
    exercise_3_3()
    
    # Bài tập 3.4 - concurrent (đo thời gian) 
    asyncio.run(exercise_3_4())
    
    # Bài tập 3.5 - error handling
    asyncio.run(exercise_3_5())
    
    # Bài tập 3.6 - aiohttp
    asyncio.run(exercise_3_6())
    
    print("\n" + "=" * 50)
    print("✅ Hoàn thành tất cả bài tập!")
    print("=" * 50)
