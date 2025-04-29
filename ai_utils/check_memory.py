# 该文件用于使用deepseek决定记忆存储相关判断
from openai import AsyncOpenAI, OpenAIError  # 处理 OpenAI 相关错误
from ..config.config_loader import get_character
import asyncio
from .ai_helper import use_ai_raw_reasoner

# 用于判断临时记忆存储
async def check_temp_memory(user_id, content) -> str:
    prompt = (
        "你是bot，请总结以下用户和你的对话，如果内容有意义（如新信息、有助于理解上下文、表明用户情绪或意图），"
        "请生成一段不超过30字的简要概括。否则，返回'无重要内容'。仅返回总结内容或者‘无重要内容’，不要返回字数"
    )
    return await use_ai_raw_reasoner(prompt, content)

# 用于判断中期记忆存储
async def check_mid_memory(user_id, content) -> str:
    prompt = (
        "你是bot，正在和该人类用户对话，请总结以下对话，生成一段50字以内的关于双方对话内容的概括。仅返回总结内容或者‘无重要内容’，不要返回字数"
    )
    return await use_ai_raw_reasoner(prompt, content)

# # 用于判断长期记忆存储
# async def check_long_memory(user_id, content) -> str:
#     prompt = (
#         "你是bot，正在和该人类用户对话，请总结以下对话，并判断其是否具有长期价值（如关于你的一些行为，用户的核心偏好、重要经历、重要承诺、"
#         "未来计划、习惯等）。如果有，请生成一段关于该对话内容和用户特点的精炼总结，不超过60字，否则仅返回'无重要内容'。"
#     )
#     return await use_ai_raw_reasoner(prompt, content)

# # 用于判断中期记忆存储
# async def check_mid_memory(user_id, content) -> str:
#     prompt = (
#         "你是一个智能助手，需要判断以下对话是否值得短期存储（中期记忆），以便在后续对话中参考。"
#         "**如果对话包含用户的近期计划、兴趣爱好、短期目标、最近的活动**，请生成50字以内的概括。"
#         "**如果内容可能在几天或几次对话后失效**，但在短期内仍然有用，也需要总结。"
#         "如果没有短期价值（如无实际信息的寒暄），返回'无重要内容'。"
#         "示例1: 用户: 我最近在学钢琴。→ 总结: 用户最近开始学习钢琴。"
#         "示例2: 用户: 今天天气不错。→ 返回: 无重要内容。"
#     )
#     return await use_ai_raw_reasoner(prompt, content)

# 用于判断长期记忆存储
async def check_long_memory(user_id, content) -> str:
    prompt = (
        "你是一个智能助手，需要判断以下对话是否具有长期价值，并进行存储。"
        "**如果内容涉及用户的核心偏好（如职业、信仰、重要习惯）、长期目标、重大经历或承诺，"
        "请生成60字以内的精炼总结**。"
        "短期或临时信息不应存入长期记忆，除非它反映了用户的稳定特征。"
        "如果判断无需存入，仅仅返回'无重要内容'，不要有多余的字符"
        "示例1: 用户: 我是一名医生，计划明年去美国进修。→ 用户是一名医生，计划明年赴美深造。"
        "示例2: 用户: 我最近喜欢听古典音乐。→ 无重要内容"
        "仅返回总结内容或者‘无重要内容’，不要返回字数"
    )
    return await use_ai_raw_reasoner(prompt, content)