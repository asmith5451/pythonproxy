from inspect import getargspec

def run_tasks(context, tasks):
    """ Execute a series of tasks passing the relevant parameters to each.
        This effectively reduces a sequence of tasks to a single call.
    """
    for task in tasks:
        func_args = getargspec(task).args
        args = {key:value for key,value in context.items() if key in func_args}
        task(**args)

def defer_task(task, *args, **kwargs):
    """ Take a function and arguments and return a deferred executor. """
    def deferred():
        """ Execute the deferred function. """
        task(*args, **kwargs)
    return deferred
