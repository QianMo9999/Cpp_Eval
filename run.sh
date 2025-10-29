#!/bin/bash

# C++作业评价系统 - 快速启动脚本

echo "================================"
echo "C++作业评价系统"
echo "================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

# 检查是否已安装依赖
if [ ! -d "venv" ]; then
    echo "首次运行，正在创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "安装依赖..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 检查.env文件是否存在
if [ ! -f ".env" ]; then
    echo ""
    echo "警告: 未找到.env文件"
    echo "请先复制.env.example为.env并配置API密钥："
    echo "  cp .env.example .env"
    echo "  然后编辑.env文件填入你的API密钥"
    echo ""
    exit 1
fi

# 检查data目录中是否有ZIP文件
ZIP_FILES=$(ls data/*.zip 2>/dev/null)

if [ -z "$ZIP_FILES" ]; then
    echo ""
    echo "警告: data目录中未找到ZIP文件"
    echo "请将学生作业ZIP文件放入data目录"
    echo ""
    exit 1
fi

# 列出可用的ZIP文件
echo "找到以下作业文件："
echo ""
select ZIP_FILE in data/*.zip "退出"; do
    if [ "$ZIP_FILE" = "退出" ]; then
        echo "已退出"
        exit 0
    fi

    if [ -n "$ZIP_FILE" ]; then
        echo ""
        echo "选择的文件: $ZIP_FILE"

        # 询问周次
        read -p "请输入作业周次 (默认: 02): " WEEK
        WEEK=${WEEK:-02}

        # 运行评价
        echo ""
        echo "开始评价..."
        python src/main.py "$ZIP_FILE" --week "$WEEK"

        echo ""
        echo "评价完成！结果保存在output目录"
        break
    else
        echo "无效选择，请重试"
    fi
done
