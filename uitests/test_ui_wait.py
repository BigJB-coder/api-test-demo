"""第2课：等待——页面变慢怎么办（真实网站必踩的坑）。

为什么会有"等待问题"：
  真实网站点按钮后要请求服务器，1 到几秒后才把结果渲染出来。
  如果你的代码"不等"就去找结果 → 像去空桌子上拿菜 → 报错。

Playwright 的两个救命工具：
  1. 自动等待：fill/click 等操作自带"等到能做为止"（很多情况不用你操心）
  2. 显式等待：page.locator(...).wait_for(timeout=10000)
     → "我要的这个元素，等你（最多10秒）出现"
"""
from pathlib import Path

from playwright.sync_api import sync_playwright
from common import launch_kwargs

PAGES = Path(__file__).parent / "pages"
ASYNC_URI = PAGES.joinpath("demo_async.html").as_uri()


def test_wait_async_result():
    """点按钮 → 2 秒后才有结果 → 用 wait_for 等它出现再断言。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs())
        page = browser.new_page()
        page.goto(ASYNC_URI)

        page.get_by_role("button", name="开始加载").click()

        # 关键一行：等"加载完成"这几个字出现（最多等 10 秒）
        # 注意：不能 wait_for #result——它一直存在，等的是"内容"
        page.get_by_text("加载完成").wait_for(timeout=10000)

        assert "加载完成" in page.locator("#result").inner_text()
        browser.close()


def test_placeholder_and_result():
    """进阶定位：get_by_placeholder 按"提示文字"找输入框。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs())
        page = browser.new_page()
        page.goto(ASYNC_URI)

        # 输入框里写着灰色提示"输入你的大名"，就靠它找到这个框
        page.get_by_placeholder("输入你的大名").fill("测试员")
        page.get_by_role("button", name="开始加载").click()
        page.get_by_text("加载完成").wait_for(timeout=10000)

        assert "测试员" in page.locator("#result").inner_text()
        browser.close()