# print("====皇家AI守门员=====")

# password = input("请输入暗号：")

#     if password == "芝麻开门":
#     print("开门了，请进")
#     print("欢迎来到宝藏库。")

#     else:
#     print("这里的山路十八弯")
#     print("快走开，冒牌货！")


# print("游戏结束")
print("====AI成本风控系统=====")

cost_input = input("请输入本次API调用的预估成本：")

cost = float(cost_input)

if cost > 50:
    print("警告！本次成本过高，请重新调用。")
    print(f"你需要{cost}元,不然老板会杀人的")
    print("操作已拦截")
else:
    print("✅ 成本在预算内。")
    print(f"正在调用 API，花费 {cost} 元...")

print("--- 检查结束 ---")   