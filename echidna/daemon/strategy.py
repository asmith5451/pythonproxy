from .tasks import run_tasks
from .util.task import defer

def deferred_daemonize(**kwargs):
    """ Return the composed tasks as a callable. """
    return defer(run_tasks, kwargs)

def daemonize(**kwargs):
    """ compose tasks """
    run_tasks(kwargs)
