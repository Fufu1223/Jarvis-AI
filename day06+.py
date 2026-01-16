#导入必要的库 (os, json, dotenv, OpenAI).
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("key.env")

api_key = os.getenv("DEEPSEEK_API_KEY")

# api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

try:

    with open("memory.json", "r", encoding="utf-8") as f:
        chat_history = json.load(f)

except FileNotFoundError:
    chat_history = []

while True:
    # 1. 获取输入
    user_input = input("\n你说: ") # 修正了 /n 为 \n
    
    # 2. 退出机制 (记得加冒号)
    if user_input == "quit":
        print("👋贾维斯正在下线...")
        break
    
    # 3. 存入用户消息 (记得缩进!)
    chat_history.append({"role": "user", "content": user_input})
    
    # --- 🛑 你漏掉的核心部分开始 ---
    
    # 4. 调用 API (让大脑思考)
    # 提示: messages=chat_history
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages = chat_history
    )
    
    # 5. 获取 AI 回复文本
    ai_msg = response.choices[0].message.content
    print(f"🤖 AI: {ai_msg}")
    
    # 6. 存入 AI 消息
    # 提示: role 是 "assistant"
    chat_history.append({"role": "assistant", "content": ai_msg})
    
    # --- 🛑 你漏掉的核心部分结束 ---

    # 7. 实时存档 (Auto-Save)
    # 这一步必须在循环里，这样每说一句话都会保存
    with open("memory.json", "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=4)

