from .tasks import compose_all_tasks
from .util.task import defer

def deferred_daemonize(**kwargs):
    """ Return the composed tasks as a callable. """
    return defer(compose_all_tasks, kwargs)

def daemonize(**kwargs):
    """ compose tasks """
    compose_all_tasks(kwargs)
