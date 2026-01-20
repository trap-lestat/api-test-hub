# 发布流程

## 1. 版本号规范
- 主版本号：不兼容变更
- 次版本号：向后兼容新功能
- 修订号：向后兼容问题修复

## 2. 发布步骤
1. 更新 `src/api_test_hub/__init__.py` 的 `__version__`
2. 更新 `CHANGELOG.md`
3. 运行测试：`pytest -q`
4. 创建发布标签：`git tag vX.Y.Z`
5. 推送标签：`git push origin vX.Y.Z`
6. 归档发布产物（Allure 报告、构建日志）

## 3. 发布说明模板
- 版本：vX.Y.Z
- 时间：YYYY-MM-DD
- 变更概述：
- 风险与回滚策略：
