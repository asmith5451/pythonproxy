import time
from echidna.daemon import daemon_init

# build daemon initializer
init = daemon_init()

try:
    # initialize daemon
    print("starting")
    init()
    print("over")
except Exception as exc:
    print(exc)

time.sleep(2)
