import os
import resource

from .util import should_detach, defer_task, run_tasks, get_username, fork_then_exit
from .errors import DaemonOSEnvironmentError

def compose_tasks(settings):
    tasks = [
        set_owner,
        set_creation_mask,
        redirect_standard_io,
        sweep_process_io,
        optional_chroot_directory,
        optional_prevent_core_dump,
        detach_or_continue_process]
    return defer_task(run_tasks, settings, tasks)

def set_owner(userid = os.getuid(), initgroups = False, groupid = os.getgid()):
    set_user(userid)
    set_group_or_groups(userid, initgroups, groupid)

def redirect_standard_io(
    stdin = os.devnull,
    stdout = os.devnull,
    stderr = os.devnull):
        print("redirect standard output")

def set_creation_mask(usermask = 0):
    """ Set file creation mask when creating a new file. """
    os.umask(usermask)

def sweep_process_io(files_preserve = []):
    print("sweep process io")

def optional_prevent_core_dump(prevent_core_dump = True):
    if prevent_core_dump:
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

def set_working_directory(working_directory = "/"):
    os.chdir(working_directory)

def optional_chroot_directory(chroot_directory = None):
    if chroot_directory:
        os.chdir(chroot_directory)
        os.chroot(chroot_directory)

def detach_or_continue_process(detach = should_detach()):
    if(detach):
        fork_then_exit(error_message = "failed first fork")
        os.setsid()
        fork_then_exit(error_message = "failed second fork")

def set_user(userid):
    """ Set the user the process runs as. """
    os.setuid(userid)

def set_group_or_groups(userid, initgroups, groupid):
        """ If we have permissions to set all the groups """
        try:
            set_groups(userid, groupid) if initgroups else set_group(groupid)
        except Exception as exc:
            raise DaemonOSEnvironmentError(
                "Unable to change process group ({exc})".format(exc=exc)
            ) from exc

def set_group(groupid):
    """  """
    os.setgid(groupid)

def set_groups(userid, groupid):
        os.initgroups(get_username(userid), groupid)
