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

## 4.1.1 按项目执行（文件夹为一个项目）
```bash
api-test-hub run -p projects/demo
```

项目配置示例（`project.yaml`）：
```yaml
version: 1
name: demo_project
base_url: http://127.0.0.1:8000
cases_dir: cases
```

用例文件示例（`cases/*.yaml`）只包含 cases，不再包含 base_url：
```yaml
version: 1
cases:
  - name: health_check
    method: GET
    path: /hello
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

## 4.3 扩展方法（随机数/时间戳/UUID）
配置中可使用扩展方法生成动态值：

```yaml
params:
  trace_id: ${uuid()}
  nonce: ${random_int(1000,9999)}
  ts: ${timestamp()}
```

如果希望缓存扩展方法结果供后续 case 使用，可用赋值语法：
```yaml
params:
  request_id: ${request_id=uuid()}
```

## 4.4 认证配置（Bearer Token / Cookie）
配置中支持认证信息，自动注入到请求头：

```yaml
auth:
  type: bearer
  token: ${access_token}
  login:
    method: POST
    path: /login
    json:
      username: demo
      password: secret
    extract:
      access_token: body.access_token
```

```yaml
auth:
  type: cookie
  cookies:
    session_id: ${session_id}
  login:
    method: POST
    path: /login
    json:
      username: demo
      password: secret
    extract:
      session_id: body.session_id
```

```yaml
auth:
  type: basic
  username: demo
  password: secret
```

## 4.5 用例文件级标签（一次配置，全用例生效）
在用例文件顶部配置元数据，自动作用到该文件内所有 case：

```yaml
version: 1
case_id: DEMO-001
epic: DemoUser
feature: 用户管理
story: 用户列表
severity: critical
cases:
  - name: 获取用户信息
    method: GET
    path: /api/v1/users
```

## 4.6 数据库校验（方案 A）
在项目配置里定义数据库连接，在用例中增加 `validate_db`：

```yaml
db:
  default:
    type: sqlite
    path: /tmp/demo.db
```

MySQL / Postgres 示例：
```yaml
db:
  default:
    type: mysql
    host: 127.0.0.1
    port: 3306
    user: demo
    password: demo
    database: demo_db
```

```yaml
db:
  default:
    type: postgres
    host: 127.0.0.1
    port: 5432
    user: demo
    password: demo
    database: demo_db
```

```yaml
validate_db:
  - name: user_count
    datasource: default
    sql: "select count(1) from users"
    assert:
      - eq: [body.value, 1]
```

也可以把查询结果缓存到上下文，供后续断言使用：
```yaml
validate_db:
  - name: latest_user
    datasource: default
    sql: "select username from users order by id desc limit 1"
    extract:
      db_user_name: value
validate:
  - eq: ["body.data.items[0].username", "${db_user_name}"]
```

支持的 `extract` 字段：
- `value`: 使用第一行第一列
- `rows`: 使用完整结果集（列表）

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
即使用例失败也会生成报告，默认输出在 `reports/allure-report`。
可使用：`allure open reports/allure-report/` 查看报告

## 7. 初始化模板项目
```bash
api-test-hub init -o ./projects/my_project
```
