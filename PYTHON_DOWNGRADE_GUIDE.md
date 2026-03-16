# Python降级指南（从3.13到3.11）

## 问题说明

当前Python版本：3.13.12
问题：PyTorch 2.10.0不支持Python 3.13，导致竞品分析功能和完整版主应用无法使用

## 解决方案

降级到Python 3.11.9（PyTorch完全支持）

---

## 详细步骤

### 第1步：下载Python 3.11

1. 访问Python官网下载页面：
   ```
   https://www.python.org/downloads/
   ```

2. 点击"Python 3.11.9"下载按钮，或直接下载：
   ```
   https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
   ```

3. 下载文件：`python-3.11.9-amd64.exe`

---

### 第2步：安装Python 3.11

1. 双击运行 `python-3.11.9-amd64.exe`

2. **重要：勾选 "Add Python 3.11 to PATH"**

3. 点击 "Install Now" 或 "Customize installation"

4. 如果选择自定义安装，确保勾选：
   - ✅ pip
   - ✅ tcl/tk and IDLE
   - ✅ Python test suite
   - ✅ py launcher (for all users)

5. 等待安装完成

---

### 第3步：验证Python 3.11安装

打开新的命令行窗口，运行：

```bash
py -3.11 --version
```

应该显示：`Python 3.11.9`

---

### 第4步：重新构建虚拟环境

在项目根目录运行脚本：

```bash
rebuild_venv.bat
```

或者手动执行：

```bash
# 1. 删除旧虚拟环境
rmdir /s /q venv

# 2. 创建新虚拟环境（使用Python 3.11）
py -3.11 -m venv venv

# 3. 激活虚拟环境
venv\Scripts\Activate.ps1

# 4. 升级pip
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 6. 安装PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cpu -i https://pypi.tuna.tsinghua.edu.cn/simple

# 7. 安装sentence-transformers
pip install sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### 第5步：测试应用

1. 测试主应用：
   ```bash
   streamlit run day3_app.py
   ```
   访问：http://localhost:8501/

2. 测试竞品分析：
   访问：http://localhost:8501/day3_competitor_analysis

---

## 完整降级脚本（推荐）

如果你想一次性完成所有步骤，可以运行：

```bash
downgrade_python.bat
```

这个脚本会：
1. 检查当前Python版本
2. 提示下载Python 3.11
3. 引导安装Python 3.11
4. 检查Python 3.11是否安装成功
5. 删除旧虚拟环境
6. 创建新虚拟环境
7. 安装所有依赖

---

## 常见问题

### Q1: 如何确认当前使用的是哪个Python版本？

```bash
python --version
py --list
```

### Q2: 可以同时保留Python 3.13和3.11吗？

可以！使用 `py` 命令可以切换版本：
```bash
py -3.13 --version  # 使用Python 3.13
py -3.11 --version  # 使用Python 3.11
```

### Q3: 虚拟环境会自动使用Python 3.11吗？

是的！当你用 `py -3.11 -m venv venv` 创建虚拟环境时，该环境会固定使用Python 3.11。

### Q4: 如果降级后还有问题怎么办？

1. 确认虚拟环境使用的是Python 3.11：
   ```bash
   venv\Scripts\python.exe --version
   ```

2. 重新安装PyTorch：
   ```bash
   venv\Scripts\pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```

3. 测试PyTorch是否可以导入：
   ```bash
   venv\Scripts\python.exe -c "import torch; print(torch.__version__)"
   ```

---

## 脚本说明

- `downgrade_python.bat` - 完整降级脚本（包含下载引导）
- `rebuild_venv.bat` - 重新构建虚拟环境脚本（假设已安装Python 3.11）

---

## 完成

降级完成后，所有功能将正常工作：

✅ 完整版主应用（day3_app.py）
✅ 竞品分析页面
✅ 所有Day 1和Day 2功能