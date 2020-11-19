import os
import duolingo

password = os.environ['PASSWORD']
user = os.environ['USER']


def run_duolingo():
    d = duolingo.Duolingo(user, password)
    ret = d.buy_streak_freeze()
    return ret


if __name__ == '__main__':
    print(run_duolingo())
