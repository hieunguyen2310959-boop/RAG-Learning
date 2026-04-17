# 📚 Khung Bài Tập: Calling External APIs with Python

## 📋 Tổng Quan

Bộ bài tập toàn diện về gọi API bên ngoài với Python, bao gồm:
- ✅ Kiến thức cơ bản về `requests` library
- ✅ Quản lý API keys an toàn với `.env` và `python-dotenv`
- ✅ Gọi API bất đồng bộ với `httpx` và `aiohttp`
- ✅ Xử lý lỗi nâng cao (retry, circuit breaker, caching, rate limiting)
- ✅ Các mini project thực tế

---

## 🎯 Cấu Trúc Bài Tập

### **Exercise 1: Basic Requests** (`exercise_1_basic_requests.py`)
Học cơ bản về gọi API với `requests` library

**Các bài tập:**
1. **1.1** - GET request cơ bản
2. **1.2** - Xử lý status codes (200, 404, etc.)
3. **1.3** - Timeout & Exception handling
4. **1.4** - Query parameters
5. **1.5** - Headers & User-Agent
6. **1.6** - POST request

**API sử dụng:**
- JSONPlaceholder (fake API): https://jsonplaceholder.typicode.com
- GitHub API: https://api.github.com

---

### **Exercise 2: Environment & API Keys** (`exercise_2_env_and_keys.py`)
Quản lý API keys an toàn

**Các bài tập:**
1. **2.1** - Tải `.env` variables
2. **2.2** - Sử dụng API keys an toàn
3. **2.3** - Helper functions cho URLs
4. **2.4** - Xây dựng API Client class

**Học:**
- Tại sao không nên commit `.env` file
- Cách sử dụng `python-dotenv`
- Thiết kế API client reusable

---

### **Exercise 3: Async API Calls** (`exercise_3_async_api.py`)
Gọi API bất đồng bộ với `httpx` và `aiohttp`

**Các bài tập:**
1. **3.1** - `httpx` synchronous client
2. **3.2** - `httpx` AsyncClient (single call)
3. **3.3** - Sequential requests (đo thời gian)
4. **3.4** - Concurrent requests (đo thời gian + so sánh)
5. **3.5** - Error handling với async
6. **3.6** - `aiohttp` alternative

**Học:**
- Sự khác biệt giữa sync vs async
- Cách sử dụng `asyncio.gather()`
- Performance improvement từ concurrency

---

### **Exercise 4: Advanced Patterns** (`exercise_4_advanced.py`)
Các pattern nâng cao để xây dựng robust API client

**Các bài tập:**
1. **4.1** - Retry logic với exponential backoff
2. **4.2** - Circuit breaker pattern
3. **4.3** - Response caching
4. **4.4** - Rate limiting (Token bucket)
5. **4.5** - Robust API Client (kết hợp tất cả)

**Học:**
- Cách handle transient failures
- Tối ưu hóa performance
- Bảo vệ API từ overload

---

### **Exercise 5: Real-World Projects** (`exercise_5_real_world.py`)
Mini projects thực tế

**Các project:**
1. **PROJECT 1** - GitHub Repository Analyzer
   - Lấy thông tin repositories
   - Phân tích stars, languages
   - Xuất CSV report

2. **PROJECT 2** - Weather Data Aggregator
   - Gọi weather API
   - Xử lý async requests
   - Compare data từ multiple cities

3. **PROJECT 3** - REST API Data Pipeline (ETL)
   - Extract từ API
   - Transform data
   - Load vào file

4. **PROJECT 4** - API Monitoring Dashboard
   - Check health của multiple APIs
   - Track response times
   - Generate report

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. **Setup Environment**

```bash
# Tạo virtual environment (tùy chọn nhưng được khuyến nghị)
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (Mac/Linux)
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. **Setup .env File**

```bash
# Copy .env.example thành .env
cp .env.example .env

# Hoặc tạo .env tay:
echo GITHUB_API_URL=https://api.github.com > .env
echo REQUEST_TIMEOUT=10 >> .env
```

### 3. **Chạy Bài Tập**

```bash
# Chạy exercise 1
python exercise_1_basic_requests.py

# Chạy exercise 2
python exercise_2_env_and_keys.py

# Chạy exercise 3 (có async)
python exercise_3_async_api.py

# Chạy exercise 4
python exercise_4_advanced.py

# Chạy exercise 5
python exercise_5_real_world.py
```

---

## 💡 Tips & Tricks

### **API Recommendations**
- **JSONPlaceholder** - Fake JSON API cho testing
  - Endpoint: https://jsonplaceholder.typicode.com
  - Không cần authentication
  - Tất cả requests sẽ thành công

- **GitHub API** - Public API
  - Endpoint: https://api.github.com
  - Cần User-Agent header
  - Rate limit: 60 requests/hour (không auth)

- **OpenWeather API** - Weather data
  - Endpoint: https://openweathermap.org/data/2.5
  - Cần API key
  - Free tier có sẵn

### **Common Errors & Solutions**

| Error | Nguyên nhân | Giải pháp |
|-------|-----------|---------|
| `requests.exceptions.Timeout` | Request quá lâu | Tăng timeout value |
| `requests.exceptions.ConnectionError` | Không kết nối được | Kiểm tra URL, internet |
| `json.JSONDecodeError` | Response không phải JSON | Kiểm tra Content-Type |
| `KeyError` từ `.env` | Biến không tồn tại | Tạo `.env` đúng format |

### **Performance Tips**
- Sử dụng **async** cho multiple API calls
- Implement **caching** để avoid duplicate requests
- Sử dụng **rate limiting** để respect API limits
- Implement **retry logic** cho reliability

---

## 📚 Kiến Thức Cần Biết

### **Before Starting**
- Cơ bản về HTTP (GET, POST, PUT, DELETE)
- Request/Response structure
- JSON format
- Python basics (functions, classes, decorators)

### **Will Learn**
- Thư viện requests, httpx, aiohttp
- Async/await programming
- Error handling patterns
- API design best practices
- Environment variables management

---

## 🔍 Debugging Tips

```python
# Xem chi tiết request
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Enable logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ✅ Checklist Hoàn Thành

- [ ] Completed Exercise 1 (Basic requests)
- [ ] Completed Exercise 2 (Environment & keys)
- [ ] Completed Exercise 3 (Async API calls)
- [ ] Completed Exercise 4 (Advanced patterns)
- [ ] Completed Exercise 5 (Real-world projects)
- [ ] All outputs working correctly
- [ ] No API keys in source code
- [ ] Error handling implemented
- [ ] Async calls running concurrently
- [ ] Caching working properly

---

## 📖 Tài Liệu Tham Khảo

- [Requests Documentation](https://docs.python-requests.org/)
- [HTTPX Documentation](https://www.python-httpx.org/)
- [AIOHTTP Documentation](https://docs.aiohttp.org/)
- [Python-Dotenv](https://github.com/theskumar/python-dotenv)
- [Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

---

## 🎓 Mục Tiêu Học Tập

Sau khi hoàn thành tất cả bài tập, bạn sẽ:
- ✅ Hiểu cách gọi external APIs
- ✅ Quản lý API keys an toàn
- ✅ Xử lý errors và edge cases
- ✅ Tối ưu hóa performance với async
- ✅ Implement advanced patterns (retry, circuit breaker, cache)
- ✅ Xây dựng production-ready API clients
- ✅ Debug và troubleshoot API issues

---

**Happy Learning! 🚀**

Nếu bạn gặp vấn đề, hãy kiểm tra:
1. URL của API (đúng format?)
2. API key (hợp lệ?)
3. Network connection
4. Status code của response
5. JSON format

