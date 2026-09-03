"""第7课：场景套件——用参数化把用例批量扩容到 50+。

全部基于 httpbin.org 的窗口接口，每条断言都有明确意义：
1) 状态码家族（正常/重定向/客户端错误/服务端错误）
2) HTTP 方法家族（GET/POST/PUT/PATCH/DELETE/OPTIONS 都能用）
3) base64 编解码（md 编码的文本，接口解码后原样返回）
4) 自定义响应头（让接口回什么头，就回什么头）
5) Cookie 设置与回显
6) GET 参数组合回显
7) 编码探测
"""
import base64
import pytest
import requests

BASE_URL = "http://httpbin.org"

# 1) 状态码家族：覆盖 2xx 正常 / 3xx 重定向 / 4xx 客户端错误 / 5xx 服务端错误
STATUS_CODES = [
    200, 201, 202, 204,
    301, 302, 304, 307, 308,
    400, 401, 403, 404, 405, 406, 409, 410, 415, 418, 429,
    500, 501, 502, 503,
]

@pytest.mark.parametrize("code", STATUS_CODES)
def test_status_code_family(code):
    """任何状态码都要原样返回（重定向不自动跟随，才能拿到真的 3xx）。"""
    resp = requests.get(f"{BASE_URL}/status/{code}", allow_redirects=False)
    assert resp.status_code == code


# 2) HTTP 方法家族
METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

@pytest.mark.parametrize("method", METHODS)
def test_http_methods(method):
    """/anything 窗口会回显你用的方法名——发什么方法，就必须回什么方法。"""
    resp = requests.request(method, f"{BASE_URL}/anything")
    assert resp.status_code == 200
    if method in ("GET", "POST", "PUT", "PATCH", "DELETE"):
        # 这些方法响应体是 JSON，可以对比回显的方法名
        assert resp.json()["method"] == method
    # OPTIONS 的响应体不是 JSON，只验证能正常应答即可


# 3) base64 编解码：先本地编码，再让接口解码，必须一致
# httpbin 用标准 base64 解码：需要保留 = 填充；样例避免编码后带 / 的文本
BASE64_SAMPLES = ["hello", "12345", "hello world!", "接口测试"]

@pytest.mark.parametrize("text", BASE64_SAMPLES)
def test_base64_decode(text):
    encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    resp = requests.get(f"{BASE_URL}/base64/{encoded}")
    assert resp.text == text


# 4) 自定义响应头：参数设置什么头，响应里就必须带什么头
CUSTOM_HEADERS = [
    {"X-Custom-1": "value-a"},
    {"X-Custom-2": "value-b"},
]

@pytest.mark.parametrize("h", CUSTOM_HEADERS)
def test_response_headers(h):
    resp = requests.get(f"{BASE_URL}/response-headers", params=h)
    assert resp.status_code == 200
    for key, value in h.items():
        assert resp.headers.get(key) == value


# 5) Cookie：设置之后，回显的 cookie 表里必须有
@pytest.mark.parametrize("name,value", [
    ("session_id", "abc123"),
    ("lang", "zh-CN"),
])
def test_cookies(name, value):
    resp = requests.get(f"{BASE_URL}/cookies/set/{name}/{value}")
    data = resp.json()
    assert data.get("cookies", {}).get(name) == value


# 6) GET 参数组合回显
PARAM_CASES = [
    {"page": 1, "size": 20},
    {"q": "python", "sort": "desc"},
    {"empty": ""},
]

@pytest.mark.parametrize("p", PARAM_CASES)
def test_get_echo(p):
    resp = requests.get(f"{BASE_URL}/get", params=p)
    data = resp.json()
    assert resp.status_code == 200
    for key, value in p.items():
        assert data["args"][key] == str(value)


# 7) 编码探测
def test_encoding_utf8():
    resp = requests.get(f"{BASE_URL}/encoding/utf8")
    assert resp.status_code == 200
    assert "utf-8" in resp.headers.get("content-type", "").lower()