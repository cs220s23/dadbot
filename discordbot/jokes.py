import random
import redis
from abc import ABC, abstractmethod
from collections.abc import Sequence


class Jokes(ABC):
    @abstractmethod
    def get_joke(self) -> tuple:
        pass

    def tell_joke(self) -> str:
        for joke_part in self.get_joke():
            yield joke_part

    def source(self) -> str:
        return type(self).__name__


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

    def get_joke(self) -> tuple[str]:
        return random.choice(self.jokes)


class RedisJokes(Jokes):
    def __init__(self, host: str, port: int):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)

    def get_joke(self) -> Sequence[str]:
        joke_id = self.r.srandmember("jokes")
        if joke_id is None:
            return "No jokes stored in Database", "Please add jokes"
        return tuple(self.r.lrange(f"jokes:{joke_id}", 0, -1))

    def add_joke(self, joke: Sequence[str]) -> None:
        joke_id = self.r.scard("jokes") + 1
        self.r.sadd("jokes", joke_id)
        for joke_part in joke:
            self.r.rpush(f'jokes:{joke_id}', joke_part)

    def read_from_file(self, fp: str) -> None:
        for joke in FileJokes(fp).jokes:
            self.add_joke(joke)

    def __del__(self):
        self.r.close()
