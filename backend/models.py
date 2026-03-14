from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserProfile(BaseModel):
    user_id: str
    name: str
    dob: date
    gender: str
    goal: str
    weight_lb: float
    height_cm: float
    preferred_workout_intensity: Optional[str]
    sleep_target_hours: Optional[float]
    notes: Optional[str] = ""

class UpdateUserProfile(BaseModel):
    name: str
    dob: date
    gender: str
    goal: str
    weight_lb: float
    height_cm: float
    preferred_workout_intensity: Optional[str]
    sleep_target_hours: Optional[float]
    notes: Optional[str] = ""