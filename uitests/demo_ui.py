"""可视化演示：让浏览器窗口弹出来，亲眼看到机器人怎么操作页面。

用法：python demo_ui.py （在 uitests 目录下）
"""
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAGES = Path(__file__).parent / "pages"
FORM_URI = PAGES.joinpath("demo_form.html").as_uri()

with sync_playwright() as p:
    # headless=False = 弹出真实浏览器窗口，让你看着它动
    browser = p.chromium.launch(channel="chrome", headless=False)
    page = browser.new_page()

    print("① 正在打开练习页……")
    page.goto(FORM_URI)
    time.sleep(2)

    print("② 在『姓名』框里输入：吴晓为")
    page.get_by_label("姓名").fill("吴晓为")
    time.sleep(1.5)

    print("③ 在『邮箱』框里输入，并在下拉里选『广州』，勾选同意")
    page.get_by_label("邮箱").fill("xw@test.com")
    page.get_by_label("意向城市").select_option("广州")
    page.get_by_label("我同意接收招聘信息").check()
    time.sleep(1.5)

    print("④ 点击『提交』按钮……")
    page.get_by_role("button", name="提交").click()
    time.sleep(1.5)

    result = page.locator("#result").inner_text()
    print(f"⑤ 页面上显示的结果：{result}")
    print("⑥ 浏览器马上自动关闭（这是机器人关的，不是你自己点）")
    time.sleep(2)
    browser.close()
    print("演示结束！浏览器已自动关闭。")