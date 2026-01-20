# 快速入门

## 1. 环境准备
- Python >= 3.8
- 推荐使用虚拟环境

## 2. 安装依赖
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

说明：Allure CLI 需单独安装（不支持通过 pip 安装）。本地安装完成后在虚拟环境内可直接使用 `allure` 命令。

## 3. 运行测试
```bash
pytest -q
```

## 4. 运行配置用例（CLI）
```bash
api-test-hub run -c src/api_test_hub/data/example.yaml
```

## 4.1 运行配置用例并生成 Allure HTML（默认）
```bash
api-test-hub run -c src/api_test_hub/data/example.yaml
```

如需跳过 Allure：
```bash
api-test-hub run -c src/api_test_hub/data/example.yaml --no-allure
```

## 4.2 缓存响应字段（extract）
在用例中增加 `extract`，缓存字段或完整 JSON，后续用例可用 `${var}` 引用。

```yaml
cases:
  - name: get_user
    method: GET
    path: /users/42
    extract:
      user_id: body.id
      user_body: body
```

## 5. 生成 pytest 用例文件
```bash
api-test-hub generate -c src/api_test_hub/data/example.yaml -o cases/test_generated.py
```

## 6. 生成 Allure 报告
```bash
pytest --alluredir reports/allure-results
allure serve reports/allure-results
```

如果提示 `allure CLI not found`，需要先安装 Allure CLI。

## 7. 初始化模板项目
```bash
api-test-hub init -o ./api-test-template
```
