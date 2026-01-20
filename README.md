# API Test Hub

API 自动化接口测试框架（脚手架）。

## 快速开始
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

说明：Allure CLI 需单独安装（不支持通过 pip 安装）。本地安装完成后在虚拟环境内可直接使用 `allure` 命令。

## 安装命令行
```bash
pip install -e .
api-test-hub generate -c src/api_test_hub/data/example.yaml -o cases/test_generated.py
```

## 初始化模板项目（CLI）
```bash
api-test-hub init -o ./api-test-template
```

## CLI 帮助与示例
- 自动生成文档：`doc/CLI_HELP.md`
- 生成命令：`python scripts/generate_cli_help.py`

## 生成 Allure 报告
```bash
pytest --alluredir reports/allure-results
allure serve reports/allure-results
```

## 运行配置驱动用例
```bash
python - <<'PY'
from api_test_hub.cases import load_cases
from api_test_hub.core import run_case
from api_test_hub.utils import configure_logging

config, _params = load_cases("src/api_test_hub/data/example.yaml")
logger = configure_logging("reports")
for case in config.cases:
    run_case(config.base_url, case, logger=logger)
PY
```

## 生成 pytest 用例文件（CLI）
```bash
python -m api_test_hub generate -c src/api_test_hub/data/example.yaml -o cases/test_generated.py
```

## 运行配置用例（CLI）
```bash
api-test-hub run -c src/api_test_hub/data/example.yaml
```

## 运行项目用例（CLI）
```bash
api-test-hub run -p examples/project_sample --no-allure
```

## 运行配置用例并生成 Allure HTML（默认）
```bash
api-test-hub run -c src/api_test_hub/data/example.yaml
```

如需跳过 Allure：
```bash
api-test-hub run -c src/api_test_hub/data/example.yaml --no-allure
```

## Mock 服务示例
```bash
python examples/mock_server/server.py
```

使用 `examples/mock_server/sample.yaml` 运行示例用例，需要设置：
```bash
export MOCK_BASE_URL=http://127.0.0.1:8000
```

## 日志输出
- 通过 `configure_logging` 生成日志文件（默认 `reports/api_test_hub.log`）
- 用例执行时可以把 logger 传给 `run_case` 记录请求与响应

## 目录结构
- src/api_test_hub: 框架源码
- tests: 框架自测
- reports: 报告输出目录
- examples: 示例配置

## 版本与变更记录
- 版本号：`src/api_test_hub/__init__.py`
- 变更记录：`CHANGELOG.md`

## 文档索引
- 快速入门：`doc/QUICKSTART.md`
- 开发计划：`doc/PLAN.md`
- 目标：`doc/GOALS.md`
- 规范：`doc/DEV_NORMS.md`
- 设计：`doc/DESIGN.md`
- 流程：`doc/PROCESS.md`
- 交付物：`doc/DELIVERABLES.md`
- 发布流程：`doc/RELEASE.md`
- CLI 帮助：`doc/CLI_HELP.md`
