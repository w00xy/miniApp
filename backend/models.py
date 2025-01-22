from sqlalchemy import ForeignKey, String, BigInteger, Integer
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from config import Settings

engine = create_async_engine(Settings.sql, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, autoincrement="auto", primary_key=True)
    username: Mapped[str] = mapped_column(String(255), default=None)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    
    
class Task(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(Integer, autoincrement="auto", primary_key=True)
    title: Mapped[str] = mapped_column(String(255), default=None)
    description: Mapped[str] = mapped_column(String(255), default=None)
    completed: Mapped[bool] = mapped_column(default=False)
    user: Mapped[int] = mapped_column(ForeignKey('users.id',  **{"ondelete": "CASCADE"}))
    


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   
    
    