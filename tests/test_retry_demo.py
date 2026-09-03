"""第5课：重试 + 断言现场信息 演示用例。

这个用例是"故意"失败的——用来亲眼看到两件事：
1. pytest 会悄悄重试 2 次（重试后还是失败才标红）
2. 失败时，报错里带着我们写的"现场说明"（状态码是多少）
"""
import requests


def test_deliberate_fail(base_url):
    """故意断言 500：httpbin 的 /get 永远返回 200，所以必然失败。"""
    resp = requests.get(f"{base_url}/get")
    assert resp.status_code == 500, f"看！失败了还能看到现场：状态码={resp.status_code}"