import random
import string


def random_five():
    return ''.join(random.choice(string.digits) for _ in range(5))
