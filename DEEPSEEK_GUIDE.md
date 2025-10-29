# DeepSeek API 配置指南

## 为什么推荐使用DeepSeek？

DeepSeek是一个性价比极高的国产大模型，特别适合用于C++作业评价系统：

### 优势对比

| 特性 | DeepSeek | GPT-4 | GPT-3.5 | Claude |
|------|----------|-------|---------|--------|
| **价格** | ￥1/百万tokens | ￥60-120/百万tokens | ￥7-15/百万tokens | ￥15-75/百万tokens |
| **代码能力** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **国内访问** | ✅ 稳定 | ❌ 需要特殊网络 | ❌ 需要特殊网络 | ❌ 需要特殊网络 |
| **响应速度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **中文支持** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

### 成本估算示例

假设评价50个学生的作业，每份代码平均100行：

- **DeepSeek**: 约 ￥0.5-1元
- **GPT-3.5**: 约 ￥3-5元
- **GPT-4**: 约 ￥30-50元
- **Claude**: 约 ￥8-15元

## 快速配置步骤

### 1. 注册DeepSeek账号

访问 [https://platform.deepseek.com/](https://platform.deepseek.com/)

1. 点击"注册"或"登录"
2. 使用手机号或邮箱注册
3. 完成实名认证（如需要）

### 2. 获取API密钥

1. 登录后进入控制台
2. 点击"API Keys"
3. 点击"创建新的API Key"
4. 复制生成的API密钥（格式类似：`sk-xxxxxxxxxxxxx`）

### 3. 配置项目

编辑项目根目录的 `.env` 文件：

```bash
# DeepSeek配置
API_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-你的API密钥
DEEPSEEK_MODEL=deepseek-chat
```

### 4. 充值（如需要）

1. 首次注册通常有免费额度
2. 如需充值，进入"充值"页面
3. 最低充值金额通常为￥10-50元
4. 支持支付宝、微信支付等

## 使用示例

### 基本使用

```bash
# 使用DeepSeek评价作业
python src/main.py data/第02周上机作业.zip --provider deepseek
```

### 在代码中使用

```python
from src.llm_evaluator import get_evaluator

# 创建DeepSeek评价器
evaluator = get_evaluator(provider='deepseek')

# 评价代码
evaluation = evaluator.evaluate(prompt)
print(evaluation)
```

## 支持的模型

DeepSeek目前提供以下模型：

| 模型名称 | 说明 | 适用场景 |
|---------|------|----------|
| `deepseek-chat` | 通用对话模型 | 推荐用于作业评价 |
| `deepseek-coder` | 代码专用模型 | 更强的代码理解能力 |

### 切换模型

修改 `.env` 文件：

```bash
# 使用代码专用模型
DEEPSEEK_MODEL=deepseek-coder
```

或在命令行指定：

```python
evaluator = get_evaluator(provider='deepseek', model='deepseek-coder')
```

## 常见问题

### Q1: API调用失败，返回401错误

**原因**: API密钥无效或已过期

**解决方案**:
1. 检查 `.env` 文件中的API密钥是否正确
2. 确认密钥以 `sk-` 开头
3. 登录控制台查看密钥是否被禁用
4. 重新生成新的API密钥

### Q2: 余额不足

**原因**: 账户余额为0或不足

**解决方案**:
1. 登录控制台查看余额
2. 进行充值
3. 首次注册用户检查是否有免费额度

### Q3: 请求超时或网络错误

**原因**: 网络连接问题

**解决方案**:
1. 检查网络连接
2. DeepSeek在国内可直接访问，无需特殊网络
3. 尝试重新运行

### Q4: 返回结果质量不佳

**解决方案**:
1. 尝试使用 `deepseek-coder` 模型（代码专用）
2. 优化 `config/prompts.py` 中的提示词
3. 调整temperature参数（在 `src/llm_evaluator.py` 中）

### Q5: 批量处理时速度慢

**原因**: API调用是串行的

**解决方案**:
1. DeepSeek响应速度已经很快
2. 可以考虑实现并发调用（需修改代码）
3. 或分批次处理

## API限制

- **速率限制**: 通常为 60次/分钟（具体以官方为准）
- **单次请求token限制**: 32K tokens
- **并发请求**: 根据账户等级而定

## 技术支持

- **官方文档**: [https://platform.deepseek.com/docs](https://platform.deepseek.com/docs)
- **API文档**: [https://platform.deepseek.com/api-docs](https://platform.deepseek.com/api-docs)
- **问题反馈**: 通过控制台联系客服

## 对比其他API

### 何时使用DeepSeek？

✅ **推荐使用DeepSeek**:
- 预算有限，需要控制成本
- 批量处理大量作业
- 在国内使用，需要稳定访问
- 代码评价为主要任务

### 何时考虑其他API？

考虑 **GPT-4**:
- 预算充足，追求最佳质量
- 需要复杂的推理能力

考虑 **Claude**:
- 需要长文本处理
- 对安全性有特殊要求

考虑 **GPT-3.5**:
- 需要OpenAI生态
- 平衡成本和质量

## 最佳实践

1. **先小规模测试**: 用几份作业测试效果和成本
2. **监控用量**: 定期检查API调用统计
3. **优化提示词**: 根据评价效果调整prompts
4. **设置预算提醒**: 在控制台设置余额告警
5. **保存评价结果**: 避免重复调用API

## 总结

DeepSeek是目前最适合C++作业评价系统的大模型选择：
- 💰 成本低廉，适合教育场景
- 🚀 代码能力强，评价准确
- 🇨🇳 国内访问稳定
- ⚡ 响应快速，体验好

立即访问 [https://platform.deepseek.com/](https://platform.deepseek.com/) 开始使用！
