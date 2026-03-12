# 🚀 快速开始指南

## 3步开始使用

### 第1步：安装依赖

```bash
pip install -r requirements.txt
```

### 第2步：配置API密钥

```bash
# 复制模板
copy .env.example .env

# 编辑 .env 文件
# 将 your_api_key_here 替换为你的 DeepSeek API 密钥
```

获取API密钥：https://platform.deepseek.com/

### 第3步：运行测试

```bash
# 方式1：运行所有测试
python test_all.py

# 方式2：单独测试某个模块
python day1_agent.py
python day2_tools.py
python day2_memory.py
```

## 📋 测试清单

### Day 1 测试

```bash
python day1_agent.py
```

✅ 预期：启动对话系统，可以与AI Agent交互

**测试对话**：
- "现在几点了？"
- "帮我总结一下今天的工作"

---

### Day 2 工具测试

#### 1. 网络搜索工具

```bash
python day2_tools.py
```

✅ 预期：搜索"AI Agent"并返回结果

---

#### 2. 文件读写工具

```bash
python day2_file_tools.py
```

✅ 预期：
- 创建示例CSV文件
- 读取并显示内容
- 生成JSON报告
- 测试数据追加功能

---

#### 3. 数据分析工具

```bash
python day2_analysis_tools.py
```

✅ 预期：
- 分析销售数据
- 计算增长率
- 生成建议
- 产品排名分析

---

#### 4. 记忆系统

```bash
python day2_memory.py
```

✅ 预期：
- 存储对话记忆
- 搜索相关记忆
- 查看最近对话
- 显示统计信息

---

#### 5. 记忆增强Agent

```bash
python day2_memory_agent.py
```

✅ 预期：
- 记住用户信息
- 搜索历史对话
- 提供连贯回答
- 显示对话摘要

---

#### 6. 多Agent团队

```bash
python day2_team.py
```

✅ 预期：
- 协调4个Agent角色
- 执行竞品分析任务
- 生成分析报告

⚠️ 注意：此测试需要较长时间（约2-3分钟）

---

#### 7. 竞品分析系统

```bash
python day2_competitor_analysis.py
```

✅ 预期：
- 分析单个产品
- 生成JSON报告
- 显示分析历史
- 报告保存到 `competitor_reports/` 目录

---

#### 8. 异步处理

```bash
python day2_async.py
```

✅ 预期：
- 性能对比测试
- 批量异步分析
- 显示加速比
- 超时处理演示

---

#### 9. 缓存机制

```bash
python day2_cache.py
```

✅ 预期：
- 缓存未命中测试
- 缓存命中测试
- 性能对比
- 显示加速比

---

## 🧪 完整测试

运行所有测试：

```bash
python test_all.py
```

选择 `0` 运行所有模块测试，或选择特定模块进行测试。

---

## 📊 预期输出

### Day 1 示例输出

```
🎯 欢迎使用你的第一个AI Agent！
==================================================
正在初始化DeepSeek模型...
创建Agent中...
✅ Agent创建成功！
==================================================

🤖 你想问什么？（输入'退出'结束）: 现在几点了？

==================================================
🤖 AI Agent回复：
现在是2024-03-12 14:30:45
```

### Day 2 工具示例输出

```
🔍 测试网络搜索工具
============================================================
{
  "title": "摘要",
  "content": "AI Agent是一种能够自主感知环境...",
  "url": "https://example.com"
}
...
✅ 搜索测试完成
```

---

## ⚠️ 常见问题

### 问题1：提示"API密钥无效"

**解决**：
1. 检查 `.env` 文件是否存在
2. 确认API密钥格式正确（sk-开头）
3. 确认DeepSeek账户有可用额度
4. 确认网络能访问 `api.deepseek.com`

### 问题2：导入错误

**解决**：
```bash
pip install --force-reinstall -r requirements.txt
```

### 问题3：数据库错误

**解决**：
```bash
# 删除数据库目录
rmdir /s /q chroma_db

# 重新运行测试
python day2_memory.py
```

### 问题4：搜索功能无响应

**解决**：
- DuckDuckGo API偶尔不稳定
- 等待几秒后重试
- 检查网络连接

### 问题5：多Agent测试超时

**解决**：
- 正常情况需要2-3分钟
- 可以增加超时时间
- 检查网络连接

---

## 📁 生成的文件

运行测试后会生成以下目录：

```
ai-agent-tutorial/
├── cache/                   # 缓存文件
│   └── *.json              # 搜索和分析缓存
├── chroma_db/              # 向量数据库
│   └── ...                 # 对话记忆存储
├── competitor_reports/     # 竞品分析报告
│   └── *.json              # 分析报告文件
└── test_*.csv/json         # 测试文件（可删除）
```

---

## 💡 使用技巧

### 1. 快速测试单个功能

```bash
# 测试网络搜索
python day2_tools.py

# 测试文件处理
python day2_file_tools.py
```

### 2. 查看生成的报告

```bash
# 查看竞品分析报告
type competitor_reports\*.json
```

### 3. 清理测试数据

```bash
# 清理缓存
del cache\*.json

# 清理数据库
rmdir /s /q chroma_db

# 清理测试文件
del test_*.csv test_*.json
```

---

## 🎓 学习路径

### 初学者

1. ✅ 运行 `day1_agent.py` 体验基础Agent
2. ✅ 运行 `day2_tools.py` 学习工具使用
3. ✅ 运行 `day2_memory.py` 了解记忆系统
4. ✅ 运行 `day2_team.py` 体验多Agent协作

### 进阶用户

1. ✅ 运行 `day2_analysis_tools.py` 学习数据分析
2. ✅ 运行 `day2_async.py` 理解异步处理
3. ✅ 运行 `day2_cache.py` 掌握缓存机制
4. ✅ 修改代码添加自定义功能

### 开发者

1. ✅ 查看源代码学习实现细节
2. ✅ 修改配置文件调整行为
3. ✅ 添加新的Agent和工具
4. ✅ 优化性能和功能

---

## 📚 参考文档

- Day 1 教程：`微信公众号文章-AI Agent实战.md`
- Day 2 教程：`微信公众号文章-AI Agent实战-Day2.md`
- README：`README.md`
- 测试脚本：`test_all.py`

---

## 🎊 开始吧！

现在你已经准备好开始学习AI Agent了！

**下一步**：
1. 安装依赖
2. 配置API密钥
3. 运行第一个测试

**祝你学习愉快！** 🚀