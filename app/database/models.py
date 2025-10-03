from sqlalchemy import BigInteger, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    infinity: Mapped[bool] = mapped_column(Boolean, default=False)
    username : Mapped[str] = mapped_column(String(10),default="**********")
    infinity_games : Mapped[int] = mapped_column(Integer,default=0)
    simple_games : Mapped[int] = mapped_column(Integer,default=0)
    is_admin : Mapped[bool] = mapped_column(Boolean,default=False)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        