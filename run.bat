@echo off
chcp 65001 >nul
echo ================================
echo C++作业评价系统
echo ================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查是否已安装依赖
if not exist "venv" (
    echo 首次运行，正在创建虚拟环境...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 安装依赖...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM 检查.env文件是否存在
if not exist ".env" (
    echo.
    echo 警告: 未找到.env文件
    echo 请先复制.env.example为.env并配置API密钥：
    echo   copy .env.example .env
    echo   然后编辑.env文件填入你的API密钥
    echo.
    pause
    exit /b 1
)

REM 检查data目录中是否有ZIP文件
set ZIP_COUNT=0
for %%f in (data\*.zip) do set /a ZIP_COUNT+=1

if %ZIP_COUNT%==0 (
    echo.
    echo 警告: data目录中未找到ZIP文件
    echo 请将学生作业ZIP文件放入data目录
    echo.
    pause
    exit /b 1
)

REM 列出可用的ZIP文件
echo 找到以下作业文件：
echo.
set INDEX=1
for %%f in (data\*.zip) do (
    echo [!INDEX!] %%f
    set ZIP_FILE_!INDEX!=%%f
    set /a INDEX+=1
)
echo.

REM 选择文件
set /p CHOICE="请选择文件编号: "
call set ZIP_FILE=%%ZIP_FILE_%CHOICE%%%

if not defined ZIP_FILE (
    echo 无效选择
    pause
    exit /b 1
)

echo.
echo 选择的文件: %ZIP_FILE%

REM 询问周次
set /p WEEK="请输入作业周次 (默认: 02): "
if not defined WEEK set WEEK=02

REM 运行评价
echo.
echo 开始评价...
python src\main.py "%ZIP_FILE%" --week %WEEK%

echo.
echo 评价完成！结果保存在output目录
pause
