"""第3课：真实网站实战——saucedemo 登录流程。

saucedemo.com 是全世界测试员练手的老牌免费练习站，密码用户名都是公开的：
  standard_user     / secret_sauce   正常用户
  locked_out_user   / secret_sauce   被锁定的用户（登录会被拒绝）

这一课要学真实网站的三样东西：
  1. 登录表单定位（用户名/密码框、登录按钮）
  2. 点击登录后"页面跳转"的等待
  3. 错误提示的断言（登录失败时网站会显示红字）
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from common import launch_kwargs

# 练习站地址（真实网站！不再是本地文件）
BASE = "https://www.saucedemo.com/"


def test_login_success():
    """正常用户能登录成功 → 页面跳转到商品页（看到 Products 标题）。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs())
        page = browser.new_page()
        page.goto(BASE)

        # ① 填登录表单（真实网站的 input 没有 label，用 placeholder 定位）
        page.get_by_placeholder("Username").fill("standard_user")
        page.get_by_placeholder("Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()

        # ② 等待跳转：登录成功后页面出现商品页标题 "Products"（最多等 10 秒）
        page.get_by_text("Products").wait_for(timeout=10000)

        # ③ 断言：不但在页面上，连网址都变成了商品页
        assert "/inventory.html" in page.url
        browser.close()


def test_login_locked_out():
    """被锁定的用户登录 → 页面显示错误红字，不跳转。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs())
        page = browser.new_page()
        page.goto(BASE)

        page.get_by_placeholder("Username").fill("locked_out_user")
        page.get_by_placeholder("Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()

        # 断言：出现错误提示（包含 "locked out"），且网址还停在登录页
        page.get_by_text("locked out").wait_for(timeout=10000)
        assert "inventory.html" not in page.url
        browser.close()