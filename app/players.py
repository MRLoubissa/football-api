
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.database import get_connection
from app.auth import get_current_user
from app.schemas import PlayerUpdate

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


@router.patch("/{player_id}")
def update_player(player_id: int, player: PlayerUpdate, user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
    existing_player = cursor.fetchone()

    if not existing_player:
        conn.close()
        raise HTTPException(status_code=404, detail="Player not found")

    update_data = player.model_dump(exclude_unset=True)

    fields = []
    values = []

    for key, value in update_data.items():
        fields.append(f"{key} = ?")
        values.append(value)

    values.append(player_id)

    query = f"UPDATE players SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, values)

    conn.commit()
    conn.close()

    return {"message": "Player updated"}


@router.delete("/{player_id}")
def delete_player(player_id: int, user=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM players WHERE id = ?", (player_id,))

    conn.commit()
    conn.close()

    return {"message": "Player deleted"}

