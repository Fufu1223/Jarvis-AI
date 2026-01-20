import subprocess
import time

def open_app(app_name: str):
    print(f"🔧 正在尝试启动 {app_name}...")
    
    try:
        # 🌟 核心知识点: Popen 是非阻塞的
        # start 是 Windows 的 cmd 命令，用来启动一个独立窗口
        # shell=True 表示我们要通过命令行壳层去运行
        subprocess.Popen(f"start {app_name}", shell=True)
        print("✅ 启动指令已发送！")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    # 测试启动计算器 (Windows 下叫 calc)
    open_app("calc")
    
    print("🚀 主程序继续运行，没有被卡住！")
    # 为了让你看清效果，我们让主程序睡 2 秒再退出
    time.sleep(2)