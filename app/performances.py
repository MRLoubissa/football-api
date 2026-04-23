
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.database import get_connection
from app.auth import get_current_user

router = APIRouter(prefix="/performances", tags=["Performances"])


class Performance(BaseModel):
    player_id: int
    goals: int
    assists: int
    matches_played: int


@router.get("/")
def get_performances(user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM performances")
    data = cursor.fetchall()

    conn.close()
    return data


@router.post("/")
def create_performance(perf: Performance, user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO performances
        (player_id, goals, assists, matches_played)
        VALUES (?, ?, ?, ?)""",
        (perf.player_id, perf.goals, perf.assists, perf.matches_played)
    )

    conn.commit()
    conn.close()

    return {"message": "Performance added"}


@router.delete("/{performance_id}")
def delete_performance(performance_id: int, user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM performances WHERE id = ?",
        (performance_id,)
    )

    conn.commit()
    conn.close()

    return {"message": "Performance deleted"}

