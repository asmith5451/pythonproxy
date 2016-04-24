import time
import sys
from echidna.daemon import deferred_daemonize

# build daemon initializer
daemonize = deferred_daemonize()

try:
    daemonize()
except Exception as exc:
    print("error! {exc}".format(exc = exc))
    pass

time.sleep(10)
