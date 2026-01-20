# 设计方案

## 1. 核心模块设计
- ConfigLoader：加载并解析 YAML/JSON
- RequestClient：封装 HTTP 请求
- CaseBuilder：根据配置生成 pytest 参数
- AssertEngine：断言执行器
- Reporter：Allure 结果输出

## 2. 测试用例配置结构（示例）
```yaml
version: 1
name: user_api
base_url: https://api.example.com
cases:
  - name: get_user
    method: GET
    path: /users/${user_id}
    extract:
      cached_id: body.id
      cached_body: body
    params:
      verbose: true
    validate:
      - eq: [status_code, 200]
      - contains: [body.name, "lei"]
```

## 2.1 项目级配置结构（示例）
```yaml
version: 1
name: demo_project
base_url: http://127.0.0.1:8000
cases_dir: cases
variables:
  user_id: 42
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

## 2.2 项目用例文件结构（示例）
```yaml
version: 1
cases:
  - name: health_check
    method: GET
    path: /hello
```

## 2.3 数据库校验结构（示例）
```yaml
db:
  default:
    type: sqlite
    path: /tmp/demo.db
```

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
## 3. 运行流程
1. 读取配置与环境变量
2. 生成测试用例集合
3. pytest 执行
4. Allure 输出报告

## 4. 关键扩展点
- 新的断言类型
- 支持不同协议（HTTP/GraphQL）
- 支持数据库校验与 mock
