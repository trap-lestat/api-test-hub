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

## 3. 运行流程
1. 读取配置与环境变量
2. 生成测试用例集合
3. pytest 执行
4. Allure 输出报告

## 4. 关键扩展点
- 新的断言类型
- 支持不同协议（HTTP/GraphQL）
- 支持数据库校验与 mock
