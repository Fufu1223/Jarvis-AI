import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("key.env")

api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def load_memory(filepath: str) -> list:
    """
    功能: 从指定路径读取 JSON 文件
    参数 filepath: 文件路径 (str)
    返回: 聊天记录列表 (list)
    """
    # --- 填空区域开始 ---
    try:
        # 注意：这里打开文件时，不要写死 "memory.json"，要用变量 filepath
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f) # 我们把读到的东西暂存到 data 变量
    except FileNotFoundError:
        data = [] # 如果找不到文件，就创建一个空列表
    # --- 填空区域结束 ---
    
    # 最后，把结果交出去
    return data

def save_memory(filepath: str, data: list) -> None:
    """
    功能: 将数据写入 JSON 文件
    参数 filepath: 文件路径 (str)
    参数 data: 要保存的数据 (list)
    返回: None
    """
    # 这里的 "w" 模式会覆盖写入，符合我们之前的逻辑
    with open(filepath, "w", encoding="utf-8") as f:
        # 👇 请把原来 json.dump 的逻辑搬进来
        # 提示: 第一个参数是要存的数据变量名，第二个是文件对象 f
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_ai_response(messages: list) -> str:
    """
    功能: 调用 DeepSeek API 获取回复
    参数 messages: 聊天记录列表 (list)
    返回: AI 的回复文本 (str)
    """
    # 🌟 25w 年薪级细节: 加上 try-except 防止断网导致程序崩溃
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            # 👇 这里要把参数传进去
            messages=messages
        )
        # 👇 提取回复文本并返回
        return response.choices[0].message.content
        
    except Exception as e:
        # 如果出错了 (比如断网、没钱了)，打印错误并返回一个提示
        print(f"❌ API 调用失败: {e}")
        return "（贾维斯掉线了，请检查网络...）"

# ... (上面是你写好的三个函数：load_memory, save_memory, get_ai_response) ...

def main():
    """
    主程序入口：负责调度所有模块
    """
    print("🚀 贾维斯 (25w工程版) 正在启动...")
    
    # 1. 定义记忆文件路径
    memory_file = "memory.json"
    
    # 2. 调用函数：加载记忆
    # 提示：把 memory_file 传进去，把结果赋值给 chat_history
    chat_history = load_memory(memory_file)

    while True:
        user_input = input("\n你说: ")
        
        if user_input.lower() == "quit":
            print("👋 再见！")
            break
        
        # 3. 记录用户输入
        chat_history.append({"role": "user", "content": user_input})
        
        # 4. 调用函数：获取 AI 回复 (最关键的一步！)
        # 提示：调用 get_ai_response，把 chat_history 传给它
        # 结果赋值给 ai_msg
        ai_msg = get_ai_response(chat_history)
        
        print(f"🤖 AI: {ai_msg}")
        
        # 5. 记录 AI 回复
        chat_history.append({"role": "assistant", "content": ai_msg})
        
        # 6. 调用函数：保存记忆
        # 提示：把 memory_file 和 chat_history 传进去
        save_memory(memory_file, chat_history)

# 标准程序的启动开关
if __name__ == "__main__":
    main()