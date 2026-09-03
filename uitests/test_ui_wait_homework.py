"""第2课作业：等待 + 定位练习"""
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGES = Path(__file__).parent / "pages"
ASYNC_URI = PAGES.joinpath("demo_async.html").as_uri()

MY_NAME = "牛逼"   # ← 改成你自己的（比如"阿伟"）


def test_hw1_async_load():
    """抄示例：点按钮 → 等"加载完成" → 断言带自己的昵称。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page()
        page.goto(ASYNC_URI)

        page.get_by_placeholder("输入你的大名").fill(MY_NAME)  # 用提示文字定位输入框
        page.get_by_role("button", name="开始加载").click()
        page.get_by_text("加载完成").wait_for(timeout=10000)   # 等新内容出现

        assert MY_NAME in page.locator("#result").inner_text()  # 结果里带你的昵称
        browser.close()


def test_hw2_before_after():
    """加载前显示占位文字，加载后被替换——一次测两个状态。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page()
        page.goto(ASYNC_URI)

        # 状态1：还没点按钮 → 占位文字还"看得见"
        assert page.get_by_text("（还没有内容）").is_visible()

        page.get_by_role("button", name="开始加载").click()
        page.get_by_text("加载完成").wait_for(timeout=10000)

        # 状态2：加载完成后 → 占位文字被替换，已经"看不见"了
        assert not page.get_by_text("（还没有内容）").is_visible()
        browser.close()