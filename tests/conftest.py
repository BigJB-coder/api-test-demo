"""多环境配置：一套用例，随时换环境跑。

注意：本文件只放"公共设施"（fixture），不放测试用例。
pytest 不会收集 conftest.py 里的 test_ 函数——它是配置间，不是考场。
"""
import os
import pytest

# 环境地址表：一套用例，每个环境一个地址
ENVIRONMENTS = {
    "dev":  "http://httpbin.org",
    "test": "http://httpbin.org",
    "prod": "http://httpbin.org",   # 练习期三个都指同一个；真实项目各指各的
}

@pytest.fixture
def base_url():
    """根据环境变量 ENV 选环境，默认 dev——这就是'切换开关'。"""
    env = os.getenv("ENV", "dev")
    return ENVIRONMENTS[env]