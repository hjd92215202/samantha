import os
# 导入加载 .env 的工具 python-dotenv 库提供的核心函数，专门用来寻找并读取 .env 文件
from dotenv import load_dotenv
# 从 brain.py 文件中导入我们刚才写好的 SamanthaBrain 类
from brain import SamanthaBrain

# Python 会在当前文件夹找 .env 文件，把里面的 DEEPSEEK_API_KEY=sk-xxx 写入到当前程序的系统环境变量缓存里。
load_dotenv()

# 从环境变量中获取 DEEPSEEK_API_KEY
# os.getenv: Python 内置的读取环境变量的函数。如果找不到这个变量，它会返回 None
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 安全检查：如果没拿到 Key，直接友情提示并报错，防止后续报错太晦涩
if not DEEPSEEK_API_KEY:
    print("❌ 错误：未检测到 DEEPSEEK_API_KEY！")
    print("请检查项目根目录下是否存在 .env 文件，且里面写有 DEEPSEEK_API_KEY=sk-xxx")
    exit(1) # 退出程序

def main():
    # 初始化你的 Samantha
    # 实例化对象。这一步会触发 brain.py 中的 __init__ 函数：加载 prompt、读取 memory.json、初始化 DeepSeek 客户端
    samantha = SamanthaBrain(api_key=DEEPSEEK_API_KEY)

    # Python 字符串乘法，直接生成 40 个 = 组成的分割线
    print("="*40)
    print("  Samantha 激活成功。(输入 'quit' 离开)")
    print("="*40)

    # 保持程序处于监听状态，不断等待用户输入，直到触发退出条件
    while True:
        try:
            # input("\n你: ")：阻塞式等待用户在命令行输入文字，敲回车提交
            # .strip()：去除用户输入字符串首尾的空格和换行符。防止用户不小心按了空格报错
            user_input = input("\n你: ").strip()
            # 如果用户直接敲了回车（空字符串），continue 跳过本次循环，重新等待输入
            if not user_input:
                continue
            if user_input.lower() in ["quit", "exit"]:
                print("\nSamantha: 晚安，明天见。")
                break
            
            samantha.chat(user_input)
        # 捕获用户在终端按下 Ctrl + C 强制终止程序的信号，优雅地打印“拜拜！”后再退出
        except KeyboardInterrupt:
            print("\nSamantha: 拜拜！")
            break

# Python 的经典语法糖
# 当直接运行 python main.py 时，__name__ 的值就是 "__main__"，下面的 main() 就会被执行
# 如果别的文件 import main，__name__ 就不是 "__main__"，main() 就不会自动触发。这保证了代码既可以作为脚本直接运行，也可以作为模块被其他代码导入
if __name__ == "__main__":
    main()