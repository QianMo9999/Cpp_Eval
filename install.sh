#!/bin/bash

# C++作业评价系统 - 安装脚本

echo "================================"
echo "C++作业评价系统 - 依赖安装"
echo "================================"
echo ""

# 检查Python版本
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "错误: 未找到Python，请先安装Python 3.7+"
    exit 1
fi

echo "使用的Python命令: $PYTHON_CMD"
$PYTHON_CMD --version
echo ""

# 检查pip
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "错误: pip未安装，请先安装pip"
    exit 1
fi

echo "开始安装依赖..."
echo "================================"
echo ""

# 安装依赖
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✓ 依赖安装成功！"
    echo "================================"
    echo ""
    echo "下一步："
    echo "1. 配置API密钥："
    echo "   cp .env.example .env"
    echo "   然后编辑.env文件填入你的API密钥"
    echo ""
    echo "2. 测试API配置："
    echo "   $PYTHON_CMD test_api.py"
    echo ""
    echo "3. 运行评价系统："
    echo "   $PYTHON_CMD src/main.py data/第02周上机作业.zip --week 02"
    echo ""
else
    echo ""
    echo "================================"
    echo "✗ 依赖安装失败"
    echo "================================"
    echo ""
    echo "请检查网络连接或尝试手动安装："
    echo "  $PYTHON_CMD -m pip install openai anthropic python-dotenv openpyxl"
    exit 1
fi
