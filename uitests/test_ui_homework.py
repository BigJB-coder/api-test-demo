from pathlib import Path
from playwright.sync_api import sync_playwright
from common import launch_kwargs

PAGES = Path(__file__).parent / "pages"
FORM_URI = PAGES.joinpath("demo_form.html").as_uri()

def test_hw1():
    with sync_playwright() as p:              # ← 固定写法：打开浏览器工厂
        browser = p.chromium.launch(**launch_kwargs())   # ← 打开 Chrome
        page = browser.new_page()                        # ← 新开一个标签页
        page.goto(FORM_URI)                              # ← ① 打开练习页

        # ② 操作区：在这一块写“点哪里、写什么”（看下面人话表）
        page.get_by_label("姓名").fill("小明")
        page.get_by_label("意向城市").select_option("广州")
        page.get_by_label("我同意接收招聘信息").check()
        page.get_by_role("button", name="提交").click()

        # ③ 断言区：检查页面显示的结果对不对
        assert "提交成功：小明，广州，同意=true" in page.locator("#result").inner_text()

        browser.close()                                  # ← 固定写法：关浏览器

def test_hw2():
    with sync_playwright() as p:              # ← 固定写法：打开浏览器工厂
        browser = p.chromium.launch(**launch_kwargs())   # ← 打开 Chrome
        page = browser.new_page()                        # ← 新开一个标签页
        page.goto(FORM_URI)                              # ← ① 打开练习页
        page.get_by_label("姓名").fill("狗蛋")
        page.get_by_label("邮箱").fill("abc")  # 填一个明显不是邮箱的东西
        page.get_by_role("button", name="提交").click()
        assert "提交成功" not in page.locator("#result").inner_text()  # 页面被拦住，没提交成功 → 通过
        browser.close()  # ← 固定写法：关浏览器

def test_hw3():
    with sync_playwright() as p:              # ← 固定写法：打开浏览器工厂
        browser = p.chromium.launch(**launch_kwargs())   # ← 打开 Chrome
        page = browser.new_page()                        # ← 新开一个标签页
        page.goto(FORM_URI)                              # ← ① 打开练习页
        page.get_by_role("button", name="提交").click()
        assert "提交成功" in page.locator("#result").inner_text()  # 页面被拦住，没提交成功 → 通过
        browser.close()  # ← 固定写法：关浏览器