from fastapi import APIRouter, Depends, BackgroundTasks
from dependencies import get_cache
from gameplay.wordguess import create_game, play_game_loop
from pydantic import BaseModel

router = APIRouter(
    prefix='/api',
    tags=["play"],
    dependencies=[Depends(get_cache)]
)



@router.get('/')
async def index():
    return "<h1>Hello!</h1>"



@router.get('/start')
async def play(cache = Depends(get_cache)):
    cache = get_cache()
    new_game = create_game(cache)
    return new_game


class Guess(BaseModel):
    game_token: str
    guess: str



@router.post('/guess')
async def make_guess(
    guess: Guess, 
    background_tasks: BackgroundTasks, 
    cache = Depends(get_cache)
):
    cache = get_cache()
    game_node = cache.get(guess.game_token)

    # TODO: Better Error Handling
    if not game_node:
        return {"error": "invalid game token"}
    
    background_tasks.add_task(cache.update_games)
    payload = play_game_loop(guess.guess, game_node)
    
    return payload

