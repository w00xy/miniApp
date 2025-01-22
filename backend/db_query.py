from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Any
from sqlalchemy import select, delete, update, func
from models import User, Task, async_session
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, ConfigDict
from models import Base, Task

P = ParamSpec("P")
R = TypeVar("R")

def using_session(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        async with async_session() as session:
            kwargs["session"] = session # Передаем сессию как именованный аргумент
            return await func(*args, **kwargs)
  
    return wrapper



class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    user: int
    
    model_config=ConfigDict(from_attributes=True)

@using_session
async def add_user(username: str, tg_id: int, session: AsyncSession):
    user = await session.scalar(select(User).where(User.username == username))

    if user:
        return user

    new_user = User(
        tg_id=tg_id,
        username=username
    )
    
    await session.add(new_user)
    await session.commit()
    await session.refresh()
    return new_user
    

@using_session
async def get_tasks(user_id: int, session: AsyncSession):
    tasks = await session.scalars(
        select(Task).where(Task.user == user_id, Task.completed == False)
    )

    serialized_tasks = [
        TaskSchema.model_validate(t).model_dump() for t in tasks
    ]


@using_session
async def get_completed_tasks_amount(user_id: int, session: AsyncSession):
    return await session.scalar(
        select(func.count(Task.id))
        .where(Task.completed == True)
        .where(Task.user == user_id)
    )
