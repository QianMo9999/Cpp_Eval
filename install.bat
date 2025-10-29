@echo off
chcp 65001 >nul
echo ================================
echo C++作业评价系统 - 依赖安装
echo ================================
echo.

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo 开始安装依赖...
echo ================================
echo.

REM 安装依赖
python -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ================================
    echo ✓ 依赖安装成功！
    echo ================================
    echo.
    echo 下一步：
    echo 1. 配置API密钥：
    echo    copy .env.example .env
    echo    然后编辑.env文件填入你的API密钥
    echo.
    echo 2. 测试API配置：
    echo    python test_api.py
    echo.
    echo 3. 运行评价系统：
    echo    python src\main.py data\第02周上机作业.zip --week 02
    echo.
) else (
    echo.
    echo ================================
    echo ✗ 依赖安装失败
    echo ================================
    echo.
    echo 请检查网络连接或尝试手动安装：
    echo   python -m pip install openai anthropic python-dotenv openpyxl
)

pause
