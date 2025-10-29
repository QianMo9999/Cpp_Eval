#!/usr/bin/env python3
"""
API配置测试脚本
用于验证各个大模型API是否配置正确
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from llm_evaluator import get_evaluator


def test_api(provider: str):
    """
    测试指定的API提供商

    Args:
        provider: API提供商名称
    """
    print(f"\n{'='*60}")
    print(f"测试 {provider.upper()} API")
    print('='*60)

    # 简单的测试代码
    test_code = """#include <iostream>
using namespace std;

int main() {
    int a = 5, b = 3;
    cout << "a + b = " << a + b << endl;
    return 0;
}"""

    test_prompt = f"""请简短评价以下C++代码（50字以内）：

```cpp
{test_code}
```

请只给出简短评价，不要太详细。"""

    try:
        # 创建评价器
        print(f"\n正在初始化 {provider} 评价器...")
        evaluator = get_evaluator(provider=provider)
        print("✓ 评价器初始化成功")

        # 调用API
        print(f"\n正在调用 {provider} API...")
        result = evaluator.evaluate(test_prompt)

        print("\n✓ API调用成功!")
        print("\n返回结果:")
        print("-" * 60)
        print(result)
        print("-" * 60)

        return True

    except ValueError as e:
        print(f"\n✗ 配置错误: {str(e)}")
        print("\n请检查 .env 文件中的API配置")
        return False
    except Exception as e:
        print(f"\n✗ API调用失败: {str(e)}")
        return False


def main():
    """主函数"""
    print("="*60)
    print("C++ 作业评价系统 - API配置测试工具")
    print("="*60)

    # 检查.env文件
    if not os.path.exists('.env'):
        print("\n✗ 错误: 未找到 .env 文件")
        print("\n请先创建 .env 文件:")
        print("  cp .env.example .env")
        print("  然后编辑 .env 文件填入你的API密钥")
        sys.exit(1)

    # 读取配置的API提供商
    api_provider = os.getenv('API_PROVIDER', 'openai')
    print(f"\n当前配置的API提供商: {api_provider.upper()}")

    # 可用的提供商列表
    available_providers = ['openai', 'claude', 'dashscope', 'deepseek']

    print("\n可测试的API提供商:")
    for i, provider in enumerate(available_providers, 1):
        status = "✓ (当前使用)" if provider == api_provider else "○"
        print(f"  {i}. {status} {provider}")

    print("\n" + "="*60)
    print("请选择要测试的API:")
    print("  1. 测试当前配置的API")
    print("  2. 测试所有已配置的API")
    print("  3. 指定API提供商测试")
    print("  0. 退出")
    print("="*60)

    choice = input("\n请输入选项 (0-3): ").strip()

    if choice == '0':
        print("\n已退出")
        return

    elif choice == '1':
        # 测试当前配置的API
        success = test_api(api_provider)
        if success:
            print(f"\n{'='*60}")
            print(f"✓ {api_provider.upper()} API 配置正确，可以使用!")
            print('='*60)
        else:
            print(f"\n{'='*60}")
            print(f"✗ {api_provider.upper()} API 配置有问题，请检查配置")
            print('='*60)

    elif choice == '2':
        # 测试所有API
        results = {}
        for provider in available_providers:
            # 检查是否配置了该API
            key_var = {
                'openai': 'OPENAI_API_KEY',
                'claude': 'ANTHROPIC_API_KEY',
                'dashscope': 'DASHSCOPE_API_KEY',
                'deepseek': 'DEEPSEEK_API_KEY'
            }

            api_key = os.getenv(key_var[provider])
            if not api_key or api_key.startswith('your_'):
                print(f"\n跳过 {provider}: 未配置API密钥")
                results[provider] = False
                continue

            success = test_api(provider)
            results[provider] = success

        # 输出汇总
        print("\n" + "="*60)
        print("测试汇总")
        print("="*60)
        for provider, success in results.items():
            status = "✓ 成功" if success else "✗ 失败"
            print(f"  {provider:12} : {status}")
        print("="*60)

    elif choice == '3':
        # 指定API测试
        print("\n可用的API提供商:")
        for i, provider in enumerate(available_providers, 1):
            print(f"  {i}. {provider}")

        provider_choice = input("\n请输入编号 (1-4): ").strip()
        try:
            idx = int(provider_choice) - 1
            if 0 <= idx < len(available_providers):
                provider = available_providers[idx]
                success = test_api(provider)
                if success:
                    print(f"\n{'='*60}")
                    print(f"✓ {provider.upper()} API 配置正确!")
                    print('='*60)
            else:
                print("\n✗ 无效的选项")
        except ValueError:
            print("\n✗ 无效的输入")

    else:
        print("\n✗ 无效的选项")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        print(f"\n✗ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
