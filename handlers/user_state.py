USER_CHARACTERS = {}  # {user_id: character} 记录用户的角色（cache）（会优先从缓存找，缓存没有再去访问数据库，防止阻塞数据库）
USER_INPUTS = {}      # {user_id: message}  存储用户输入缓冲
USER_TASKS = {}       # {user_id: asyncio.Task}  存储用户的延迟任务
