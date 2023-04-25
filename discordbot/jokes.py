import random
import redis
from abc import ABC, abstractmethod


class Jokes(ABC):
    @abstractmethod
    def get_joke(self) -> tuple:
        pass

    def tell_joke(self) -> str:
        for joke_part in self.get_joke():
            yield joke_part


class FileJokes(Jokes):
    def __init__(self, joke_src: str):
        self.joke_src = joke_src
        self.jokes = []
        with open(joke_src) as joke_file:
            joke = []
            for line in joke_file:
                line = line.strip()
                if line != "":
                    joke.append(line)
                else:
                    self.jokes.append(tuple(joke))
                    joke.clear()

    def get_joke(self):
        return random.choice(self.jokes)


class RedisJokes(Jokes):
    def __init__(self, host: str, port: int):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)

    def get_joke(self):
        joke_id = self.r.srandmember("jokes")
        print(f'joke_id={joke_id}')
        if joke_id is None:
            return ("No jokes stored in Database","Please add jokes")
        return tuple(self.r.lrange(f"jokes:{joke_id}", 0, -1))
