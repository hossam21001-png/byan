"""دعم AI للغة بيان"""
import os


class ByanAI:
    """يتعامل مع AI (OpenAI, etc.)"""

    def __init__(self, provider='openai', api_key=None):
        self.provider = provider
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        self.model = 'gpt-3.5-turbo'

    def ask(self, prompt):
        """يسأل AI ويرجع الرد"""
        if not self.api_key:
            return "⚠️ محتاج OPENAI_API_KEY في البيئة"

        try:
            import openai
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ خطأ: {e}"
