面向对象基础：class（类）、__init__（构造方法）、self（实例指针）。
文件安全操作：with open(...) as f 上下文管理器，防止文件句柄泄漏。
JSON 序列化与反序列化：json.load()（文件转列表/字典），json.dump()（列表/字典转文件）。
列表高级切片：list[-20:] 获取末尾 20 个元素，list[0] 获取头部元素，list1 + list2 拼接。
异常捕获与稳健性：try ... except Exception as e，确保线上程序不会因偶发网络波动崩溃。
实时流式输出控制：print(..., end="", flush=True) 刷新输出缓冲区实现打字机特效。
程序标准入口：if __name__ == "__main__": 的规范写法。