import random

class Jokes:
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

    def tell_joke(self):
        for joke_part in self.get_joke():
            yield joke_part
