import os

# 1. 告诉我你现在在哪里
current_folder = os.getcwd()
print(f"📍 Python 当前工作目录: {current_folder}")

# 2. 告诉我这里面都有谁
print(f"📂 目录下的文件清单:")
files = os.listdir(current_folder)

found_env = False
for file in files:
    # 打印每个文件名
    print(f"  - {file}")
    if ".env" in file:
        found_env = True
        # 重点检查：是不是叫 .env.txt？
        if file == ".env":
            print("    ✅ 发现标准的 .env 文件！")
        elif file == ".env.txt":
            print("    ❌ 发现伪装者！文件名是 .env.txt，请重命名！")
        else:
            print(f"    ⚠️ 发现类似文件: {file}")

if not found_env:
    print("\n❌ 完蛋！在这个目录下根本没找到包含 '.env' 的文件。")
    print("可能原因：你的 .env 文件在上一级，或者被你存到别的地方去了。")