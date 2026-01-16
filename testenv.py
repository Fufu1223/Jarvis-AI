import os
from dotenv import load_dotenv

# 1. 加载 .env 文件
# override=True 表示：如果 .env 里有值，就强制覆盖系统里的旧值（防止读取到过期的）
load_dotenv(override=True)

# 2. 尝试获取 Key
api_key = os.getenv("DEEPSEEK_API_KEY")

# 3. 打印诊断报告
print("-" * 30)
if api_key:
    print("✅ 成功！Key 已加载。")
    # 为了安全，只打印前 5 位和后 5 位，中间打码
    masked_key = f"{api_key[:5]}...{api_key[-5:]}"
    print(f"Key 内容: {masked_key}")
else:
    print("❌ 失败！os.getenv 返回了 None。")
    print("请检查：")
    print("1. 文件名是不是严格叫 .env？(不要叫 .env.txt)")
    print("2. .env 文件是不是和 test_env.py 在同一个文件夹里？")
print("-" * 30)