"""第1课：第一个 UI 自动化用例。

被测对象：本地练习页（uitests/pages/demo_form.html）
—— 自己造的网页，零网络、零反爬，专心学"怎么让机器人操作页面"。

对比一下你已经会的接口测试：
  接口测试 = 机器人直接找网站后台"要数据"（requests）
  UI 测试  = 机器人打开真实页面，像人一样"点击填写"（playwright）
"""
from pathlib import Path

from playwright.sync_api import sync_playwright
from common import launch_kwargs

# 练习页的"网址"（本地文件，用 file:// 方式打开）
PAGES = Path(__file__).parent / "pages"
FORM_URI = PAGES.joinpath("demo_form.html").as_uri()


def test_form_submit():
    """填表 → 提交 → 检查页面显示的提交结果。

    整段代码就是三件事：打开页面（goto）→ 操作（填/选/点）→ 断言（查结果）。
    """
    with sync_playwright() as p:
        # 用你电脑上的 Chrome 打开浏览器（channel="chrome" 免下载）
        browser = p.chromium.launch(**launch_kwargs())
        page = browser.new_page()

        # ① 打开练习页（相当于在地址栏输入网址回车）
        page.goto(FORM_URI)

        # ② 像个真人一样操作：
        page.get_by_label("姓名").fill("吴晓为")                # 在"姓名"框里打字
        page.get_by_label("邮箱").fill("xw@test.com")          # 在"邮箱"框里打字
        page.get_by_label("意向城市").select_option("广州")     # 下拉选"广州"
        page.get_by_label("我同意接收招聘信息").check()          # 勾选同意
        page.get_by_role("button", name="提交").click()        # 点"提交"按钮

        # ③ 断言：页面上的 #result 区域显示了我们预期的那句话
        assert "提交成功：吴晓为，广州，同意=true" in page.locator("#result").inner_text()

        browser.close()


def test_form_required_check():
    """不勾"同意"，页面也会显示提交结果里 同意=false —— 验证勾选状态被记录。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs())
        page = browser.new_page()
        page.goto(FORM_URI)
        page.get_by_label("姓名").fill("小明")
        page.get_by_label("意向城市").select_option("上海")
        page.get_by_role("button", name="提交").click()
        assert "提交成功：小明，上海，同意=false" in page.locator("#result").inner_text()
        browser.close()