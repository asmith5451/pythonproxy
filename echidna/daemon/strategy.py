from .util import defer_task, run_tasks
from .tasks import compose_tasks

def daemon_init(**kwargs):
    """ Return the composed tasks as a callable. """
    return compose_tasks(kwargs)
