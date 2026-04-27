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
        backoff_factor: hệ số b ackoff (2^attempt * backoff_factor)
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
            last_exception = None
            for i in range (0, max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if i < max_retries - 1: 
                        delay = backoff_factor ** (i+1)
                        print(f"Retry attempt {i+1} after {delay} seconds")
                        time.sleep(delay)
            raise last_exception
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
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response


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
    url = "https://domain-khong-ton-tai.com"
    try:
        response = fetch_with_retry(url)
        print(f"Thành công: {response.status_code}")
    except Exception as e:
        print(f"\n🛑 Kết quả cuối cùng: Thất bại sau nhiều lần thử.")
        print(f"Lỗi gặp phải: {e}")


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
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
    
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
        if self.state == "OPEN":
            current_time = time.time()
            if current_time - self.last_failure_time >= self.recovery_timeout:
                print("Chuyen sang Half-Open")
                self.state = "HALF_OPEN"
            else:
                raise Exception("Mach dang OPEN")
            
        try:
            result = func(*args, **kwargs)
             
            if self.state == "HALF_OPEN":
                print("Service hoi phuc. CLOSED")
            
            self.state = "CLOSED"
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                print(f"Loi lan thu {self.failure_count}. OPEN")
                self.state = "OPEN"
            
            raise e


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
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=5)

    def unstable_api():
        raise Exception("Server Error 500")
    
    for i in range(1,11):
        print(f"\n--- Lan goi thu {i} ---")
        try:
            cb.call(unstable_api)
        except Exception as e:
            print(e)
        if i == 5:
            print("... Đang đợi 6 giây cho service hồi phục ...")
            time.sleep(6)
    


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
        self.ttl_seconds = ttl_seconds
        self.cache = {} 

    
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
        if url in self.cache:
            response, timestamp = self.cache[url]
            if time.time() - timestamp < self.ttl_seconds:
                return response
            else:
                del self.cache[url]
        
        return None


    def set(self, url, response):
        """
        TODO: Implement set method
        1. Lưu response và current timestamp vào cache
        """
        self.cache[url] = (response, time.time())


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
    url = "https://jsonplaceholder.typicode.com/posts/1"
    cache = SimpleCache(ttl_seconds=10)
    print("Lan 1:")
    cache_response = cache.get(url)
    if cache_response is None:
        response = requests.get(url)
        cache.set(url,response)
        print(f"From API: {response.status_code} - {response.json()}")
    else:
        print(f"From Cache: {cache_response.status_code} - {cache_response.json()}")

    print("\nLần gọi 2:")
    cached_response = cache.get(url)
    if cached_response is None:
        response = requests.get(url)
        cache.set(url, response)
        print(f"From API: {response.status_code} - {response.json()}")
    else:
        print(f"From Cache: {cached_response.status_code} - {cached_response.json()}")

    # 4. Đợi 11 seconds
    print("\nĐang đợi 11 giây để TTL hết hạn...")
    time.sleep(11)
    
    # 5. Gọi API lần 3 (cache hết hạn, nên hit API server lại)
    print("\nLần gọi 3:")
    cached_response = cache.get(url)
    if cached_response is None:
        response = requests.get(url)
        cache.set(url, response)
        print(f"From API: {response.status_code} - {response.json()}")
    else:
        print(f"From Cache: {cached_response.status_code} - {cached_response.json()}") 

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
        self.capacity = requests_per_second
        self.tokens = requests_per_second
        self.last_refill_time = time.time()
    
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
        current_time = time.time() 
        elapsed_time = current_time - self.last_refill_time
        new_tokens = elapsed_time  * self.capacity
        self.tokens = min(self.tokens + new_tokens, self.capacity)
        self.last_refill_time = current_time

        if self.tokens > 0: 
            self.tokens -= 1
            return True
        return False


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
    limiter = RateLimiter(requests_per_second=2)

    for i in range(5):
        if limiter.allow_request():
            print(f"Request {i+1}: Request allowed")
        else:
            print(f"Request {i+1}: Rate limit exceeded, wait...")
        time.sleep(0.3)


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
        self.base_url = base_url 
        self.cache = SimpleCache(ttl_seconds=cache_ttl)
        self.cb = CircuitBreaker()
        self.rate_limiter = RateLimiter(requests_per_second=rate_limit)
    
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
        url = self.base_url + endpoint
        if not self.rate_limiter.allow_request():
            raise Exception("Rate limit exceeded")

        cached_response = self.cache.get(url)
        if cached_response:
            print(f"Cache hit for {url}")
            return cached_response
        
        # Gọi API qua circuit breaker
        response = self.cb.call(requests.get, url)
        self.cache.set(url, response)
        print(f"API call for {url}")
        return response




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
    url = "https://jsonplaceholder.typicode.com"
    rac = RobustAPIClient(base_url=url)
    for i in range(3):
        print(f"\n--- Call {i+1} ---")
        response = rac.get("/posts/1")
        print(f"Status: {response.status_code}")


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
