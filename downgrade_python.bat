@echo off
chcp 65001 >nul
echo ========================================
echo Python降级脚本 - 从3.13到3.11
echo ========================================
echo.

REM 检查当前Python版本
echo [1/6] 检查当前Python版本...
python --version
echo.

REM 下载Python 3.11
echo [2/6] 准备下载Python 3.11...
echo 请访问以下链接下载Python 3.11安装包：
echo https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
echo.
echo 下载完成后，请按任意键继续...
pause >nul

REM 提示用户安装Python 3.11
echo [3/6] 请安装Python 3.11...
echo.
echo 重要提示：
echo 1. 运行下载的 python-3.11.9-amd64.exe
echo 2. 勾选 "Add Python 3.11 to PATH"
echo 3. 选择 "Install Now" 或 "Customize installation"
echo 4. 如果选择自定义，确保勾选：
echo    - pip
echo    - tcl/tk and IDLE
echo    - Python test suite
echo    - py launcher (for all users)
echo 5. 安装完成后，按任意键继续...
echo.
pause >nul

REM 检查Python 3.11是否安装成功
echo [4/6] 检查Python 3.11是否安装成功...
py -3.11 --version 2>nul
if errorlevel 1 (
    echo ❌ Python 3.11未正确安装
    echo 请确保已成功安装Python 3.11
    pause
    exit /b 1
) else (
    echo ✅ Python 3.11已成功安装
    py -3.11 --version
)

echo.

REM 删除旧虚拟环境
echo [5/6] 删除旧的虚拟环境...
if exist venv (
    echo 正在删除 venv 目录...
    rmdir /s /q venv
    echo ✅ 旧虚拟环境已删除
) else (
    echo ℹ️ 没有找到旧的虚拟环境
)

echo.

REM 创建新虚拟环境
echo [6/6] 创建新的虚拟环境并安装依赖...
py -3.11 -m venv venv
echo ✅ 新虚拟环境已创建

echo.
echo 正在激活虚拟环境...
call venv\Scripts\activate.bat

echo.
echo 正在升级pip...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在安装项目依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在安装PyTorch...
pip install torch --index-url https://download.pytorch.org/whl/cpu -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在安装sentence-transformers...
pip install sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ========================================
echo ✅ Python降级完成！
echo ========================================
echo.
echo 现在可以运行以下命令测试：
echo streamlit run day3_app.py
echo.
pause