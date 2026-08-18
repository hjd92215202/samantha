import json
import os
from openai import OpenAI
from memory_manager import Hippocampus

class SamanthaBrain:
    def __init__(self, api_key: str, prompt_file: str = "prompt.txt", memory_file: str = "memory.json"):

        self.model_name = "deepseek-v4-flash"
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

        self.memory_file = memory_file
        
        with open(prompt_file, "r", encoding="utf-8") as f:
            self.base_prompt = f.read()

        self.hippocampus = Hippocampus(client=self.client, model=self.model_name)
            
        self.history = self._load_memory()

    def _load_memory(self):
        """从 JSON 文件读取历史记忆"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return [{"role": "system", "content": self.base_prompt}]

    def _save_memory(self):
        """将记忆保存到本地 JSON"""
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def chat(self, user_input: str) -> str:
        """思考并回答"""
        self.history.append({"role": "user", "content": user_input})
        
        # 检查是否需要触发海马体记忆巩固 (例如：当积攒的原始对话历史超过 10 条时)
        # 1 个 system + 10 个 user/assistant = 11
        if len(self.history) >= 11:
            # 触发手写的记忆提炼，压缩历史，更新长期记忆 profile.json
            self.history = self.hippocampus.consolidate_memory(self.history)

        # 动态组装超级 System Prompt (注入最新的用户事实与情感状态)
        dynamic_system_prompt = self.hippocampus.build_dynamic_system_prompt(self.base_prompt)

        # 替换当前用于发给大模型的 System 消息
        active_messages = [{"role": "system", "content": dynamic_system_prompt}] + self.history[1:]

        try:
            response = self.client.chat.completions.create(
                model="deepseek-v4-flash",
                messages=active_messages,
                temperature=0.8, # 略高的温度，让她的性格更活泼、有创造力
                stream=True     # 开启流式传输，像人类说话一样逐字吐出
            )

            reply_content = ""
            # end=""：打印完后不换行（默认 print 会在结尾加 \n 换行）
            # flush=True：强制刷新缓冲区。Python 为了性能默认会攒一波字符才输出到屏幕，flush=True 能保证字一旦出来立刻显示在控制台上
            print("Samantha: ", end="", flush=True)

            for chunk in response:
                # DeepSeek API 返回的数据结构。delta 表示“增量数据”，即新生成的这一个字或词
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    # 一边打印，一边把新字拼接到完整回复字符串中
                    print(content, end="", flush=True)
                    reply_content += content
            print() # 换行

            self.history.append({"role": "assistant", "content": reply_content})
            self._save_memory()
            
            return reply_content

        # 捕获所有可能出现的错误（网络断网、API 额度不足、Key 错误等），打印友好提示，防止整个程序直接卡死崩掉
        except Exception as e:
            print(f"\n[脑神经连接断开: {e}]")
            return "抱歉，我刚刚走神了..."