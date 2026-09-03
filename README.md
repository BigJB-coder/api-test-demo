# API + UI 自动化测试框架（api-test-demo）

基于 Python + pytest + Playwright 的自动化测试框架，覆盖 **接口测试** 与 **UI 测试** 两个层面，
集成 **Allure 可视化测试报告**（UI 关键步骤自动截图）与 **GitHub Actions 定时回归**。

## 技术栈

- **接口层**：Python 3.13 · pytest · requests
- **UI 层**：Playwright（本地用系统 Chrome，CI 用自带浏览器）
- **报告**：Allure（allure-pytest）· 失败自动重试（pytest-rerunfailures）
- **CI**：GitHub Actions（代码推送触发 + 每日 09:00 UTC 定时回归）

## 功能特性

- **接口功能测试**：GET / POST、JSON 与表单提交、自定义 headers、参数化数据驱动
  （状态码家族、参数回显、HTTP 方法、base64 编解码等场景）
- **UI 自动化**：真实网站（SauceDemo）的登录 / 错误场景 / 加购流程，多账号参数化；
  本地练习页的表单、异步加载、定位练习
- **稳定性**：内容等待（wait_for）替代固定 sleep，失败用例自动重试 2 次
- **Allure 报告**：接口断言详情 + UI 步骤截图（看报告 = 看现场）
- **多环境切换**：接口层通过环境变量 `ENV` 切换 dev / test / prod
- **CI 定时回归**：每日 09:00（UTC）自动执行全量测试并生成报告

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 跑全部测试（接口 61 条 + UI 22 条 = 83 条）
python -m pytest

# 3. 生成并打开 Allure 报告（Windows 可直接运行 run_report.bat）
python -m pytest --alluredir=report/results
allure generate report/results -o report/html --clean
allure open report/html

# 4. 切换接口运行环境（默认 dev）
set ENV=test && python -m pytest tests
```

> UI 测试本地默认使用系统 Chrome（无需额外下载）；
> CI 中会自动安装 Playwright 自带浏览器并全量回归。

## 目录结构

```
api-test-demo/
├── .github/workflows/ci.yml   # CI：推送/每日定时回归 + 生成报告
├── tests/                     # 接口自动化（61 条用例）
│   ├── conftest.py            # 多环境 fixture（base_url）
│   ├── test_httpbin_basic.py  # GET 基础断言
│   ├── test_httpbin_more.py   # 状态码 / user-agent / IP
│   ├── test_post_submit.py    # POST、JSON/表单、headers
│   ├── test_parametrize.py    # 参数化（状态码家族、数字回显）
│   ├── test_allure_demo.py    # Allure 装饰器示例
│   ├── test_retry_demo.py     # 失败重试与断言现场信息
│   └── test_httpbin_suite.py  # 场景套件（参数化扩容）
├── uitests/                   # UI 自动化（22 条用例）
│   ├── common.py              # 浏览器启动参数（本地 Chrome / CI 自带）
│   ├── pages/                 # 本地练习页（表单 / 异步加载）
│   ├── test_ui_basic.py       # 表单提交、勾选状态
│   ├── test_ui_wait.py        # 内容等待、placeholder 定位
│   ├── test_sauce_login.py    # 真实网站登录成功/锁定场景
│   ├── test_sauce_param.py    # 多账号参数化 + Allure 截图
│   └── test_sauce_cart.py     # 加购流程参数化
├── pytest.ini                 # pytest 配置（重试、测试目录）
├── requirements.txt
└── run_report.bat             # Windows 一键生成并打开报告
```

## CI 状态

[![API Test CI](https://github.com/BigJB-coder/api-test-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/BigJB-coder/api-test-demo/actions)