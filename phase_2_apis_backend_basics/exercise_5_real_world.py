"""
Bài tập 5: Thực tế - Xây dựng mini project
Mục tiêu: Kết hợp tất cả kiến thức để xây dựng ứng dụng thực tế
"""

import requests
import asyncio
import httpx
from datetime import datetime
import csv
import json
from typing import List, Dict


# ============================================
# PROJECT 1: GitHub Repository Analyzer
# ============================================
class GitHubAnalyzer:
    """
    Lấy thông tin chi tiết về repositories của một user
    """
    
    def __init__(self, username):
        """
        TODO:
        1. Lưu username
        2. Khởi tạo base_url = "https://api.github.com"
        3. Khởi tạo headers với User-Agent
        """
        pass
    
    def get_user_info(self):
        """
        TODO:
        1. Gọi GET /users/{username}
        2. Return thông tin: name, bio, public_repos, followers, following
        """
        pass
    
    def get_repositories(self):
        """
        TODO:
        1. Gọi GET /users/{username}/repos
        2. Lọc chỉ public repos
        3. Return list repos với: name, url, stars, language, description
        """
        pass
    
    def get_most_starred_repos(self, limit=5):
        """
        TODO:
        1. Lấy danh sách repos
        2. Sắp xếp theo stars giảm dần
        3. Return top N repos
        """
        pass


def project_1():
    """
    Sử dụng GitHubAnalyzer
    """
    print("=" * 50)
    print("PROJECT 1: GitHub Repository Analyzer")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo GitHubAnalyzer cho username "torvalds"
    # 2. In ra user info
    # 3. In ra 5 repositories được star nhiều nhất
    # 4. Tính statistics: tổng stars, ngôn ngữ được dùng nhiều nhất
    # 5. Xuất kết quả ra CSV file
    
    pass


# ============================================
# PROJECT 2: Weather Data Aggregator
# ============================================
class WeatherAggregator:
    """
    Lấy dữ liệu thời tiết từ multiple cities
    """
    
    def __init__(self, api_key=None):
        """
        TODO:
        1. Lưu api_key từ parameter hoặc từ .env
        2. Khởi tạo base_url = "https://openweathermap.org/data/2.5"
        """
        pass
    
    async def get_weather(self, city):
        """
        TODO:
        1. Gọi async GET /weather?q={city}&appid={api_key}
        2. Parse response JSON
        3. Return: temp, feels_like, humidity, description
        4. Xử lý exception nếu city không tồn tại
        """
        pass
    
    async def get_weather_multiple(self, cities: List[str]):
        """
        TODO:
        1. Gọi get_weather() cho tất cả cities đồng thời
        2. Sử dụng asyncio.gather()
        3. Return list kết quả
        """
        pass


async def project_2():
    """
    Sử dụng WeatherAggregator
    """
    print("\n" + "=" * 50)
    print("PROJECT 2: Weather Data Aggregator")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo WeatherAggregator (nếu không có API key, dùng mock data)
    # 2. Lấy thời tiết cho 5 thành phố: Hà Nội, HCM, Bangkok, Tokyo, Seoul
    # 3. So sánh nhiệt độ, tìm thành phố nóng nhất
    # 4. In ra report
    # 5. Lưu dữ liệu vào JSON file với timestamp
    
    pass


# ============================================
# PROJECT 3: REST API Data Pipeline
# ============================================
class DataPipeline:
    """
    Xây dựng pipeline để lấy, transform, và lưu trữ dữ liệu từ API
    """
    
    def __init__(self, source_url):
        """
        TODO:
        1. Lưu source_url
        2. Khởi tạo list để lưu trữ data
        """
        pass
    
    def extract(self, endpoint):
        """
        TODO:
        1. Gọi GET request
        2. Parse JSON response
        3. Return raw data
        """
        pass
    
    def transform(self, data: List[Dict]):
        """
        TODO:
        1. Lọc các fields không cần thiết
        2. Normalize data (ví dụ: convert date format)
        3. Remove duplicates
        4. Return transformed data
        """
        pass
    
    def load(self, data: List[Dict], filename):
        """
        TODO:
        1. Lưu data vào CSV hoặc JSON file
        2. Thêm timestamp khi lưu
        """
        pass


def project_3():
    """
    Sử dụng DataPipeline
    """
    print("\n" + "=" * 50)
    print("PROJECT 3: REST API Data Pipeline (ETL)")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo DataPipeline với source = jsonplaceholder API
    # 2. Extract: Lấy tất cả posts
    # 3. Transform: 
    #    - Chỉ giữ lại: id, title, body, userId
    #    - Tính độ dài của body
    #    - Group by userId
    # 4. Load: Lưu vào "posts_data.csv"
    # 5. In ra summary: tổng posts, users, stats
    
    pass


# ============================================
# PROJECT 4: API Monitoring Dashboard
# ============================================
class APIMonitor:
    """
    Monitoring health của multiple APIs
    """
    
    def __init__(self):
        """
        TODO:
        1. Khởi tạo dict để lưu status của các API
        2. Khởi tạo dict để lưu response times
        """
        pass
    
    def check_health(self, api_name, url, timeout=5):
        """
        TODO:
        1. Ghi lại thời gian bắt đầu
        2. Gọi GET request với timeout
        3. Tính response time
        4. Lưu: status (UP/DOWN), response_time, timestamp
        5. Return status và response_time
        """
        pass
    
    def check_multiple_apis(self, apis: Dict[str, str]):
        """
        TODO:
        1. Gọi check_health() cho tất cả APIs
        2. Return summary: UP count, DOWN count, avg response time
        """
        pass
    
    def generate_report(self):
        """
        TODO:
        1. Tạo report text về status của tất cả APIs
        2. Include: status, response time, last checked
        3. Return formatted report
        """
        pass


def project_4():
    """
    Sử dụng APIMonitor
    """
    print("\n" + "=" * 50)
    print("PROJECT 4: API Monitoring Dashboard")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo APIMonitor
    # 2. Kiểm tra health của các public APIs:
    #    - https://api.github.com
    #    - https://jsonplaceholder.typicode.com
    #    - https://httpbin.org/get
    #    - https://invalid-api-url-12345.com (nên DOWN)
    # 3. In ra report
    # 4. Tìm API nhanh nhất, chậm nhất
    
    pass


# ============================================
# BƯỚC KIỂM TRA KẾT QUẢ
# ============================================
if __name__ == "__main__":
    print("\n🚀 THỰC TẾ - MINI PROJECTS\n")
    
    project_1()
    asyncio.run(project_2())
    project_3()
    project_4()
    
    print("\n" + "=" * 50)
    print("✅ Hoàn thành tất cả projects!")
    print("=" * 50)
