import os
from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
import app.keyboards as kb
from dotenv import load_dotenv
import app.database.requests as rq
from aiogram.fsm.context import FSMContext
import app.states as st
from app.utils import format_score, generate
load_dotenv()
router = Router()
CEO = list(map(int, os.getenv("CEO", "").split(",")))

@router.message(CommandStart())
async def start_bot(message : Message):
    await message.answer_photo(photo="AgACAgIAAxkBAAIKpWi_xFhV5sMmg3RQaUZvssoRJi-6AAKw_jEbtS0BSonMsR80pDmXAQADAgADeQADNgQ",caption=f"<b>Добро пожаловать в Wordle Russian, {message.from_user.first_name} !</b>\nДанный бот - копия оригинальной игры Worlde на русском языке, с возможностью изменять количество жизней через настройки и бесконечными словами, создающиеся автоматически с помощью нашего AI 🤖\nВы можете ознакомиться с правилами и остальными командами в меню.Чтобы начать можете нажать на кнопку \"Играть 🕹\"",reply_markup=kb.base_inline,parse_mode="HTML")
    await message.delete()
    await rq.set_user(message.from_user.id,message.from_user.first_name)

@router.message(F.photo)
async def photo(message : Message):
    await message.answer(message.photo[-1].file_id)

@router.message(Command("profile"))
async def comm_profile(message : Message,state : FSMContext):
    await message.delete()
    id = message.from_user.id
    if await state.get_state() != None:
        await message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    await message.answer(f"<b>Ваш текущий профиль 🥇</b>\n\nВаш никнейм : <b>{await rq.get_name(id)} 👤</b>\nВаше число очков : <b>{await format_score(await rq.get_score(id))} ⭐️</b>\nЧисло игр с обычным режимом : <b>{await format_score(await rq.get_simple_games(id))} 👾</b>\nЧисло игр с бесконечностью : <b>{await format_score(await rq.get_inf_games(id))} ♾️</b>",parse_mode="HTML",reply_markup=kb.base_inline)

@router.message(Command("top"))
async def comm_top(message : Message,state : FSMContext):
    await message.delete()
    id = message.from_user.id
    if await state.get_state() != None:
        await message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    await message.answer(await rq.top(id),parse_mode="HTML")

@router.message(Command("edit_name"))
async def comm_edit_name(message : Message, state : FSMContext):
    await message.delete()
    if await state.get_state() != None:
        await message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    await state.set_state(st.Edit_name.name)
    await message.answer("Скиньте следуйщим сообщением ваш новый ник 🗣\nГлавное правило чтобы длинна не превышала 10 букв ⛔️" )

@router.message(Command("settings"))
async def comm_settings(message : Message,state : FSMContext):
    await message.delete()
    if await state.get_state() != None:
        await message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    if await rq.is_infinity(message.from_user.id): await message.answer("На данный момент у вас включена опция бесконечных жизней, желаете выключить ее ?",reply_markup=kb.settings_if_6) 
    else: await message.answer("На данный момент у вас 6 жизней,но вы можете изменить его на бесконечность, желаете изменить ?",reply_markup=kb.settings_if_inf)

@router.message(Command("id"))
async def comm_id(message : Message):
    await message.delete()
    await message.answer(f"Ваш персональный Telegram ID : <b>{message.from_user.id}</b>",parse_mode="HTML")

@router.message(Command("connect"))
async def connect_with_administration(message : Message,state : FSMContext):
    await message.delete()
    if await state.get_state() != None:
        await message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    await message.answer("Напишите сообщение которое вы хотите отправить администрации 👨‍💻",reply_markup=kb.otmena)
    await state.update_data(id=message.from_user.id)
    await state.set_state(st.Mess_to_admin.msg)

@router.message(Command("rules"))
async def comm_rules(message : Message):
    await message.delete()
    await message.answer(
        "<b>Правила игры в Wordle:</b>\n"
        "После нажатия на кнопку «Играть 🕹», бот выберет одно случайное слово, состоящее из 5 букв. "
        "Ваша задача — угадать это слово.\n\n"
        "Вы должны отправлять реальные слова из 5 букв. Бот ответит, какие буквы подходят:\n"
        "🟥 — такой буквы нет в слове.\n"
        "🟨 — буква есть, но в другом месте.\n"
        "🟩 — буква и её позиция верны.\n\n"
        "Игра закончится, когда вы найдёте все 5 букв.\n"
        "Удачи, игроки! 🍀",
        parse_mode="HTML",reply_markup=kb.play
    )

@router.message(Command("game"))
async def game(message : Message,state : FSMContext):
    await message.delete()
    id = message.from_user.id
    if await state.get_state() != None:
        await message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    msg = await message.answer("Ждем чтобы AI сделал слово... 🤖")
    word = await generate()
    if word == "*****":
        await msg.edit_text("Нам очень жаль, но что то пошло не так 🫤")
        return
    await state.set_state(st.Game)
    await state.update_data(word=word,lifes=6)
    await msg.edit_text("Игра началась ! 🎰\nМожете скидывать слова !",reply_markup=kb.out_game)

@router.message(st.Game,F.text)
async def playing(message : Message,state : FSMContext):
    text = message.text.strip().lower()
    id = message.from_user.id
    data = await state.get_data()
    word = data["word"]
    lifes = data["lifes"]
    if len(text) != 5: 
        await message.reply("Это слово не подходит ❌\nОно должно состоять из 5 букв !",reply_markup=kb.out_game)
        return
    word = word.strip().lower()
    ans = ["🟥"] * 5
    used = [False] * 5
    for i in range(5):
        if text[i] == word[i]:
            ans[i] = "🟩"
            used[i] = True
    for i in range(5):
        if ans[i] == "🟩":
            continue 
        for j in range(5):
            if not used[j] and text[i] == word[j]:
                ans[i] = "🟨"
                used[j] = True
                break
    res = "".join(ans)
    if await rq.is_infinity(id):
        if text == word:
            await state.clear()
            await rq.change_inf_games(id,-1)
            await message.answer(f"Отличная работа, ты угадал слово ! ✅\nЗа бесконечный режим у тебя <b>+0.5 ⭐️</b> Если хочешь играть еще нажми на кнопку ниже ⤵️",reply_markup=kb.base_inline,parse_mode="HTML")
            return
        await message.answer(f"Немножко не повезло !\nТвое слово: {res}",reply_markup=kb.out_game)
    else:
        if text == word:
            await state.clear()
            await rq.change_simple_games(id,-1)
            await message.answer(f"Отличная работа, ты угадал слово ! ✅\nЗа обычный режим у тебя <b>+1.0 ⭐️\n</b> Если хочешь играть еще нажми на кнопку ниже ⤵️",reply_markup=kb.base_inline,parse_mode="HTML")
            return
        lifes -= 1
        if lifes == 0:
            await message.answer(f"Твои жизни закончились, ты проиграл !\nЗагаданное слово : {word}",reply_markup=kb.base_inline)
            await state.clear()
            return
        await message.answer(f"Немножко не повезло !\nТвое слово: {res}\nОсталось жизней : {lifes}",reply_markup=kb.out_game)