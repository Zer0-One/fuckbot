import random

ANSWERS = [
    "of course not you idiot",
    "sure, why not",
    "do i look like an oracle to you?",
    "yes, obviously",
    "no",
    "yes",
    "literally kys",
    "absolutely haram",
    "idk, probably",
    "is grass green? is the sky blue? is taiwan numbah wan?"
]

def is_question(msg):
    m = msg.lower()

    if (m.startswith("can ") or
        m.startswith("could ") or
        m.startswith("do ") or
        m.startswith("does ") or
        m.startswith("is ") or
        m.startswith("may ") or
        m.startswith("shall ") or
        m.startswith("should ") or
        m.startswith("would ") or
        m.startswith("will ")):
            return True

    return False

def answer():
    i = random.randint(1, len(ANSWERS) - 1)

    return ANSWERS[i]
