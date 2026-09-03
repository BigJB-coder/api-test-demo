# API 自动化测试框架（api-test-demo）

基于 Python + pytest 的接口自动化测试框架，覆盖公共 API（httpbin.org）的功能、参数化、异常场景测试，
集成 **Allure 可视化测试报告** 与 **GitHub Actions 定时回归**。

## 技术栈

- Python 3.13 · pytest · requests
- Allure 测试报告（allure-pytest）
- pytest-rerunfailures 失败自动重试
- GitHub Actions：推送触发 + 每日定时回归

## 功能特性

- 接口功能测试：GET / POST、JSON 与表单提交、自定义 headers
- 参数化数据驱动：一条用例展开多组数据（状态码家族、回显校验等）
- 失败自动重试（2 次）＋ 断言现场信息（失败时附状态码与响应内容）
- 多环境切换：dev / test / prod，通过环境变量 `ENV` 控制
- Allure 可视化测试报告：章节、中文标题、步骤、失败现场
- CI 定时回归：每日 09:00（UTC）自动执行，结果生成报告

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 跑全部测试
python -m pytest

# 3. 跑测试并生成 Allure 原始数据
python -m pytest --alluredir=report/results

# 4. 生成并打开 Allure 网页报告（Windows 可运行 run_report.bat 一步完成）
allure generate report/results -o report/html --clean
allure open report/html

# 5. 切换运行环境（默认 dev）
set ENV=test && python -m pytest
```

## 目录结构

```
api-test-demo/
├── .github/workflows/ci.yml   # CI：推送/每日定时回归 + 生成报告
├── tests/
│   ├── conftest.py            # 多环境 fixture（base_url）
│   ├── test_httpbin_basic.py  # GET 基础断言
│   ├── test_httpbin_more.py   # 状态码 / user-agent / IP
│   ├── test_post_submit.py    # POST、JSON/表单、headers
│   ├── test_parametrize.py    # 参数化（状态码家族、数字回显）
│   ├── test_allure_demo.py    # Allure 装饰器示例（章节/标题/步骤）
│   ├── test_retry_demo.py     # 失败重试与断言现场信息
│   └── test_httpbin_suite.py  # 场景套件（参数化扩容）
├── pytest.ini                 # pytest 配置（重试、测试目录）
├── requirements.txt
└── run_report.bat             # Windows 一键生成并打开报告
```

## CI 状态

[![API Test CI](https://github.com/BigJB-coder/api-test-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/BigJB-coder/api-test-demo/actions)