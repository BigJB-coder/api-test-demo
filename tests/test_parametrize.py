import requests
import pytest
# 这家"餐馆"的地址。以后所有用例，都去这里问。
BASE_URL = "http://httpbin.org"

# 这张"进货单"：列出所有要测的状态码
STATE_CODES = [200, 301, 404, 500]

@pytest.mark.parametrize("code", STATE_CODES)
def test_status_code(code):
    resp = requests.get(f"{BASE_URL}/status/{code}",allow_redirects=False)
    assert resp.status_code == code

NUMBER = [1, 98, 333, 1001]
@pytest.mark.parametrize("number", NUMBER)
def test_return_number(number):
    resp = requests.get(f"{BASE_URL}/get",params={"id":number})
    data = resp.json()
    assert data["args"]["id"] == str(number)