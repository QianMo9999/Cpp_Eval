"""
大模型API调用模块
支持多个大模型提供商：OpenAI、Claude、通义千问等
"""
import os
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class LLMEvaluator:
    """大模型评价器基类"""

    def __init__(self):
        self.api_provider = os.getenv('API_PROVIDER', 'openai')

    def evaluate(self, prompt: str) -> str:
        """
        调用大模型进行评价

        Args:
            prompt: 评价提示词

        Returns:
            大模型返回的评价结果
        """
        raise NotImplementedError("子类必须实现此方法")


class OpenAIEvaluator(LLMEvaluator):
    """OpenAI评价器"""

    def __init__(self, model: str = None):
        super().__init__()
        from openai import OpenAI

        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("请在.env文件中设置OPENAI_API_KEY")

        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        self.client = OpenAI(api_key=self.api_key)

    def evaluate(self, prompt: str) -> str:
        """
        使用OpenAI API进行评价

        Args:
            prompt: 评价提示词

        Returns:
            评价结果
        """
        try:
            print(f"正在调用OpenAI API ({self.model})...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的C++编程教师，负责评价学生的作业代码。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API调用失败: {str(e)}")


class ClaudeEvaluator(LLMEvaluator):
    """Claude评价器"""

    def __init__(self, model: str = None):
        super().__init__()
        from anthropic import Anthropic

        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("请在.env文件中设置ANTHROPIC_API_KEY")

        self.model = model or os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
        self.client = Anthropic(api_key=self.api_key)

    def evaluate(self, prompt: str) -> str:
        """
        使用Claude API进行评价

        Args:
            prompt: 评价提示词

        Returns:
            评价结果
        """
        try:
            print(f"正在调用Claude API ({self.model})...")
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"Claude API调用失败: {str(e)}")


class DashScopeEvaluator(LLMEvaluator):
    """通义千问评价器"""

    def __init__(self, model: str = "qwen-turbo"):
        super().__init__()
        self.api_key = os.getenv('DASHSCOPE_API_KEY')
        if not self.api_key:
            raise ValueError("请在.env文件中设置DASHSCOPE_API_KEY")

        self.model = model
        # 设置API Key
        os.environ['DASHSCOPE_API_KEY'] = self.api_key

    def evaluate(self, prompt: str) -> str:
        """
        使用通义千问API进行评价

        Args:
            prompt: 评价提示词

        Returns:
            评价结果
        """
        try:
            import dashscope
            from dashscope import Generation

            print(f"正在调用通义千问API ({self.model})...")
            response = Generation.call(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': '你是一位专业的C++编程教师，负责评价学生的作业代码。'},
                    {'role': 'user', 'content': prompt}
                ],
                result_format='message',
                temperature=0.7,
                max_tokens=2000
            )

            if response.status_code == 200:
                return response.output.choices[0].message.content
            else:
                raise Exception(f"API返回错误: {response.message}")
        except ImportError:
            raise Exception("请安装dashscope库: pip install dashscope")
        except Exception as e:
            raise Exception(f"通义千问API调用失败: {str(e)}")


def get_evaluator(provider: str = None, model: str = None) -> LLMEvaluator:
    """
    获取评价器实例

    Args:
        provider: API提供商 (openai, claude, dashscope)
        model: 模型名称（可选）

    Returns:
        评价器实例
    """
    if provider is None:
        provider = os.getenv('API_PROVIDER', 'openai')

    provider = provider.lower()

    evaluators = {
        'openai': OpenAIEvaluator,
        'claude': ClaudeEvaluator,
        'dashscope': DashScopeEvaluator,
    }

    if provider not in evaluators:
        raise ValueError(f"不支持的API提供商: {provider}. 支持的提供商: {list(evaluators.keys())}")

    evaluator_class = evaluators[provider]

    if model:
        return evaluator_class(model=model)
    else:
        return evaluator_class()


def main():
    """测试函数"""
    # 测试评价器
    test_prompt = """你是一位经验丰富的C++编程教师。请对以下学生的C++代码进行简短评价。

代码：
```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}
```

请简短评价这段代码。
"""

    try:
        evaluator = get_evaluator()
        result = evaluator.evaluate(test_prompt)
        print("\n评价结果:")
        print(result)
    except Exception as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main()
