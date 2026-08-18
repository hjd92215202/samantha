工作记忆（Short-term Memory）：最近几句的原话对话（逐字逐句）。
事实记忆（User Profile）：关于用户的客观事实（如：“喜好”、“职业”、“性格”）。
事件总结（Episodic Memory）：将过去聊过的大段对话，压缩提炼成简短的剧情梗概。
心理状态（Emotional State）：Samantha 对你的看法和当下的情感变化（《Her》的精髓！）。

[ 用户输入 ] ──► 追加到短期对话历史 (Short-term History)
                       │
                       ▼
         ┌───────────────────────────┐
         │ 触发检查: 历史记录是否超过 6 轮? │
         └─────────────┬─────────────┘
                       │
             ┌─────────┴─────────┐
             │ 是                 │ 否
             ▼                   ▼
    【手写海马体整理机制】        直接拼接 System Prompt
    1. 提取大段旧对话
    2. 调用 DeepSeek 执行“反思”
    3. 更新 profile.json:
       - 提取用户的最新事实
       - 更新 Samantha 的心理感受
       - 压缩旧对话为剧情梗概
    4. 裁剪 Raw History (释放 Token)
             │
             └─────────┬─────────┘
                       ▼
        【动态组装超级 System Prompt】
        Base Prompt + 用户事实 + Samantha心声 + 剧情总结
                       │
                       ▼
            发送给 DeepSeek 生成回答