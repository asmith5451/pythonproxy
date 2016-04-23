from .tasks import compose_all_tasks

def build_daemon_strategy(**kwargs):
    """ Return the composed tasks as a callable. """
    return compose_all_tasks(kwargs)
