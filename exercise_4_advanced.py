"""
Bài tập 4: Nâng cao - Retry logic, Rate limiting, Caching
Mục tiêu: Xây dựng robust API client với xử lý lỗi nâng cao
"""

import requests
import time
import json
from functools import wraps
from datetime import datetime, timedelta
import asyncio
import httpx


# ============================================
# BÀI TẬP 4.1: Retry logic với exponential backoff
# ============================================
def retry_with_backoff(max_retries=3, backoff_factor=2):
    """
    Decorator để thử lại request nếu thất bại
    
    Args:
        max_retries: số lần thử lại
        backoff_factor: hệ số backoff (2^attempt * backoff_factor)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Implement retry logic
            # 1. Loop từ 0 đến max_retries
            # 2. Thử gọi func
            # 3. Nếu thành công, return result
            # 4. Nếu lỗi và không phải lần cuối:
            #    - Tính delay = backoff_factor ^ attempt
            #    - In ra "Retry attempt X after Y seconds"
            #    - Sleep X giây
            # 5. Nếu lần cuối vẫn lỗi, raise exception
            pass
        return wrapper
    return decorator


@retry_with_backoff(max_retries=3, backoff_factor=1)
def fetch_with_retry(url, timeout=5):
    """
    Gọi API với retry logic
    """
    # TODO:
    # 1. Gọi requests.get(url, timeout=timeout)
    # 2. Raise exception nếu status không phải 2xx
    # 3. Return response
    pass


def exercise_4_1():
    """
    Thử gọi API với retry logic
    """
    print("=" * 50)
    print("BÀI TẬP 4.1: Retry with Exponential Backoff")
    print("=" * 50)
    
    # TODO:
    # 1. Gọi fetch_with_retry() với URL hợp lệ
    # 2. Kiểm tra xem retry logic hoạt động không
    # 3. Có thể test bằng cách nhập URL "timeout" trong retry logic
    
    pass


# ============================================
# BÀI TẬP 4.2: Request timeout + Circuit breaker pattern
# ============================================
class CircuitBreaker:
    """
    Circuit Breaker pattern để tránh gọi API quá nhiều khi service down
    """
    
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        """
        TODO: Implement __init__
        1. Lưu failure_threshold
        2. Lưu recovery_timeout
        3. Khởi tạo:
           - failure_count = 0
           - last_failure_time = None
           - state = "CLOSED" (bình thường)
        """
        pass
    
    def call(self, func, *args, **kwargs):
        """
        TODO: Implement call method
        1. Kiểm tra state của circuit breaker
        2. Nếu state = "OPEN" (service down):
           - Nếu đủ recovery_timeout: set state = "HALF_OPEN"
           - Nếu chưa đủ: raise "Circuit breaker is OPEN"
        3. Thử gọi func
        4. Nếu thành công:
           - Nếu state = "HALF_OPEN": set state = "CLOSED"
           - Đặt failure_count = 0
           - Return result
        5. Nếu lỗi:
           - Tăng failure_count
           - Nếu failure_count > failure_threshold: state = "OPEN"
           - Raise exception
        """
        pass


def exercise_4_2():
    """
    Sử dụng Circuit Breaker pattern
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 4.2: Circuit Breaker Pattern")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo CircuitBreaker instance
    # 2. Định nghĩa function để gọi API bất ổn
    #    (hoặc dùng URL timeout)
    # 3. Gọi 10 lần qua circuit breaker
    # 4. Quan sát state chuyển đổi: CLOSED -> OPEN
    # 5. In ra trạng thái mỗi lần gọi
    
    pass


# ============================================
# BÀI TẬP 4.3: Caching responses
# ============================================
class SimpleCache:
    """
    Cache đơn giản để lưu trữ responses
    """
    
    def __init__(self, ttl_seconds=300):
        """
        TODO: Implement __init__
        1. Lưu ttl_seconds (time-to-live)
        2. Khởi tạo cache dict: {url: (response, timestamp)}
        """
        pass
    
    def get(self, url):
        """
        TODO: Implement get method
        1. Kiểm tra xem url có trong cache không
        2. Nếu có:
           - Kiểm tra xem data có hết hạn không (so sánh timestamp)
           - Nếu còn hạn: return cached response
           - Nếu hết hạn: xóa khỏi cache, return None
        3. Nếu không: return None
        """
        pass
    
    def set(self, url, response):
        """
        TODO: Implement set method
        1. Lưu response và current timestamp vào cache
        """
        pass


def exercise_4_3():
    """
    Sử dụng caching
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 4.3: Response Caching")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo SimpleCache instance với ttl=10 seconds
    # 2. Gọi API lần 1 (nên hit API server)
    # 3. Gọi API lần 2 (nên hit cache)
    # 4. In ra response + "From Cache" hoặc "From API"
    # 5. Đợi 11 seconds
    # 6. Gọi API lần 3 (cache hết hạn, nên hit API server lại)
    
    pass


# ============================================
# BÀI TẬP 4.4: Rate limiting (Token bucket)
# ============================================
class RateLimiter:
    """
    Rate limiter sử dụng Token Bucket algorithm
    """
    
    def __init__(self, requests_per_second=2):
        """
        TODO: Implement __init__
        1. Lưu capacity = requests_per_second
        2. Khởi tạo tokens = requests_per_second
        3. Lưu last_refill_time = current_time
        """
        pass
    
    def allow_request(self):
        """
        TODO: Implement allow_request method
        1. Refill tokens dựa trên thời gian đã trôi qua
           - elapsed_time = current_time - last_refill_time
           - new_tokens = elapsed_time * requests_per_second
           - tokens = min(tokens + new_tokens, capacity)
           - last_refill_time = current_time
        2. Kiểm tra xem tokens > 0 không
           - Nếu có: tokens -= 1, return True
           - Nếu không: return False
        """
        pass


def exercise_4_4():
    """
    Sử dụng rate limiter
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 4.4: Rate Limiting - Token Bucket")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo RateLimiter với 2 requests per second
    # 2. Loop 5 lần, cố gắng gọi API:
    #    - Nếu allow_request() = True: in "Request allowed"
    #    - Nếu = False: in "Rate limit exceeded, wait..."
    #    - Sleep 0.3 seconds giữa các lần
    # 3. Quan sát xem rate limiter hoạt động như thế nào
    
    pass


# ============================================
# BÀI TẬP 4.5: Robust API Client
# ============================================
class RobustAPIClient:
    """
    Kết hợp tất cả: retry, circuit breaker, cache, rate limiting
    """
    
    def __init__(self, base_url, cache_ttl=300, rate_limit=10):
        """
        TODO: Implement __init__
        1. Lưu base_url
        2. Tạo cache
        3. Tạo circuit breaker
        4. Tạo rate limiter
        """
        pass
    
    def get(self, endpoint, **kwargs):
        """
        TODO: Implement get method
        1. Kiểm tra rate limit
           - Nếu exceed: raise "Rate limit exceeded"
        2. Kiểm tra cache
           - Nếu có: return cached response
        3. Kiểm tra circuit breaker
           - Nếu open: raise "Circuit breaker open"
        4. Gọi API
        5. Lưu vào cache
        6. Return response
        """
        pass


def exercise_4_5():
    """
    Sử dụng RobustAPIClient
    """
    print("\n" + "=" * 50)
    print("BÀI TẬP 4.5: Robust API Client")
    print("=" * 50)
    
    # TODO:
    # 1. Tạo RobustAPIClient instance
    # 2. Gọi .get("/posts/1") 3 lần
    # 3. Quan sát:
    #    - Lần 1: hit API, lưu cache
    #    - Lần 2 & 3: hit cache (nhanh hơn)
    # 4. Tạo tình huống rate limit bằng cách gọi nhiều lần
    # 5. In ra log của toàn bộ quá trình
    
    pass


# ============================================
# BƯỚC KIỂM TRA KẾT QUẢ
# ============================================
if __name__ == "__main__":
    print("\n🛡️ API CALLING - NÂNG CAO\n")
    
    exercise_4_1()
    exercise_4_2()
    exercise_4_3()
    exercise_4_4()
    exercise_4_5()
    
    print("\n" + "=" * 50)
    print("✅ Hoàn thành tất cả bài tập nâng cao!")
    print("=" * 50)
