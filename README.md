# virtual_friend 插件

[![IppClub](https://img.shields.io/badge/I%2B%2B%E4%BF%B1%E4%B9%90%E9%83%A8-%E8%AE%A4%E8%AF%81-11A7E2?logo=data%3Aimage%2Fsvg%2Bxml%3Bcharset%3Dutf-8%3Bbase64%2CPHN2ZyB2aWV3Qm94PSIwIDAgMjg4IDI3NCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWw6c3BhY2U9InByZXNlcnZlIiBzdHlsZT0iZmlsbC1ydWxlOmV2ZW5vZGQ7Y2xpcC1ydWxlOmV2ZW5vZGQ7c3Ryb2tlLWxpbmVqb2luOnJvdW5kO3N0cm9rZS1taXRlcmxpbWl0OjIiPjxwYXRoIGQ9Im0xNDYgMzEgNzIgNTVWMzFoLTcyWiIgc3R5bGU9ImZpbGw6I2Y2YTgwNjtmaWxsLXJ1bGU6bm9uemVybyIvPjxwYXRoIGQ9Im0xNjkgODYtMjMtNTUgNzIgNTVoLTQ5WiIgc3R5bGU9ImZpbGw6I2VmN2EwMDtmaWxsLXJ1bGU6bm9uemVybyIvPjxwYXRoIGQ9Ik0yNiAzMXY1NWg4MEw4MSAzMUgyNloiIHN0eWxlPSJmaWxsOiMwN2ExN2M7ZmlsbC1ydWxlOm5vbnplcm8iLz48cGF0aCBkPSJNMTA4IDkydjExMmwzMS00OC0zMS02NFoiIHN0eWxlPSJmaWxsOiNkZTAwNWQ7ZmlsbC1ydWxlOm5vbnplcm8iLz48cGF0aCBkPSJNMCAyNzR2LTUyaDk3bC0zMyA1MkgwWiIgc3R5bGU9ImZpbGw6I2Y2YTgwNjtmaWxsLXJ1bGU6bm9uemVybyIvPjxwYXRoIGQ9Im03NyAyNzQgNjctMTA3djEwN0g3N1oiIHN0eWxlPSJmaWxsOiNkZjI0MzM7ZmlsbC1ydWxlOm5vbnplcm8iLz48cGF0aCBkPSJNMTUyIDI3NGgyOWwtMjktNTN2NTNaIiBzdHlsZT0iZmlsbDojMzM0ODVkO2ZpbGwtcnVsZTpub256ZXJvIi8%2BPHBhdGggZD0iTTE5MSAyNzRoNzl2LTUySDE2N2wyNCA1MloiIHN0eWxlPSJmaWxsOiM0ZTI3NWE7ZmlsbC1ydWxlOm5vbnplcm8iLz48cGF0aCBkPSJNMjg4IDEwMGgtMTdWODVoLTEzdjE1aC0xN3YxM2gxN3YxNmgxM3YtMTZoMTd2LTEzWiIgc3R5bGU9ImZpbGw6I2M1MTgxZjtmaWxsLXJ1bGU6bm9uemVybyIvPjxwYXRoIGQ9Im0yNiA4NiA1Ni01NUgyNnY1NVoiIHN0eWxlPSJmaWxsOiMzMzQ4NWQ7ZmlsbC1ydWxlOm5vbnplcm8iLz48cGF0aCBkPSJNOTMgMzFoNDJsLTMwIDI5LTEyLTI5WiIgc3R5bGU9ImZpbGw6IzExYTdlMjtmaWxsLXJ1bGU6bm9uemVybyIvPjxwYXRoIGQ9Ik0xNTggMTc2Vjg2bC0zNCAxNCAzNCA3NloiIHN0eWxlPSJmaWxsOiMwMDU5OGU7ZmlsbC1ydWxlOm5vbnplcm8iLz48cGF0aCBkPSJtMTA2IDU5IDQxLTEtMTItMjgtMjkgMjlaIiBzdHlsZT0iZmlsbDojMDU3Y2I3O2ZpbGwtcnVsZTpub256ZXJvIi8%2BPHBhdGggZD0ibTEyNCAxMDAgMjItNDEgMTIgMjctMzQgMTRaIiBzdHlsZT0iZmlsbDojNGUyNzVhO2ZpbGwtcnVsZTpub256ZXJvIi8%2BPHBhdGggZD0ibTEwNiA2MCA0MS0xLTIzIDQxLTE4LTQwWiIgc3R5bGU9ImZpbGw6IzdiMTI4NTtmaWxsLXJ1bGU6bm9uemVybyIvPjxwYXRoIGQ9Im0xMDggMjA0IDMxLTQ4aC0zMXY0OFoiIHN0eWxlPSJmaWxsOiNiYTAwNzc7ZmlsbC1ydWxlOm5vbnplcm8iLz48cGF0aCBkPSJtNjUgMjc0IDMzLTUySDBsNjUgNTJaIiBzdHlsZT0iZmlsbDojZWY3YTAwO2ZpbGwtcnVsZTpub256ZXJvIi8%2BPHBhdGggZD0iTTc3IDI3NGg2N2wtNDAtNDUtMjcgNDVaIiBzdHlsZT0iZmlsbDojYTgxZTI0O2ZpbGwtcnVsZTpub256ZXJvIi8%2BPHBhdGggZD0iTTE2NyAyMjJoNThsLTM0IDUyLTI0LTUyWiIgc3R5bGU9ImZpbGw6IzExYTdlMjtmaWxsLXJ1bGU6bm9uemVybyIvPjxwYXRoIGQ9Im0yNzAgMjc0LTQ0LTUyLTM1IDUyaDc5WiIgc3R5bGU9ImZpbGw6IzA1N2NiNztmaWxsLXJ1bGU6bm9uemVybyIvPjxwYXRoIGQ9Ik0yNzUgNTVoLTU3VjBoMjV2MzFoMzJ2MjRaIiBzdHlsZT0iZmlsbDojZGUwMDVkO2ZpbGwtcnVsZTpub256ZXJvIi8%2BPHBhdGggZD0iTTE4NSAzMWg1N3Y1NWgtMjVWNTVoLTMyVjMxWiIgc3R5bGU9ImZpbGw6I2M1MTgxZjtmaWxsLXJ1bGU6bm9uemVybyIvPjwvc3ZnPg%3D%3D&labelColor=fff)](https://ippclub.org)

此插件用于[ncatbot](https://docs.ncatbot.xyz/)，为基于DeepSeek大模型的AI聊天机器人，专为私聊场景优化，旨在提供更接近真人的聊天体验。

（给你的纸片人老婆完整的一生）（不是）

## 特点

### 1. 模仿真人的回复逻辑

- **可设置等待时间**：在指定的时间内，机器人会等待用户输入。如果用户有新输入，计时器会被重置，反之机器人将在超时后自动回复。所有在时限内的输入将一并发送给AI，确保上下文不丢失。
- **自然分段回复**：AI会根据对话内容自动判断分段回复，每一段之间有短暂的停顿，模拟真实人类的对话节奏，让聊天更加自然流畅。

### 2. 长期记忆

- 使用**SQLite数据库**存储用户的聊天数据，开箱即用，无需额外配置。
- 聊天记录分为**短期记忆**、**中期记忆**和**长期记忆**三个层次，层层浓缩，确保在不增加过多负担的情况下保持良好的上下文联想和长期记忆。
- 记忆池的浓缩比例可自定义，用户可以根据需要调整各部分记忆的存储和反映效果。

### 3. 角色热切换

- 支持在对话中随时通过发送命令“**切换角色 角色名**”来切换聊天机器人的角色。
- 内置多个角色设置，用户也可以自定义并添加新的角色。
- 机器人会记住用户上次的角色选择，并将其存储到数据库中。每次启动时，机器人会自动读取并将上次的角色设定存入文件缓存，避免每次都需要手动选择，也避免频繁访问数据库。
- 角色配置可以通过修改JSON文件实时生效，无需重启机器人。

### 4. NEW：识图回复

- 支持向机器人发送图片，机器人将会识别图中内容进行回复
- 识图部分使用豆包的api
- 如果保持豆包部分api配置不变，即为不开启识图功能，其余部分可以正常使用

### 5. NEW：主动发送消息

- 机器人现在可以定时向主用户发送消息。
- 用户可以设置消息发送的最短和最长间隔，机器人将在这两个时间范围内随机时长发送消息。
- 用户还可以设置静默时间段，在此时间段内，机器人将不会主动发送消息。

### 6. NEW：更好的记忆！

- 新增高级记忆功能，使用向量数据库进行记忆存储！
- bot自动提取对话事实存入向量数据库，之后进行每次对话时从向量数据库中抽取可能的相关记忆进行回复
- 自动的时间转换记忆
- 考虑到相关配置可能比较复杂，提供了这部分的开关，用户可以自行选择是否开启高级记忆功能，此操作不影响之前的记忆存储存储功能
- 事实提取的prompt在`RAG_memory/prompt`中，可以根据自己使用的体验进行修改，以适应自己的需求
- 注意高级记忆默认关闭，如果需要使用请手动开启

## 插件安装

**前置条件：**

1. 已经安装过python

2. 按照[ncatbot官方文档](https://docs.ncatbot.xyz/)的教程完成基本配置。

3. 拥有deepseek官方的api_key

**安装：**

1. 在你的ncatbot的根目录下创建`plugins`文件夹，并将本项目克隆到该目录下。

2. 安装依赖库：

   安装`requirements.txt`中的依赖项。（以下步骤供参考）


   ```bash
   # 创建虚拟环境
   python -m venv venv
   # 激活虚拟环境
   source venv/bin/activate   # Linux/Mac
   .\venv\Scripts\activate    # Windows
   # 安装依赖
   pip install -r plugins/ncatbot-virtual_friend/requirements.txt
   ```

3. 进入项目文件夹，找到`setting.ini.template`文件，复制一份并去掉后缀`.template`。打开该文件，修改其中的`API_KEY`为你的DeepSeek API密钥：

   ```ini
   API_KEY = <input_your_key>
   ```

   修改其中的`USER_ID`为你的主用户QQ号：

   ```ini
   USER_ID = <input_your_qq_id>
   ```

   其余参数可根据注释说明自行调整。

   ```ini
   [deepseek]
   API_KEY = <input_your_key>
   BASE_URL = https://api.deepseek.com

   [doubao]
   API_KEY = <input_your_key>
   BASE_URL = https://ark.cn-beijing.volces.com/api/v3

   [memory]
   # 每一组处理的临时记忆条数，也是直接联想的上下文条数，数字越大上下文直接联想越多，但会使prompt过长，建议不要太大
   TEMP_GROUP_SIZE=20 
   # 每一组处理的中期记忆条数（建议不要太大，否则记忆归档不及时）
   MID_GROUP_SIZE=5

   [task]
   #BOT等待用户回复的时间（秒）
   WAIT_TIME=5

   [host]
   # 主用户id
   USER_ID = <input_your_qq_id>

   [active-send]
   # 最长回复间隔（秒）
   max_reply_interval = 120 
   # 最短回复间隔（秒） 
   min_reply_interval = 60  
   # 静默时间段开始（小时:分钟）
   silent_start = 1:00      
   # 静默时间段结束（小时:分钟）
   silent_end = 06:00 
   ```
4. 配置高级记忆

> 该部分需要使用 ollama 运行文本向量化模型和 qdrant 向量数据库做数据存储，以下将会首先指引安装这两个服务，如果已经安装过，可以跳过前两个步骤

> 精力有限没有做多样的适配，这两个是我测试下来配置简单、成本低廉、效果又好的模型和数据库，之后会做更多模型和数据库的适配

**STEP1：ollama下载**

直接点击[下载链接](https://ollama.com/)，点击download后按照指引下载电脑对应版本即可

无需下载模型，运行的时候会自动检测下载

**STEP2：qdrant安装**

官方推荐使用docker容器，这里也只涉及这个办法，关于docker的下载和使用这里不作说明，请读者自行询问ai安装

此处附上[QDrant官方教程](https://qdrant.tech/documentation/quickstart/)

拉取镜像：

```bash
docker pull qdrant/qdrant
```

开启容器：

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```
这个指令开启了数据持久化，把你当前目录下的 qdrant_storage 文件夹挂载到容器内的 /qdrant/storage 目录中。不管你怎么重启容器，数据都会保存在本地的 qdrant_storage 文件夹中。

也可以选择不持久化，数据仅存储在容器中，如下：
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

tip:可以用浏览器访问webUI，查看和编辑数据库中数据

Web UI: localhost:6333/dashboard

**STEP3：相关配置修改**

修改settings.ini文件中的配置：

```ini
[RAG_memory]
OPEN = true
OLLAMA_BASE_URL =  http://127.0.0.1:11434
QDRANT_HOST = 172.0.0.1
QDRANT_PORT = 6333
# 向量相似度阈值，用于判断是否需要进入更新判断
SIMILARITY_THRESHOLD = 0.85 
```

当OPEN为"true"的时候才会开启高级记忆，（不要拼错），其余字符都是关闭，记得修改

端口和地址请根据你的配置自行修改，通常来说这里配置是不需要修改的

向量相似度阈值 指的是当两个文本向量相似度大于这个值时，才会进入更新判断，最大为1，最小为0

## 角色配置

角色配置文件位于`ncatbot-virtual_friend/config/characters.json`。你可以根据需要添加、删除或修改角色prompt内容。

如果添加角色，加入的需要符合以下格式：
```json
    "角色名":{
        "system_prompt": "这里是对这个角色的描述",
        "error_msg": "如果ai回复出错的时候的回复语"
    }
```
对于该json文件的修改实时生效，无需重启机器人

**一些建议：**

1. 对于角色的system_prompt，建议不要太长，因为发送给ai的prompt还有之前的记忆，过长怕超出限制。另外描述建议更多聚焦于对于角色的性格描述，用“你是”开头

2. 不要过于频繁切换角色聊天，尤其是带有完整人设和世界观的角色（这也是我的设计局限了，最开始设计数据库只想要给自己一个真实的虚拟朋友，没有考虑多角色，导致数据库存储没有区分角色，如果不同角色差异过大可能会使记忆池混乱，让ai回复质量下降）（考虑之后修改设计不同角色分开存储）（咕咕咕）

   （比如：你和可莉聊天说要去炸鱼，然后切换回魈，魈读取前面的记忆一脸懵逼不明所以，回复可能会有点怪，但ai回复通常会会避开，测试下来还不错）

## 关于记忆

1. 目前的记忆池是SQLite数据库，在数据库中存储了用户的聊天记录

2. 每一次聊天，会给ai全部的短期记忆、最近的长期记忆和全部的长期记忆

3. 短期记忆达到阈值（TEMP_GROUP_SIZE*2）时，会归档，取出最早的 TEMP_GROUP_SIZE 条记忆，交给ai总结后作为中期记忆存入中期记忆池中，并删除这些记忆

4. 中期记忆达到阈值（MID_GROUP_SIZE）时，会归档，取出最早的 MID_GROUP_SIZE - 1 条记忆，交给ai总结后作为长期记忆存入长期记忆池中，并删除这些记忆

5. 如果想要手动查看和修改记忆池里面的内容，建议下载 SQLite Studio 一类软件进行查看编辑，
可以手动插入一些描述你的长期记忆（要用命令行也行就是了）

6. 当前的设计还是比较粗糙和简陋的，欢迎提出更好的设计建议！

## 帮助命令

提供一些在聊天过程中使用的帮助命令，直接在聊天窗口发送给bot即可
1. 设置角色 角色名
2. 切换角色 角色名
3. 查看当前角色
4. 查看所有角色
5. 帮助
   
   （查看所有可以使用的命令）

## 后续开发计划（也许）

1. 由于我这个插件大部分内容算是独立于ncatbot的，（算是就用了消息收发）所以未来可能会考虑将其独立成一个单独的后端项目，用java重写接口，便于和其他的前端进行对接

2. 打的控制台log比较多比较抽象（为了调试谅解一下），然后没有本地log存储（私密马赛我懒），也许之后改改()

3. 识图、发图功能（eg.接入豆包的api，ai生图）

4. 更多更拟人化的设计（eg.时间感知、主动发送消息等）

5. 单独的前端页面，脱离ncatbot使用，更好地支持多角色聊天（壮大后宫）（不）

6. 更好的长期记忆

## 项目结构

我知道很乱你先别急 XD

```bash
ncatbot-virtual_friend/
│  main.py # 主入口
│  README.md
│  requirements.txt
│  settings.ini #配置文件
│  __init__.py
│
├─ai_utils # 和AI直接接触和处理
│  │  ai_helper.py
│  │  check_memory.py
│  │  img_handler.py # 识图
│  └─ __init__.py
│
├─config # 角色的配置
│  │  characters.json
│  │  config_loader.py
│  └─ __init__.py
│
├─handlers # 聊天处理部分
│  │  private_handler.py
│  │  task_manager.py
│  │  user_state.py
│  └─ __init__.py
│
├─RAG_memory # 高级记忆
│  │  em_ollama.py
│  │  main.py
│  │  prompt.py
│  │  qdrant.py
│  └─ __init__.py
│
└─memory # 记忆数据库操作
   │  memory.db
   │  memory_manager.py
   │  user_manager.py
   └─ __init__.py
```
## 贡献

欢迎提交贡献！如果你有任何建议、问题或改进，请通过GitHub Issues或Pull Requests来联系我。