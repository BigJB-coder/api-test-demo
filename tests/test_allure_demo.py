import allure
import requests

ALLURE_BASE = "http://httpbin.org"


@allure.feature("复读机餐馆")        # 相册的"章节名"
@allure.title("测试 /get 窗口是否活着")   # 照片的中文名字
def test_get_alive():
    with allure.step("请求 /get 接口"):        # 步骤 1（点开能展开）
        resp = requests.get(f"{ALLURE_BASE}/get")
    with allure.step("检查返回状态码是 200"):  # 步骤 2
        assert resp.status_code == 200


@allure.feature("复读机餐馆")
@allure.title("测试 /status/404 窗口假装没有")
def test_status_404():
    with allure.step("请求 /status/404 接口"):
        resp = requests.get(f"{ALLURE_BASE}/status/404", allow_redirects=False)
    with allure.step("检查状态码是 404"):
        assert resp.status_code == 404