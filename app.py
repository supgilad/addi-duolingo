import trace
import traceback

import duolingo
import time


def run_duolingo():
    if __name__ == '__main__':
        d = duolingo.Duolingo('addi390582', '132457')
        ret = d.buy_streak_freeze()
        print ret


def try_buy_streak():
    run_duolingo()

try:
    try_buy_streak()
except Exception as e:
    print(e)
    # traceback.print_exc()
raw_input("Press Enter to Quit..")
