"""第4课：参数化 UI 用例——一条用例覆盖多个账号 + 报告里带截图。

saucedemo 有多个公开测试账号，登录后都应进入商品页：
  standard_user / problem_user / performance_glitch_user / error_user
参数化：一个函数，pytest 自动展开成 4 条用例（报错直接点名是哪个账号）。
Allure：页面截图塞进测试报告，看报告=看现场。
"""
import allure
import pytest
from playwright.sync_api import sync_playwright

from common import launch_kwargs

BASE = "https://www.saucedemo.com/"

# 能正常登录的账号（locked_out_user 登录会被拒，故意不放进来）
LOGIN_USERS = [
    "standard_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
]


@pytest.mark.parametrize("username", LOGIN_USERS)
def test_login_ok(username):
    """每个账号都能登录成功，进入商品页；截图留档到 Allure 报告。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs())
        page = browser.new_page()
        # ① 进入登录页
        page.goto(BASE)
        play_ok = False
        try:
            # ② 用参数化给的账号登录
            page.get_by_placeholder("Username").fill(username)
            page.get_by_placeholder("Password").fill("secret_sauce")
            page.get_by_role("button", name="Login").click()
            # ③ 等商品页出现（performance_glitch_user 加载偏慢，给足 15 秒）
            page.get_by_text("Products").wait_for(timeout=15000)
            # ④ 断言 + 截图留档
            assert "inventory.html" in page.url
            play_ok = True
        finally:
            allure.attach(
                page.screenshot(),
                name=f"{username} 登录{'成功' if play_ok else '失败'}",
                attachment_type=allure.attachment_type.PNG,
            )
            browser.close()