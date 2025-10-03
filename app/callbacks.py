import os
from aiogram import F,Router
from aiogram.types import CallbackQuery,Message
from dotenv import load_dotenv
import app.database.requests as rq
from aiogram.fsm.context import FSMContext
import app.states as st
import app.keyboards as kb
from app.utils import generate
load_dotenv()
router = Router()
CEO = list(map(int, os.getenv("CEO", "").split(",")))

@router.callback_query(F.data == "settings")
async def settings1(callback : CallbackQuery,state : FSMContext):
    await callback.answer()
    if await state.get_state() != None:
        await callback.message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    if await rq.is_infinity(callback.from_user.id):
        await callback.message.answer("На данный момент у вас включена опция бесконечных жизней, желаете выключить ее ?",reply_markup=kb.settings_if_6) 
    else:
        await callback.message.answer("На данный момент у вас 6 жизней,но вы можете изменить его на бесконечность, желаете изменить ?",reply_markup=kb.settings_if_inf)

@router.callback_query(F.data == "start_play")
async def start_play(callback : CallbackQuery,state : FSMContext):
    await callback.answer()
    id = callback.from_user.id
    if await state.get_state() != None:
        await callback.message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    await state.set_state(st.Game)
    msg = await callback.message.answer("Ждем чтобы AI сделал слово... 🤖")
    word = await generate()
    await state.set_data(word=word,lifes=6)
    await msg.edit_text("Игра началась ! 🎰\nМожете скидывать слова !",reply_markup=kb.out_game)

@router.callback_query(F.data == "nothing")
async def nothing(callback : CallbackQuery,state : FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.clear()

@router.callback_query(F.data == "turn_on_inf")
async def turn_on_inf(callback : CallbackQuery,state : FSMContext):
    await callback.answer()
    if await state.get_state() != None:
        await callback.message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    await rq.change_inf(callback.from_user.id, True)
    await callback.message.delete()
    await callback.message.answer("Теперь у вас бесконечные жизни ! ♾️",reply_markup=kb.base_inline)

@router.callback_query(F.data == "turn_off_inf")
async def turn_off_inf(callback : CallbackQuery,state : FSMContext):
    await callback.answer()
    if await state.get_state() != None:
        await callback.message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    await rq.change_inf(callback.from_user.id, False)
    await callback.message.delete()
    await callback.message.answer("Теперь у вас 6 жизней !",reply_markup=kb.base_inline)

@router.callback_query(F.data == "quit")
async def quit(callback : CallbackQuery,state : FSMContext):
    await callback.answer()
    id = callback.from_user.id
    if await state.get_state() != "Game":
        await callback.message.reply("На данный момент вы не играете ❌")
        return
    word = (await state.get_data())["word"]
    await callback.message.answer(f"Игра закончилась, ранее загаданное слово -> {word}",reply_markup=kb.base_inline)
    await state.clear()

@router.callback_query(F.data == "rules")
async def rules(callback: CallbackQuery,state : FSMContext):
    await callback.answer()
    if await state.get_state() != None:
        await callback.message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    await callback.message.answer(
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

@router.message(st.Edit_name.name)
async def edit_name(message : Message, state : FSMContext):
    text = message.text
    if len(text) > 10:
        await message.reply("Ваш ник не должен привышать 10 букв ⛔️")
        return
    if text.lower() in ["wordle ceo", "ceo wordle"]:
        if await rq.is_admin(message.from_user.id):
            await rq.change_name(message.from_user.id,text)
            await state.clear()
            await message.reply(f"Ваш ник успешно изменен ✅\nВаш новый ник : <b>{text}</b>\nВоспользовано разрешение админа 👤",parse_mode="HTML")
        else: await message.reply("Вы не можете поставить имя создателя ❌")
        return
    await rq.change_name(message.from_user.id,text)
    await state.clear()
    await message.reply(f"Ваш ник успешно изменен ✅\nВаш новый ник : <b>{text}</b>",parse_mode="HTML")

@router.message(st.Mess_to_admin.msg)
async def wait_message_admin(message : Message,state : FSMContext):
    data = await state.get_data();
    msg = f"<b>Вам пришло новое сообщение от пользователя 💬</b>\n\n<i>{message.text}</i>ID пользователя: {data['id']}"
    for ceo in CEO: await message.bot.send_message(ceo,msg,parse_mode="HTML")
    await message.answer("Ваше сообщение успешно отправлено администрации ✅")
    await state.clear()