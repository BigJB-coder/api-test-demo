import requests

# 这家"餐馆"的地址。以后所有用例，都去这里问。
BASE_URL = "http://httpbin.org"

def test_get_returns_404():
    resp = requests.get(f"{BASE_URL}/status/404")
    assert resp.status_code == 404

def test_get_user_agent():
    resp = requests.get(f"{BASE_URL}/user-agent")
    data = resp.json()
    assert "python-requests" in data['user-agent']

def test_get_ip():
    resp = requests.get(f"{BASE_URL}/ip")
    data = resp.json()
    assert data['origin']