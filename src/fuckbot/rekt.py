import logging
import random

replies = [
    "{} has left the server. Good riddance",
    "Don't let the door hit your ass, {}",
    "{} has left for gayer pastures"
]

def rekt(member):
    idx = random.randint(0, len(replies) - 1)

    return replies[idx].format(member)
