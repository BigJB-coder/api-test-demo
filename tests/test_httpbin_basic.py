"""第一课：第一个接口测试用例。

先打个比方，把"接口测试"变成你熟悉的事：
----------------------------------------
把 httpbin.org 当成一家【复读机餐馆】——
你点什么，它就重复什么，绝对不骗你。

你问它："我要一份 page=2"（在浏览器打开 httpbin.org/get?page=2）
它就会回你一串数据，里面"url"那一行写着：
    http://httpbin.org/get?page=2   ← 它把你的点单原样重复了一遍

接口测试 = 让程序替你去问它，然后核对：
    它回的话对不对 → 对就 PASS（通过），不对就 FAIL（失败）
----------------------------------------
"""
import requests

# 这家"餐馆"的地址。以后所有用例，都去这里问。
BASE_URL = "http://httpbin.org"


def test_get_returns_200():
    """用例1：问 /get 这个窗口——"你活着吗？能正常接单吗？"

    resp        = 网站"回话"的结果（打包好的一整包东西）
    status_code = 网站给的处理结果编号：
                   200 = 一切正常，办好了
                   404 = 对不起，没这回事
                   500 = 服务器自己出事了

    assert 就是把关的检查员：
      检查员说 "我要求是 200，不是就标红"，不满意的结果直接记为失败。
    """
    resp = requests.get(f"{BASE_URL}/get")
    assert resp.status_code == 200


def test_get_echoes_query_params():
    """用例2：我点了 page=2 和 size=10，你重复的话里必须能对得上。

    四步走：
      1. requests.get(地址, params={...})
            → 带着"点单参数"去问（params 就是点单的小纸条）
      2. resp.json()
            → 网站回的数据是 JSON 格式，这句话把它翻译成 Python 字典
              （字典 ≈ 带名字的表格，可以按名字查内容）
      3. data["url"]
            → 从表格里查"url"这一栏的值
      4. assert 一堆 ==
            → 检查员逐项核对：一模一样，才算通过
    """
    resp = requests.get(f"{BASE_URL}/get", params={"page": 2, "size": 10})
    data = resp.json()
    assert data["url"] == f"{BASE_URL}/get?page=2&size=10"
    assert data["args"]["page"] == "2"
    assert data["args"]["size"] == "10"