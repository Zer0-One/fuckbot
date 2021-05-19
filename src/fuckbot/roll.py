import logging
import random

USAGE = "```\n"
USAGE += "Usage: roll <num>d<sides>[+<add>]\n"
USAGE += "<num>        Number of dice to roll.\n"
USAGE += "<sides>      Type of dice to roll.\n"
USAGE += "<add>        An optional addition.\n"
USAGE += "\nNotes: Supplied values must be positive integers."
USAGE += "```"

def roll(rolldef):
    try:
        if "+" in rolldef:
            d, add = rolldef.split(sep="+")
        else:
            d = rolldef
            add = None

        if "d" not in rolldef:
            return "Input is missing a 'd' delimiter." + USAGE

        num, sides = d.split(sep='d')
        if int(num) <= 0 or int(sides) <= 0:
            return "Supplied values must be greater than 0." + USAGE

        total = 0
        ret = "```\n"

        for i in range(int(num)):
            val = random.randint(1, int(sides))
            ret += f"[Roll {i+1}] = {val}\n"
            total += val

        if add:
            ret += f"\n[Add] = {add}\n"
            total += int(add)

        ret += f"\n[Total] = {total}\n```"

        if len(ret) > 2000:
            ret = "Roll output too long to fit in one message.\n"

        return ret

    except Exception as e:
        logging.debug(f"roll command encountered an exception: {e}")
        return USAGE
