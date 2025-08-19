from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import uuid4, UUID

app = FastAPI()


users_db = {}
workouts_db = {}

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

@app.get("/")
def read_root():
    return {"Hello": "World"}
    
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

@app.post("/workouts", response_model=WorkoutPlan)
def create_workout(workout: WorkoutPlan):
    workout_id = uuid4()
    workout_data = workout.dict()
    workout_data['id'] = workout_id
    workouts_db[workout_id] = workout_data
    return workout_data

@app.get("/workouts/{workout_id}", response_model=WorkoutPlan)
def get_workout(workout_id: UUID):
    workout = workouts_db.get(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@app.put("/workouts/{workout_id}", response_model=WorkoutPlan)
def update_workout(workout_id: UUID, workout: WorkoutPlan):
    if workout_id not in workouts_db:
        raise HTTPException(status_code=404, detail="Workout not found")
    workouts_db[workout_id].update


@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: UUID):
    if workout_id not in workouts_db:
        raise HTTPException(status_code=404, detail="Workout not found")
    del workouts_db[workout_id]
    return {"detail": "Workout deleted"}
