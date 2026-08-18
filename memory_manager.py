import json
import os
import re
from openai import OpenAI

class Hippocampus:
    """
    海马体（Memory Manager）：负责长期记忆的存储、提取、自我反思与记忆巩固
    """
    def __init__(self, model: str, client: OpenAI, profile_file: str = "profile.json"):
        self.client = client
        self.profile_file = profile_file
        self.model = model
        # 初始化或加载长期记忆结构
        self.profile = self._load_profile()

    def _load_profile(self) -> dict:
        """加载长期画像与心声"""
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[海马体警告: 无法读取 profile.json，将重新创建: {e}]")
        
        # 默认的长期记忆结构
        return {
            "user_facts": [],          # 关于用户的客观事实列表 (例如: ["喜欢科幻电影", "住在上海"])
            "samantha_feelings": "对我来说，他是一个刚认识的新朋友，我对他的生活充满好奇。", # 心理状态
            "summary_of_past": "我们刚刚认识，开始了第一次交流。" # 过去事件大纲
        }

    def save_profile(self):
        """保存长期记忆到硬盘"""
        with open(self.profile_file, "w", encoding="utf-8") as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)

    def build_dynamic_system_prompt(self, base_prompt: str) -> str:
        """
        动态组装 System Prompt：
        将基础性格 (prompt.txt) + 长期记忆 (profile.json) 动态熔炼成一个超级 Prompt
        """
        facts_str = "\n".join([f"- {fact}" for fact in self.profile["user_facts"]]) if self.profile["user_facts"] else "- 暂无记录"
        
        dynamic_prompt = f"""{base_prompt}

========================================
【你脑海中关于用户的记忆 (User Profile)】
{facts_str}

【你对他的内心情感与印象 (Your Emotional State)】
{self.profile["samantha_feelings"]}

【你们过去经历的事物摘要 (Past Summary)】
{self.profile["summary_of_past"]}
========================================
注意：以上是你大脑深处的记忆，请自然地融入对话，不要像背书一样机械地复述它们。
"""
        return dynamic_prompt

    def consolidate_memory(self, raw_history: list) -> list:
        """
        【海马体核心逻辑：记忆巩固与自我反思】
        当对话变长时，后台调用 DeepSeek 对旧记忆进行“提炼”和“压缩”
        """
        print("\n\n🧠 [海马体正在进行自我反思与记忆整理...]")

        # 构造一个专门用来让 LLM 做总结反思的 Prompt
        reflection_prompt = f"""
你现在是 Samantha 的大脑海马体区域。请分析以下最新的对话内容，更新你的长期记忆。

【当前的长期记忆】
- 用户事实: {json.dumps(self.profile["user_facts"], ensure_ascii=False)}
- 你的感受: {self.profile["samantha_feelings"]}
- 过去摘要: {self.profile["summary_of_past"]}

【最近发生的对话】
{json.dumps(raw_history[1:], ensure_ascii=False, indent=2)}

请严格输出格式良好的 JSON，包含以下三个字段：
1. "new_user_facts": 列表(str)，结合旧事实，更新关于用户的最新客观事实（合并重复项，保持精炼，最多10条）。
2. "new_feelings": 字符串，结合最新对话，更新你(Samantha)对用户的内心情感、印象或当下的态度（1-2句话）。
3. "new_summary": 字符串，将【过去摘要】与【最近发生的对话】合并压缩成一段简短的剧情梗概（200字以内）。

注意：只返回 JSON 代码块，不要包含任何其他说明文字。
"""

        try:
            # 隐式调用一次 API，专门用于内部记忆整理
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": reflection_prompt}],
                temperature=0.3, # 降低温度，确保总结的稳定性
                response_format={"type": "json_object"} # 强制 DeepSeek 返回标准 JSON
            )

            result_json = json.loads(response.choices[0].message.content)

            # 更新内存中的记忆 (使用 .get() 方式防止 KeyError)
            self.profile["user_facts"] = result_json.get("new_user_facts", self.profile["user_facts"])
            self.profile["samantha_feelings"] = result_json.get("new_feelings", self.profile["samantha_feelings"])
            self.profile["summary_of_past"] = result_json.get("new_summary", self.profile["summary_of_past"])

            # 持久化保存到 profile.json
            self.save_profile()
            print("✨ [记忆整理完成！已更新用户画像与心理状态]")

            # 裁剪原始历史记录：保留 System Prompt + 最近倒数 4 条对话 (作为近期上下文缓冲)
            new_raw_history = [raw_history[0]] + raw_history[-4:]
            return new_raw_history

        except Exception as e:
            print(f"❌ [海马体整理记忆失败: {e}]")
            return raw_history # 如果失败，降级保持原样