import signal
from echidna.pidfile import pidfile

def resume(nsignal, frame):
    print("next step")

signal.signal(signal.SIGINT, resume)

with pidfile('test.pid'):
    signal.pause()
