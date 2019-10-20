import trace
import traceback

import duolingo
import time


def run_duolingo():
    d = duolingo.Duolingo('addi390582', '132457')
    ret = d.buy_streak_freeze()
    return ret

from flask import Flask
app = Flask(__name__)

@app.route('/')
def homepage():
    try:
        return run_duolingo()
    except Exception as e:
        print(e)
        traceback.print_exc()
        # raw_input("Press Enter to Quit..")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


