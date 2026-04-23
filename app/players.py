
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.database import get_connection
from app.auth import get_current_user

router = APIRouter(prefix="/players", tags=["Players"])


class Player(BaseModel):
    name: str
    team: str


@router.get("/")
def get_players(user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()

    conn.close()

    return players


@router.post("/")
def create_player(player: Player, user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO players (name, team) VALUES (?, ?)",
        (player.name, player.team)
    )

    conn.commit()
    conn.close()

    return {"message": "Player created"}


@router.delete("/{player_id}")
def delete_player(player_id: int, user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM players WHERE id = ?", (player_id,))
    conn.commit()
    conn.close()

    return {"message": "Player deleted"}

    