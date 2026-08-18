import os
from dotenv import load_dotenv
from brain import SamanthaBrain

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    print("❌ 错误：未检测到 DEEPSEEK_API_KEY！")
    print("请检查项目根目录下是否存在 .env 文件，且里面写有 DEEPSEEK_API_KEY=sk-xxx")
    exit(1) # 退出程序

def main():
    samantha = SamanthaBrain(api_key=DEEPSEEK_API_KEY)

    print("="*40)
    print("  Samantha 激活成功。(输入 'quit' 离开)")
    print("="*40)

    # 保持程序处于监听状态，不断等待用户输入，直到触发退出条件
    while True:
        try:
            user_input = input("\n你: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quit", "exit"]:
                print("\nSamantha: 晚安，明天见。")
                break
            
            samantha.chat(user_input)
        except KeyboardInterrupt:
            print("\nSamantha: 拜拜！")
            break

if __name__ == "__main__":
    main()