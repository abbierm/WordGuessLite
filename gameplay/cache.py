from collections import OrderedDict
from typing import Optional
from datetime import datetime, timezone, timedelta
import secrets
from fastapi import FastAPI
import time

MAX_SIZE = 100

class GameNode:
    def __init__(self, correct_word: str):
        self.correct_word = correct_word
        self.token: Optional[str] = None
        self.token_expiration: datetime = datetime.now(timezone.utc) + \
                                    timedelta(seconds=36000)
        self.guess_count: int = 0
        self.guesses: list[str] = []
        self.feedback: list[str] = []
        self.status: bool = True
        self.results: Optional[bool] = None
        self._add_token()


    def _add_token(self):
        self.token = secrets.token_hex(8)


    def create_payload(self, message: Optional[str] = "") -> dict:
        payload = {
            "game_token": self.token,
            "token_expiration": self.token_expiration,
            "guess_count": self.guess_count,
            "guesses": {},
            "message": message,
            "status": self.status,
            "results": None
        }
        if self.guess_count > 0:
            for i in range(self.guess_count):
                feedback_pair = {
                    "guess": self.guesses[i],
                    "feedback": self.feedback[i]
                }
                payload["guesses"][i + 1] = feedback_pair
        if self.status == False:
            payload["results"] = "won" if self.results == True else "lost"
        return payload



class GameCache:
    """ LRU cache for current wordguess games"""

    def __init__(self, app: FastAPI = None, capacity: int=MAX_SIZE):
        time.sleep(3)
        if app is not None:
            self.init_app(app)
        self.capacity = capacity
        self.cache = OrderedDict()
        self.current_size = 0

    def init_app(self, app: FastAPI):
        self.app = app

    def get(self, api_key: str) -> GameNode:
        try:
            game = self.cache[api_key]
            self.cache.move_to_end(api_key)
            return game
        except KeyError:
            return None

    def put(self, game_node: GameNode):
        if self.current_size == self.capacity:
            x = self.cache.popitem(last=False)
            self.current_size -= 1
        self.cache[game_node.token] = game_node
        self.cache.move_to_end(game_node.token)
        self.current_size += 1
       

    def remove(self, api_key):
        if api_key in self.cache:
            self.cache.popitem(api_key)
            self.current_size -= 1

    def empty(self):
        self.cache = OrderedDict()
        self.current_size = 0


    def _remove_expired(self):
        expired = []
        for game in self.cache.values():
            if game.token_expiration < datetime.now(timezone.utc):
                expired.append(game.token)
        for game_token in expired:
            self.remove(game_token)
        return


    def _remove_completed_games(self):
        complete = []
        for game in self.cache.values():
            if game.status == False:
                complete.append(game.token)
        for game_token in complete:
            self.remove(game_token)
        return


    def update_games(self):
        self._remove_expired()
        self._remove_completed_games()

