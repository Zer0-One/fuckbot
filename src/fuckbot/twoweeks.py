import random

ANSWERS = [
    "TWO MORE WEEKS"
]

def is_question(msg):
    m = msg.lower()

    if("how long until" in m):
        return True

def answer():
    i = random.randint(0, len(ANSWERS) - 1)

    return ANSWERS[i]
