import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("key.env")
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# ==========================================
# 1. 🛠️ 数据层：请完成天气函数
# ==========================================
def get_weather(city: str):
    print(f"🕵️ DEBUG: 正在查询 {city} 的天气...")
    weather_data = {
        "北京": "晴天, 25°C",
        "上海": "小雨, 22°C",
        "广州": "多云, 28°C"
    }
    # 👇 【填空 1】用 .get() 安全取值，如果找不到城市，默认返回 "未知城市"
    return weather_data.get(city, "未知城市")

# ==========================================
# 2. 📜 协议层：请定义工具菜单
# ==========================================
tools = [
    {
        "type": "function",
        "function": {
            # 👇 【填空 2】告诉 AI 工具的名字 (必须和下面的 Python 函数名一模一样)
            "name": "get_weather",
            "description": "当用户询问天气时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如北京、上海"
                    }
                },
                # 👇 【填空 3】哪个参数是必填的？(填参数名)
                "required": ["city"]
            }
        }
    }
]



def get_ai_response(messages):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools
        )
        return response.choices[0].message
    except Exception as e:
        print(e)
        return None

# ==========================================
# 3. 🧠 决策层：主程序
# ==========================================
def main():
    print("🌤️ Jarvis 气象站已启动...")
    messages = [{"role": "system", "content": "你是一个天气预报员。"}]

    while True:
        user_input = input("\n👤 用户: ")
        if user_input.lower() == "quit":
            break
        
        messages.append({"role": "user", "content": user_input})
        
        # 第一次呼叫 AI
        ai_message = get_ai_response(messages)

        # 判断是否要调用工具
        if ai_message.tool_calls:
            tool_call = ai_message.tool_calls[0]
            func_name = tool_call.function.name
            
            # 👇 【填空 4】解析 AI 给的参数 (回顾 json.loads 和 tool_call 的结构)
            # 提示：参数在 tool_call.function.arguments 里
            print(f"🕵️ [解剖工具对象] func: {tool_call.function}")
            args = json.loads(tool_call.function.arguments)
            
            # 👇 【填空 5】从 args 字典里拿出城市名
            # 提示：我们在 tools 里定义的参数名是 "city"
            city_name = args.get("city")
            
            print(f"🤖 AI 请求查询: {city_name}")

            # 执行本地函数
            if func_name == "get_weather":
                # 👇 【填空 6】调用上面写好的 Python 函数，传入城市名
                weather_info = get_weather(city_name)
                
                print(f"✅ 本地结果: {weather_info}")

                messages.append(ai_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(weather_info)
                })
                
                final_response = get_ai_response(messages)
                print(f"🤖 AI: {final_response.content}")
                messages.append({"role": "assistant", "content": final_response.content})
        
        else:
            print(f"🤖 AI: {ai_message.content}")
            messages.append({"role": "assistant", "content": ai_message.content})

if __name__ == "__main__":
    main()