# 开发规范

## 1. 代码规范
- Python >= 3.8
- 遵循 PEP8，使用 black + isort + flake8
- 函数/类命名：snake_case / PascalCase
- 单一职责原则，模块职责清晰

## 2. 目录规范
- core：核心能力（请求、断言、运行器）
- config：配置加载与校验
- data：测试数据与环境
- cases：生成的测试用例
- reports：Allure 报告输出
- utils：通用工具
- tests：框架自身单元测试

## 3. 文档规范
- README：快速上手与常用命令
- docs：设计文档与示例
- 变更记录：CHANGELOG

## 4. 配置规范
- 配置文件必须带版本号（version）
- 环境配置与用例配置分离
- 必须支持变量引用（${var}）
- 支持用例级响应缓存（extract）
