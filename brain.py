# python内置库 用于把python的对象（如列表、字典）转换成文本字符串存储到硬盘，或者反过来解析
import json
# python内置库 用于操作系统底层功能，比如判断“某个文件是否存在”
import os
# 从openai第三方库中导入 OpenAI 客户端类
# DeepSeek官方API完全兼容OpenAI的接口格式，所以我们可以直接用OpenAI的官方SDK来调用DeepSeek模型
from openai import OpenAI

# 定义了一个类，可以想象成制作 “Samantha大脑” 的蓝图
class SamanthaBrain:
    # 构造函数/初始化方法
    # 当写 Samantha(...)创建实例时，这个函数会自动执行
    # self 代表创建出来的这个实例对象本身。通过self.xxx 可以在类的各个方法之间共享数据
    # api_key: str: 类型提示(Type Hint), 冒号后面的 str 表示传入字符串类型的API密钥
    # prompt_file: str = "prompt.txt" : 默认参数(Default Argument) 如果调用时没传这个参数，默认就是“prompt.txt”
    def __init__(self, api_key: str, prompt_file: str = "prompt.txt", memory_file: str = "memory.json"):
        # 实例化OpenAI客户端
        self.client = OpenAI(
            api_key=api_key,
            # 将请求目标服务器改到DeepSeek的服务器
            base_url="https://api.deepseek.com"
        )
        # 将记忆文件的路径保存到self身上，方便后续读取和写入
        self.memory_file = memory_file
        
        # 1. 加载灵魂设定 (System Prompt)
        # with open(...) as f: 上下文管理器。用来打开文件
        # with好处是: 文件用完后会自动帮你关闭，即使中途报错也不会造成文件损坏或内存泄漏
        # r 以只读模式打开文件
        # encoding="utf-8": 字符编码。极为重要！不加的话在windows系统上打开中文文件极易报乱码错误
        with open(prompt_file, "r", encoding="utf-8") as f:
            # f.read() 读取文件的全部文本内容，并赋值给实例变量 self.system_prompt
            self.system_prompt = f.read()
            
        # 2. 加载或初始化记忆
        # 调用内部方法 _load_memory()来加载旧的聊天记录，并存入self.history列表中
        self.history = self._load_memory()

    # 函数名前面带一个下划线 _ 是 Python 的命名规范，提示开发者“这是一个内部私有方法，外部请不要随意调用”
    def _load_memory(self):
        """从 JSON 文件读取历史记忆"""
        # 检查本地目录下是否存在 memory.json 文件。存在返回 True，不存在返回 False
        if os.path.exists(self.memory_file):
            # 异常处理语句。
            # 尝试去读取 JSON 文件，如果文件损坏、格式不对（解析报错），就跳到 except，执行 pass（什么也不做），防止程序崩溃。
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    # 把 JSON 格式的文本反序列化为 Python 的对象（这里是一个字典列表 [{"role": ...}, ...]）
                    return json.load(f)
            except:
                pass
        # 如果没有记忆，初始化系统设定
        return [{"role": "system", "content": self.system_prompt}]

    def _save_memory(self):
        """将记忆保存到本地 JSON"""
        # "w"：Write，以写入模式打开文件（如果文件不存在会自动创建，如果已存在会清空重写）
        with open(self.memory_file, "w", encoding="utf-8") as f:
            # json.dump(...)：把 Python 对象 self.history 转化为 JSON 格式写入文件 f
            # ensure_ascii=False：极其关键！ 默认是 True（中文会变成 \u4f60\u597d 这样的编码）。设为 False 才能在 JSON 文件中正确显示原汁原味的中文。
            # indent=2：格式化缩进 2 个空格
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    # -> str：类型提示，说明这个函数最终会返回一个字符串 (str)
    def chat(self, user_input: str) -> str:
        """思考并回答"""
        # 记录你说的话
        # 把用户最新输入的内容，包装成大模型能认出的格式字典：{"role": "user", "content": "内容"}，追加到完整历史列表中
        self.history.append({"role": "user", "content": user_input})
        
        # 简单控制记忆长度，防止 Token 爆炸（只保留系统设定 + 最近 20 条对话）
        # 以后升级 Lv.2 时，这里会改成真正的海马体总结算法！
        # self.history[-20:]：列表切片语法。取列表倒数第 20 个元素到最后一个元素（即最近 20 条对话内容）
        active_messages = [self.history[0]] + self.history[-20:]

        try:
            # 调用 DeepSeek-V4 模拟快速思考与对话
            response = self.client.chat.completions.create(
                model="deepseek-v4-flash",
                messages=active_messages,
                # 越低（如 0.2）：回答越严谨、固定、像机器人
                # 越高（如 0.8）：回答越富有创造力、随机性、像活生生的人
                temperature=0.8, # 略高的温度，让她的性格更活泼、有创造力
                # False：等大模型把几百个字全部生成完后，一次性返回（等待时间长）
                # True：大模型每生成一个字或词（Chunk），就实时推送给客户端（体验极佳，即“打字机效果”）
                stream=True     # 开启流式传输，像人类说话一样逐字吐出
            )

            # 初始化一个空字符串，用来累加保存 AI 回复的完整文本
            reply_content = ""
            # end=""：打印完后不换行（默认 print 会在结尾加 \n 换行）
            # flush=True：强制刷新缓冲区。Python 为了性能默认会攒一波字符才输出到屏幕，flush=True 能保证字一旦出来立刻显示在控制台上
            print("Samantha: ", end="", flush=True)

            # 当 stream=True 时，response 变成了一个可迭代的生成器（Generator）。通过 for 循环一个个获取推送过来的数据块
            for chunk in response:
                # DeepSeek API 返回的数据结构。delta 表示“增量数据”，即新生成的这一个字或词
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    # 一边打印，一边把新字拼接到完整回复字符串中
                    print(content, end="", flush=True)
                    reply_content += content
            print() # 换行

            # 记录她说的话并保存到硬盘
            # 把 Samantha 刚刚说的话，以 assistant 的身份追加进完整的 self.history
            self.history.append({"role": "assistant", "content": reply_content})
            # 立刻把最新的历史记录（包含刚刚的用户输入和 AI 回复）写入硬盘的 memory.json 文件中
            self._save_memory()
            
            return reply_content

        # 捕获所有可能出现的错误（网络断网、API 额度不足、Key 错误等），打印友好提示，防止整个程序直接卡死崩掉
        except Exception as e:
            print(f"\n[脑神经连接断开: {e}]")
            return "抱歉，我刚刚走神了..."