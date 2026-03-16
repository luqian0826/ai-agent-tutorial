@echo off
chcp 65001 >nul
echo ========================================
echo 重新构建虚拟环境脚本
echo ========================================
echo.

REM 删除旧虚拟环境
echo [1/3] 删除旧的虚拟环境...
if exist venv (
    echo 正在删除 venv 目录...
    rmdir /s /q venv
    echo ✅ 旧虚拟环境已删除
) else (
    echo ℹ️ 没有找到旧的虚拟环境
)

echo.

REM 创建新虚拟环境（使用Python 3.11）
echo [2/3] 创建新的虚拟环境（Python 3.11）...
py -3.11 -m venv venv
if errorlevel 1 (
    echo ❌ 创建虚拟环境失败
    echo 请确保已安装Python 3.11
    pause
    exit /b 1
)
echo ✅ 新虚拟环境已创建

echo.

REM 安装依赖
echo [3/3] 安装项目依赖...
call venv\Scripts\activate.bat

echo.
echo 正在升级pip...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在安装项目依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在安装PyTorch CPU版本...
pip install torch --index-url https://download.pytorch.org/whl/cpu -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 正在安装sentence-transformers...
pip install sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ========================================
echo ✅ 虚拟环境重新构建完成！
echo ========================================
echo.
echo 现在可以运行以下命令：
echo streamlit run day3_app.py
echo.
pause