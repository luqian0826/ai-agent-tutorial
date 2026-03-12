# AI Agent Tutorial 教程项目

基于《从零搭建你的第一个AI Agent：3天实现自动化工作流》教程的完整代码实现。

## 📁 项目结构

```
ai-agent-tutorial/
├── day1_agent.py              # Day 1: 第一个AI Agent
├── day2_tools.py              # Day 2: 网络搜索工具
├── day2_file_tools.py         # Day 2: 文件读写工具
├── day2_analysis_tools.py     # Day 2: 数据分析工具
├── day2_memory.py             # Day 2: 记忆系统
├── day2_memory_agent.py       # Day 2: 记忆增强Agent
├── day2_team.py               # Day 2: 多Agent团队
├── day2_competitor_analysis.py # Day 2: 竞品分析系统
├── day2_async.py              # Day 2: 异步处理
├── day2_cache.py              # Day 2: 缓存机制
├── requirements.txt           # Python依赖
├── .env.example               # 环境变量模板
└── README.md                  # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制模板
copy .env.example .env

# 编辑 .env 文件，设置你的 DeepSeek API 密钥
DEEPSEEK_API_KEY=your_api_key_here
```

获取API密钥：https://platform.deepseek.com/

### 3. 运行测试

每个文件都可以独立运行测试：

```bash
# Day 1 测试
python day1_agent.py

# Day 2 工具测试
python day2_tools.py
python day2_file_tools.py
python day2_analysis_tools.py
python day2_memory.py
python day2_memory_agent.py
python day2_team.py
python day2_competitor_analysis.py
python day2_async.py
python day2_cache.py
```

## 📋 功能说明

### Day 1: 基础Agent

**文件**: `day1_agent.py`

- ✅ 环境配置和模型初始化
- ✅ 基础工具（时间获取、文本总结）
- ✅ 对话交互功能

### Day 2: 功能扩展

#### 1. 网络搜索工具 (`day2_tools.py`)
- 异步网络搜索
- DuckDuckGo API集成
- 结果解析和格式化

#### 2. 文件读写工具 (`day2_file_tools.py`)
- CSV文件读写
- JSON文件处理
- 数据追加功能

#### 3. 数据分析工具 (`day2_analysis_tools.py`)
- 销售数据分析
- 产品对比分析
- 趋势预测和建议

#### 4. 记忆系统 (`day2_memory.py`)
- ChromaDB向量数据库
- 对话历史存储
- 语义搜索功能
- 自动清理过期记忆

#### 5. 记忆增强Agent (`day2_memory_agent.py`)
- 带记忆的对话
- 上下文关联
- 对话摘要统计

#### 6. 多Agent团队 (`day2_team.py`)
- 4个角色Agent
- 任务依赖管理
- 协作流程

#### 7. 竞品分析系统 (`day2_competitor_analysis.py`)
- 完整的分析系统
- 批量分析功能
- 报告生成和保存

#### 8. 异步处理 (`day2_async.py`)
- 并发执行
- 性能对比
- 超时处理

#### 9. 缓存机制 (`day2_cache.py`)
- 智能缓存
- 过期清理
- 性能统计

## 🧪 测试指南

### 测试Day 1

```bash
python day1_agent.py
```

预期：启动交互式对话，可以与AI Agent聊天。

### 测试Day 2工具

```bash
# 测试网络搜索
python day2_tools.py

# 测试文件处理
python day2_file_tools.py

# 测试数据分析
python day2_analysis_tools.py

# 测试记忆系统
python day2_memory.py

# 测试记忆增强Agent
python day2_memory_agent.py
```

### 测试多Agent系统

```bash
# 测试多Agent团队
python day2_team.py

# 测试竞品分析系统
python day2_competitor_analysis.py
```

### 测试性能优化

```bash
# 测试异步处理
python day2_async.py

# 测试缓存机制
python day2_cache.py
```

## 📊 生成的文件

运行后会生成以下目录：

```
ai-agent-tutorial/
├── cache/                   # 缓存文件
├── chroma_db/              # 向量数据库
├── competitor_reports/     # 竞品分析报告
└── test_*.csv/json         # 测试文件
```

## ⚠️ 常见问题

### Q1: 提示"API密钥无效"

**A**: 检查 `.env` 文件格式，确保：
- 没有多余空格
- API密钥格式正确（sk-开头）
- DeepSeek账户有可用额度

### Q2: 导入错误

**A**: 重新安装依赖：

```bash
pip install --force-reinstall -r requirements.txt
```

### Q3: 数据库错误

**A**: 删除 `chroma_db/` 目录，程序会自动重建。

### Q4: 搜索功能无响应

**A**: DuckDuckGo API偶尔不稳定，等待几秒后重试。

## 🔗 相关资源

- Day 1 教程：`微信公众号文章-AI Agent实战.md`
- Day 2 教程：`微信公众号文章-AI Agent实战-Day2.md`
- DeepSeek API: https://platform.deepseek.com/
- LangChain文档: https://python.langchain.com/
- CrewAI文档: https://docs.crewai.com/

## 📝 注意事项

1. 所有文件都可以独立运行测试
2. 每个文件都有完整的测试代码
3. 首次运行会下载依赖，可能需要几分钟
4. API调用需要网络连接和DeepSeek额度
5. 数据存储在本地，可以随时查看

## 🎯 下一步

- Day 3: 部署上线与商业化实战
- 集成企业微信/飞书
- 添加Web界面
- 性能监控与优化

---

**祝你学习愉快！** 🚀