"""UI 测试公共配置：浏览器启动参数。

本地跑：用你电脑上的 Chrome（channel="chrome"，免下载）
CI 跑：GitHub Action 里没有 Chrome，改用 Playwright 自带浏览器
      （ci.yml 会设置环境变量 PW_BUNDLED_CHROMIUM=1，并提前安装浏览器）
"""
import os
from pathlib import Path

# 练习页目录（本地 file:// 页面）
PAGES = Path(__file__).parent / "pages"


def launch_kwargs():
    """返回浏览器启动参数：本地用 Chrome，CI 用自带浏览器。"""
    if os.getenv("PW_BUNDLED_CHROMIUM"):
        return {}          # 不指定 channel → Playwright 自带浏览器
    return {"channel": "chrome"}   # 本地 → 系统 Chrome