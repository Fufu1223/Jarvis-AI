import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 配置 API (这一步你应该很熟了)
load_dotenv("key.env")
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# 2. 你的核心函数 (保持原样，不要动)
def get_stock_price(symbol: str):
    # ... (这里是你刚才写的代码，保留它) ...
    symbol = symbol.upper()
    market_data = {
        "AAPL": 150.5,
        "TSLA": 200.0,
        "GOOGL": 180.2,
        "MSFT": 300.1
    }
    return market_data.get(symbol, "未查询到该股票数据")

# 3. 🔥 新增：定义工具菜单
# 这段 JSON 告诉 AI：有个工具叫 get_stock_price，需要一个叫 symbol 的参数
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "当用户询问股票价格时使用。注意：如果是中文公司名，请先转换为美股代码（如 苹果->AAPL）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码，例如 AAPL, TSLA, MSFT"
                    }
                },
                "required": ["symbol"]
            }
        }
    }
]

# 4. 🔥 新增：API 调用函数 (复习 Day 09)
def get_ai_response(messages: list) -> object:
    """
    发送消息并附带工具菜单
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools  # 把菜单递上去
        )
        return response.choices[0].message
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        return None

def main():
    print("🚀 华尔街之狼 (AI 行情助手) 已启动...")
    
    # 初始化聊天记录
    # 我们先给 AI 洗脑，设定它是一个专业助理
    messages = [
        {"role": "system", "content": "你是一个专业的金融助手。如果用户问股价，请使用工具查询。"}
    ]

    while True:
        user_input = input("\n👤 用户: ")
        if user_input.lower() == "quit":
            break
        
        # 1. 把用户的话加进去
        messages.append({"role": "user", "content": user_input})
        
        # 2. 第一轮调用：看看 AI 想不想用工具？
        ai_message = get_ai_response(messages)
        
        # 3. 判断：AI 是想聊天，还是想调用工具？
        if ai_message.tool_calls:
            # === 🟢 进入工具调用流程 ===
            
            tool_call = ai_message.tool_calls[0]
            func_name = tool_call.function.name
            
            # 解析参数 (记得昨天的 json.loads 吗？)
            args = json.loads(tool_call.function.arguments)
            stock_symbol = args.get("symbol")
            
            print(f"🤖 AI 请求调用工具: {func_name} | 参数: {stock_symbol}")
            
            # --- 真正的干活环节 ---
            if func_name == "get_stock_price":
                # 调用我们在 Step 1 写的函数
                price_result = get_stock_price(stock_symbol)
                print(f"✅ 本地执行结果: {price_result}")
                
                # --- 🔥 关键步骤：把结果骗回给 AI (闭环) ---
                # 我们要伪造一条 "tool" 类型的消息，告诉 AI 结果是多少
                # 这一步如果不做，AI 就永远不知道股价是多少
                messages.append(ai_message) # 把 AI 刚才的“请求”加进历史
                
                messages.append({
                    "role": "tool",              # 角色是工具
                    "tool_call_id": tool_call.id, # 对应刚才的请求 ID
                    "content": str(price_result)  # 告诉它结果 (必须转成字符串)
                })
                
                # 4. 第二轮调用：让 AI 根据结果生成最终回答
                # AI 现在看到历史记录里有股价了，它可以说话了
                final_response = get_ai_response(messages)
                print(f"🤖 AI 最终回复: {final_response.content}")
                
                # 记得把最终回复也加进历史，保持连贯
                messages.append({"role": "assistant", "content": final_response.content})

        else:
            # === 🔵 普通聊天流程 ===
            print(f"🤖 AI: {ai_message.content}")
            messages.append({"role": "assistant", "content": ai_message.content})

if __name__ == "__main__":
    main()
