# Mock 服务

## 启动
```bash
python examples/mock_server/server.py
```

## 可用接口
- `GET /users/{id}`
- `POST /submit`
- `GET /hello`

## 示例配置
- 配置文件：`examples/mock_server/sample.yaml`
- 需要设置环境变量 `MOCK_BASE_URL`，例如：
```bash
export MOCK_BASE_URL=http://127.0.0.1:8000
```
