from openai import AsyncOpenAI
import os

async def format_score(score : float) -> str:
    if score.is_integer(): return "{:,}".format(int(score)).replace(",", ".")
    else: return "{:,}".format(int(score)).replace(",", ".") + ",5"
    
async def get_ai() -> str:
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("AITOKEN"),)
    completion = await client.chat.completions.create(
        model="z-ai/glm-4.5v", 
        messages=[{
                "role": "user",
                "content": "Смотри я тебя подключил к игре по Wordle ТЫ ДОЛЖЕН СЕЙЧАС ОТВЕТИТЬ ТОЛЬКО ОДНИМ СЛОВОМ,ОБСОЛЮТНО СЛУЧАЙНЫМ,ИЗ 5 БУКВ,СУЩЕСТВИТЕЛЬНОЕ,ИМЕНИТЕЛЬНЫЙ ПАДЕЖ,ЕДИНСТВЕННОЕ ЧИСЛО !!!!"}])
    return completion.choices[0].message.content

async def generate() -> str:
    return '*' * 5;
    #chances = 5
    #word = await get_ai()
    #while chances != 0 and len(word) != 5:
    #     chances -= 1
    #     word = await get_ai()
    #if len(word) != 5: word = "*****"
    #return word