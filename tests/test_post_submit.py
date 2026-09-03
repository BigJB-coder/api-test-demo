import requests

# 这家"餐馆"的地址。以后所有用例，都去这里问。
BASE_URL = "http://httpbin.org"

def test_post_json():
    resp = requests.post(f"{BASE_URL}/post",json={"name": "小红", "age": 20})
    data = resp.json()
    assert data["json"]["name"] == "小红"
    assert data["json"]["age"] == 20

def test_post_form():
    resp = requests.post(f"{BASE_URL}/post",data={"city":"深圳"})
    data = resp.json()
    assert data["form"]["city"] == "深圳"

def test_get_headers():
    resp = requests.get(f"{BASE_URL}/headers",headers={"X-Test-Token": "hello123"})
    data = resp.json()
    assert "X-Test-Token" in data["headers"]