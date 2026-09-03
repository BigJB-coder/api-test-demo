"""第3课作业：saucedemo 真实网站——两道题。

练习站说明：
  saucedemo.com 是全世界测试员练手的老牌免费练习站，账号是公开的：
    standard_user / secret_sauce    正常用户（能登录）
    密码填错时    → 页面显示红色错误提示 "Username and password do not match"

作业内容：
  1. 密码错误 → 登录被拒，断言出现错误提示、且网址没进商品页
  2. 正常登录 → 断言网址进入商品页、且能看到"Add to cart"按钮
"""
from playwright.sync_api import sync_playwright
from common import launch_kwargs

# 练习站地址（真实网站）
BASE = "https://www.saucedemo.com/"


def test_login_wrong_password():
    """题目1：密码填错 → 登录被拒，页面显示错误提示，不跳转商品页。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs())
        page = browser.new_page()
        page.goto(BASE)

        # ① 填登录表单：用户名对，密码故意填错
        page.get_by_placeholder("Username").fill("standard_user")
        page.get_by_placeholder("Password").fill("wrong_password")
        page.get_by_role("button", name="Login").click()

        # ② 等错误提示出现（密码错误时页面显示 "do not match" 红字）
        page.get_by_text("do not match").wait_for(timeout=10000)

        # ③ 断言：登录被拒 → 网址不能变成商品页
        assert "/inventory.html" not in page.url
        browser.close()


def test_login_cart():
    """题目2：正常登录 → 网址进入商品页，且能看到"Add to cart"按钮。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs())
        page = browser.new_page()
        page.goto(BASE)

        # ① 用标准账号正常登录
        page.get_by_placeholder("Username").fill("standard_user")
        page.get_by_placeholder("Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()

        # ② 等商品页标题 "Products" 出现（页面跳转完成）
        page.get_by_text("Products").wait_for(timeout=10000)

        # ③ 断言：登录成功 → 网址必须是商品页；页面上第一个"Add to cart"按钮可见
        assert "inventory.html" in page.url
        assert page.get_by_text("Add to cart").first.is_visible()
        browser.close()