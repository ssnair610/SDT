import subprocess
import sys
import os

__home__ = os.path.dirname(__file__)

if __name__ == '__main__':
    while True:
        try:
            subprocess.call(("python", "-u", f"{__home__}/listen.py"))
            subprocess.call(("python", '-u', f"{__home__}/process.py"))
            subprocess.call(("python", '-u', f"{__home__}/analyze.py"))
        except KeyboardInterrupt:
            break