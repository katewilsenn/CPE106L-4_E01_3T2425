from pydantic import BaseModel
from typing import List

class EcoAction(BaseModel):
    id: int
    action: str
    points: int

eco_actions: List[EcoAction] = [
    EcoAction(id=1, action="Biking", points=10),
    EcoAction(id=2, action="Planting a tree", points=15),
    EcoAction(id=3, action="Recycling", points=5),
]
