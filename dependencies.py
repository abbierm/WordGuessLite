from gameplay.cache import GameCache


games_cache = GameCache()

def get_cache() -> GameCache:
    return games_cache