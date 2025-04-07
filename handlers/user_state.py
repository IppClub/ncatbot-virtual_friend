import asyncio
USER_CHARACTERS = {}  # {user_id: character} 记录用户的角色（cache）（会优先从缓存找，缓存没有再去访问数据库，防止阻塞数据库）
USER_INPUTS = {}      # {user_id: message}  存储用户输入缓冲
USER_TASKS = {}       # {user_id: asyncio.Task}  存储用户的延迟任务
USER_TASKS_QUEUES = {} # {user_id:queue[{"user_id":user_id,"api":api,"character":character}]}存储用户的核心执行任务队列
USER_TASKS_MANAGER = {} # 每一个用户的任务管理器
USER_IMGS = {}    # 用于存放用户输入的图片url

USER_DATA_LOCK = asyncio.Lock()  # 用于保护 USER_INPUTS 和 USER_IMGS 的并发访问
USER_TASKS_LOCK = asyncio.Lock()
USER_TASKS_MANAGER_LOCK = asyncio.Lock()