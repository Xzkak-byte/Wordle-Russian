import os
from aiogram import F,Router
from aiogram.filters import Command
from aiogram.types import Message,CallbackQuery
import app.keyboards as kb
from dotenv import load_dotenv
import app.database.requests as rq
from aiogram.fsm.context import FSMContext
import app.states as st
load_dotenv()
router = Router()
CEO = list(map(int, os.getenv("CEO", "").split(",")))

@router.message(Command("admin"))
async def admin_command(message: Message,state : FSMContext):
    if await state.get_state() != None:
        await message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    if message.from_user.id in CEO: await message.answer("Здравствуйте уважаемый создатель, что желаете сделать ?", reply_markup=kb.ceo_panel)
    elif await rq.is_admin(message.from_user.id): await message.answer("Здравствуйте дорогой админ, что желаете сделать ?", reply_markup=kb.admin_panel)
    else: await message.answer("У вас нет прав для этой команды ❌")

@router.callback_query(F.data.endswith("_admin"))
async def set_admin(callback : CallbackQuery,state : FSMContext):
    await callback.answer()
    if await state.get_state() != None:
        await callback.message.answer("На данный момент вы выполняете другую опцию и не можете воспользоваться этой командой ❌")
        return
    action = callback.data
    await state.update_data(action=action)
    await callback.message.answer("Отправьте ID пользователя:",reply_markup=kb.otmena)
    await state.set_state(st.CEOState.id)

@router.callback_query(F.data.startswith("admin_change_"))
async def admin_choose_action(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    action = callback.data
    await state.update_data(action=action)
    await callback.message.answer("Отправьте ID пользователя:")
    await state.set_state(st.AdminStates.waiting_for_target_id)

@router.callback_query(F.data == "send_messages")
async def send_messages_call(callback : CallbackQuery,state : FSMContext):
    await callback.answer()
    await state.update_data(id=0)
    await callback.message.answer("Выберите кому хотите отправить сообщение 👇",reply_markup=kb.choice_message)
    await state.set_state(st.SendMessages.choice)

@router.message(st.SendMessages.choice,F.text == "Конкретному человеку 🧍")
async def choice_man(message : Message,state : FSMContext):
    await message.answer("Отправьте ID пользователя которому хотите отправить сообщение",reply_markup=kb.otmena)
    await state.set_state(st.SendMessages.id)

@router.message(st.SendMessages.id)
async def choice_man_msg(message : Message,state: FSMContext):
    try: id = int(message.text.strip())
    except Exception: 
        await message.answer("Отправьте пожалуйста реальный ID",reply_markup=kb.otmena)
        return
    await state.update_data(id=id)
    await message.answer("Теперь скиньте сообщение, которое надо отправить 💬",reply_markup=kb.otmena)
    await state.set_state(st.SendMessages.msg)

@router.message(st.SendMessages.choice)
async def choice_send_message(message : Message,state : FSMContext):
    if message.text == "Всем пользователям 👥": await state.update_data(choice=1)
    elif message.text == "Главной администрации 👨‍💻": await state.update_data(choice=3)
    elif message.text == "Всем администраторам 👤": await state.update_data(choice=4)
    else:
        await message.answer("Вы должны выбрать из вариантов ниже ❌",reply_markup=kb.otmena)
        return
    await message.answer("Теперь скиньте сообщение, которое надо отправить 💬",reply_markup=kb.otmena)
    await state.set_state(st.SendMessages.msg)

@router.message(st.SendMessages.msg)
async def send_messages(message : Message,state : FSMContext):
    data = await state.get_data()
    choice,id = data.get("choice"),data.get("id")

    if id: 
        await message.answer("Сообщение отправлено конкретному пользователю ✅")
        await state.clear()
        await message.bot.copy_message(chat_id=id,from_chat_id=message.chat.id,message_id=message.message_id)
        return
    if choice == 1: users = await rq.get_all_users()
    elif choice == 3: users = CEO
    elif choice == 4: users = await rq.get_all_admins()

    for user in users:
        try: await message.bot.copy_message(chat_id=user,from_chat_id=message.chat.id,message_id=message.message_id)
        except Exception: pass

    await message.answer("Сообщения успешно отправлены ✅")
    await state.clear()

@router.message(st.AdminStates.waiting_for_target_id)
async def admin_get_id(message: Message, state: FSMContext):
    try:
        if message.text.strip().lower() == "мой": target_id = message.from_user.id
        else : target_id = int(message.text.strip())
    except ValueError:
        await message.answer("ID должен быть числом ❌",reply_markup=kb.otmena)
        return
    await state.update_data(target_id=target_id)
    await message.answer("Теперь отправьте новое значение:")
    await state.set_state(st.AdminStates.waiting_for_value)

@router.message(st.AdminStates.waiting_for_value)
async def admin_get_value(message: Message, state: FSMContext):
    try:
        value = float(message.text.strip())
    except ValueError:
        await message.answer("Значение должно быть числом ❌",reply_markup=kb.otmena)
        return

    data = await state.get_data()
    action = data["action"]
    target_id = data["target_id"]

    if action == "admin_change_score": await rq.change_score(target_id, value)
    elif action == "admin_change_inf_games": await rq.change_inf_games(target_id, value)
    elif action == "admin_change_simple_games": await rq.change_simple_games(target_id, value)

    await message.answer("Данные успешно изменены! ✅")
    await state.clear()

@router.message(st.CEOState.id)
async def get_id_ceo(message : Message,state : FSMContext):
    text = message.text
    try:
        if message.text.strip().lower() == "мой": id = message.from_user.id
        else : id = int(message.text.strip())
    except Exception:
        await message.answer("Вы ввели неаверный ID ❌",reply_markup=kb.otmena)
        return
    action = (await state.get_data())["action"]
    if id in CEO:
        await message.answer("Вы не можете делать ничего с высшей администрацией ❌",reply_markup=kb.otmena)
        return
    if action == "set_admin": await rq.change_admin(id, True)
    else:
        if not await rq.is_admin(id):
            await message.answer("Данный пользователь не являеться админом ❌",reply_markup=kb.otmena)
            return
        await rq.change_admin(id,False)
    await message.answer(f"Работа администратора <b>{id}</b> успешно {'закончена' if action != 'set_admin' else 'начата'} ✅",parse_mode="HTML")
    if action == "set_admin": await message.bot.send_message(id,"<b>Главная администрация назначила вас на пост админа, добро пожаловать на новую должность дорогой админ 👤</b>\n\nВы можете воспользоваться вашими привелегиями с помощью команды /admin",parse_mode="HTML")
    else: await message.bot.send_message(id,"Главная администрация убрала вас из поста админа, теперь команда /admin и все ее привелегии вам недоступны ❌")
