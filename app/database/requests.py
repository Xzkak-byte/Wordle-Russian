from app.database.models import async_session, User
from sqlalchemy import select, desc
from app.utils import  format_score

async def set_user(t_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        if not user:
            session.add(User(tg_id=t_id, word="", lifes=6, username = name))
            await session.commit()

async def is_infinity(t_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        return user.infinity

async def change_inf(t_id, v):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        user.infinity = v
        await session.commit()

async def top(id):
    async with async_session() as session:
        result = await session.execute(
        select(User).order_by(desc(User.infinity_games * 0.5 + User.simple_games)).limit(10))
        top = result.scalars().all()
        text = "<b>Топ 10 игроков 🏆</b>\n\n"
        for i, user in enumerate(top,1):
            text += f"{i}. {user.username} - {await format_score(user.infinity_games * 0.5 + user.simple_games)} очков ⭐️\n"
        t = await get_rank(id)
        if t == 1: place = "Первом месте 🥇"
        elif t == 2 : place = "Втором месте 🥈"
        elif t == 3 : place = "Третьем месте 🥉"
        else : place = f'{await format_score(t)} месте в топе 🏆'
        text += f"<b>Вы на {place}</b>"
        return text

async def get_rank(id):
    async with async_session() as session:
        result = await session.execute(select(User).order_by(desc(User.infinity_games * 0.5 + User.simple_games)))
        all_users = result.scalars().all()
        for i, user in enumerate(all_users, start=1):
            if user.tg_id == id:
                return i  

async def change_name(t_id,name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        user.username = name
        await session.commit()

async def find_place(t_id):
    async with async_session() as session:
        user = await session.execute(select(User).where(User.tg_id == t_id))
        user = user.scalar_one_or_none()
        if user:
            result = await session.execute(select(User).order_by(desc(User.infinity_games * 0.5 + User.simple_games)))
            all_users = result.scalars().all()
            user_rank = next((i + 1 for i,u in enumerate(all_users) if u.tg_id == user.tg_id), None)
            return user_rank

async def get_name(t_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        return user.username

async def get_score(t_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        return user.infinity_games * 0.5 + user.simple_games

async def change_inf_games(t_id,v):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id)) 
        if v == -1: user.infinity_games += 1
        else: user.infinity_games = v
        await session.commit()

async def change_simple_games(t_id,v):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        if v == -1: user.simple_games += 1
        else: user.simple_games = v
        await session.commit()
    
async def get_inf_games(t_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        return user.infinity_games

async def get_simple_games(t_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        return user.simple_games

async def is_admin(t_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        return user.is_admin
    
async def change_admin(t_id,value):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == t_id))
        user.is_admin = value
        await session.commit()

async def get_all_users():
    async with async_session() as session:
        user = await session.scalars(select(User.tg_id))
        return user.all()
    
async def get_all_admins():
    async with async_session() as session:
        user = await session.scalars(select(User.tg_id).where(User.is_admin))
        return user.all()