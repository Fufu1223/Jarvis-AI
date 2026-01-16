from openai import OpenAI
from dotenv import load_dotenv
import os
# --- 配置部分 (Boilerplate) ---
load_dotenv("key.env")

api_key = os.getenv("DEEPSEEK_API_KEY")

# api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# 3. 发送请求 (发微信)
# messages 是一个列表，里面装着对话的历史

cost_input = input("请输入你想问的问题：")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        # 👇 直接写变量名，不要加 {}，也不要加 ""
        {"role": "user", "content": cost_input} 
    ]
)
# 4. 获取并打印回答
# (这行代码看起来很长，别怕，我等会儿解释)
answer = response.choices[0].message.content

print("----------------")
print("🤖 AI 回答：")
print(answer)