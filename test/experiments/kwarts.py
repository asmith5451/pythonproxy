import time
import sys
from echidna.daemon import build_daemon_strategy

# build daemon initializer
daemonize = build_daemon_strategy()

try:
    daemonize()
except Exception as exc:
    print("error! {exc}".format(exc = exc))
    pass

time.sleep(10)
