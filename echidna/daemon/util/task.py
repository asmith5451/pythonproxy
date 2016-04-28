from inspect import getargspec

def run_all(context, tasks):
    """ Execute a series of tasks passing the relevant parameters to each.
        This effectively reduces a sequence of tasks to a single call.
    """
    for task in tasks:
        context = task(**context)

def defer(task, *args, **kwargs):
    """ Take a function and arguments and return a deferred executor. """
    def deferred():
        """ Execute the deferred function. """
        task(*args, **kwargs)
    return deferred
