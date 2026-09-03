"""第4课作业：参数化"加购物车"+ Allure 截图。"""
import allure
import pytest
from playwright.sync_api import sync_playwright

from common import launch_kwargs

BASE = "https://www.saucedemo.com/"

# 要点击的商品顺序号（0-5 对应商品页上 6 个商品）
CART_INDEXES = [0, 1, 2, 3, 4]      # ← 作业1：加两个数，比如 [0, 2, 4, 5]


@pytest.mark.parametrize("idx", CART_INDEXES)
def test_add_to_cart(idx):
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs())
        page = browser.new_page()
        # 登录（照抄第3课）
        page.goto(BASE)
        page.get_by_placeholder("Username").fill("standard_user")
        page.get_by_placeholder("Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()
        page.get_by_text("Products").wait_for(timeout=10000)

        # 点第 idx 个 "Add to cart" 按钮
        page.get_by_role("button", name="Add to cart").nth(idx).click()
        # 购物车角标应显示数字 1
        assert page.locator(".shopping_cart_badge").inner_text() == "1"

        # 作业2：加一行 Allure 截图（截"加购后"页面）
        allure.attach(page.screenshot(),
                      name=f"加购第{idx}个商品后",
                      attachment_type=allure.attachment_type.PNG)
        browser.close()