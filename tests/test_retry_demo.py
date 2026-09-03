"""第5课：重试 + 断言现场信息 演示用例。

这个用例经历过"故意失败"的教学演示（断言 500），
现在断言已修正为真实结果（200），让 CI 全绿。
"""
import requests


def test_deliberate_fail(base_url):
    """验证 /get 接口正常返回 200；失败时输出现场信息（状态码）。"""
    resp = requests.get(f"{base_url}/get")
    assert resp.status_code == 200, f"看！失败了还能看到现场：状态码={resp.status_code}"