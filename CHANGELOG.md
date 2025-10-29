# 更新日志

## v1.1.0 (2024) - 新增DeepSeek支持

### 🆕 新增功能
- **DeepSeek API支持**：新增对DeepSeek大模型的支持
  - 性价比极高（比GPT-4便宜10-20倍）
  - 代码能力强，特别适合C++作业评价
  - 国内访问稳定，无需特殊网络环境
  - 响应速度快

### 📝 文档更新
- 新增 `DEEPSEEK_GUIDE.md`：DeepSeek API详细配置指南
- 更新 `README.md`：添加DeepSeek使用说明
- 更新 `QUICKSTART.md`：推荐使用DeepSeek
- 更新 `.env.example`：添加DeepSeek配置示例

### 🔧 代码优化
- `src/llm_evaluator.py`：添加 `DeepSeekEvaluator` 类
- `src/main.py`：命令行参数支持deepseek选项
- 新增 `test_api.py`：API配置测试工具

### 📊 支持的API提供商
- ✅ DeepSeek（推荐）
- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ Anthropic Claude
- ✅ 阿里云通义千问

### 🎯 最佳实践建议
- 首选DeepSeek：适合预算有限、批量处理的场景
- GPT-4：追求最佳质量但成本较高
- GPT-3.5：平衡成本和质量
- Claude：长文本处理优势

---

## v1.0.0 (2024) - 首次发布

### ✨ 核心功能
- ZIP文件自动解压和扫描
- 智能识别学生姓名
- 支持多种C++文件格式（.cpp, .cc, .h等）
- 大模型API集成（OpenAI、Claude、通义千问）
- 自定义评价提示词
- 生成Markdown格式的评价报告
- 导出Excel汇总表格
- JSON格式数据导出

### 📦 项目结构
- 模块化设计，易于维护和扩展
- 完整的配置文件系统
- 详细的使用文档

### 🛠️ 开发工具
- 快速启动脚本（run.sh / run.bat）
- 环境变量配置（.env）
- Git忽略文件配置

### 📚 文档
- README.md：完整使用文档
- QUICKSTART.md：快速开始指南
- data/README.md：数据文件组织说明

---

## 路线图

### 未来计划
- [ ] 支持更多编程语言（Python, Java等）
- [ ] Web界面支持
- [ ] 批量并发处理
- [ ] 自定义评分标准
- [ ] 历史记录管理
- [ ] 学生作业对比功能
- [ ] 代码相似度检测
- [ ] 邮件自动发送功能
- [ ] 更多本地大模型支持

### 欢迎贡献
如果你有好的想法或发现了bug，欢迎提Issue或Pull Request！
