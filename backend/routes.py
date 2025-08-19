from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Body, status
from pydantic import BaseModel, EmailStr, Field
from uuid import uuid4, UUID

app = FastAPI()


users_db = {}
workouts_db = {}
exercises_db = {}
progress_db = {}
nutrition_db = {}
chat_history_db = {}


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    fitness_goals: Optional[str] = None
    medical_conditions: Optional[str] = None
    activity_level: Optional[str] = None

class WorkoutPlan(BaseModel):
    id: UUID
    user_id: UUID
    plan_name: str
    difficulty_level: str
    duration: int
    target_muscle_groups: List[str]
    exercises_list: List[UUID]

class Exercise(BaseModel):
    id: UUID
    exercise_name: str
    category: str
    equipment_needed: Optional[str] = None
    difficulty: str
    instructions: str
    target_muscles: List[str]

class ProgressEntry(BaseModel):
    id: UUID
    user_id: UUID
    workout_id: UUID
    date: str
    exercises_completed: List[UUID]
    sets: int
    reps: int
    weights: float
    duration: int
    calories_burned: float

class NutritionEntry(BaseModel):
    id: UUID
    user_id: UUID
    date: str
    meals: List[str]
    calories: float
    macronutrients: dict

class ChatRequest(BaseModel):
    user_id: UUID
    question: str

class ChatResponse(BaseModel):
    response: str


@app.post("/auth/register")
def register(user: UserRegister):
    for u in users_db.values():
        if u['username'] == user.username or u['email'] == user.email:
            raise HTTPException(status_code=400, detail="Username or email already exists")
    user_id = uuid4()
    users_db[user_id] = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "age": None,
        "weight": None,
        "height": None,
        "fitness_goals": None,
        "medical_conditions": None,
        "activity_level": None
    }
    return {"id": user_id, "username": user.username, "email": user.email}

@app.post("/auth/login")
def login(credentials: UserLogin):
    for user in users_db.values():
        if user['username'] == credentials.username and user['password'] == credentials.password:
            return {"id": user['id'], "username": user['username'], "email": user['email']}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/auth/user/{user_id}", response_model=UserProfile)
def get_user_profile(user_id: UUID):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/auth/user/{user_id}", response_model=UserProfile)
def update_user_profile(user_id: UUID, profile: UserProfile):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id].update(profile.dict(exclude_unset=True))
    return users_db[user_id]


