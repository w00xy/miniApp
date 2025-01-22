from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db_query import *
from models import *
from pydantic import BaseModel
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


@app.get("api/tasks/tg_id")
async def tasks(username: str, tg_id: int):
    user = await add_user(username, tg_id)
    
    return await get_tasks(user.id)
    
    
@app.get("api/main/{tg_id}")    
async def profile(username: str, tg_id: int):
    user = await add_user(username, tg_id)
    completed_amount = await get_completed_tasks_amount(user.id)
    
    return {"completedTasksAmount": completed_amount}
    
    

# # Зависимость для получения сессии базы данных
# async def get_db_session():
#     async with async_session() as session:
#         yield session


# class UserCreate(BaseModel):
#     username: str
#     tg_id: int
    

# class UserResponse(BaseModel):
#     id: int
#     username: str
#     tg_id: int
    
    
# class TaskCreate(BaseModel):
#     title: str
#     description: str
    
    
# class TaskResponse(BaseModel):
#     id: int
#     title: str
#     description: str
#     completed: bool
#     user_id: int
    
    
# class TaskUpdate(BaseModel):
#     title: str | None = None
#     description: str | None = None
#     completed: bool | None = None
    
        

# @app.get("/")
# def root():
#     return {"Started": True}

# @app.post("/users/", response_model=UserResponse, status_code=201)
# async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
#     new_user = User(**user.model_dump())
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)
#     return UserResponse(**new_user.__dict__)


# # Получение пользователя по ID
# @app.get("/users/{user_id}", response_model=UserResponse)
# async def get_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
#     user = await db.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return UserResponse(**user.model_dump())


# # Получение всех пользователей
# @app.get("/users/", response_model=List[UserResponse])
# async def get_all_users(db: AsyncSession = Depends(get_db_session)):
#     result = await db.execute(sqlalchemy.select(User))
#     return {result.scalars().all()}

    

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
