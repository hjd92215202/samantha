1. 面向对象架构解耦（模块化）：把大功能（记忆管理）拆分到一个独立的文件 memory_manager.py 和类 Hippocampus 中，brain.py 只负责调度。这是大型项目开发的核心思想！
2. 列表推导式（List Comprehension）：
3. [f"- {fact}" for fact in array] 比写一个 for 循环追加列表要精简得多。
4. 字符串与对象转换（JSON 序列化）：
json.dumps(obj)：把对象变字符串（用来构造 Prompt）。
json.loads(str)：把字符串解析成字典（用来解析模型返回的 JSON）。
安全字典获取（.get()）：
result_json.get("new_user_facts", default_value)，能够有效规避因 Missing Key 导致的 KeyError 崩溃。
5. LLM 结构化输出（JSON Mode）：
response_format={"type": "json_object"}，这是 Agent 开发中让大模型100%听话输出可解析数据的核心秘诀。
