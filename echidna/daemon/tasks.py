import os
import sys

from .util.task import defer, run_all
from .util.system import (
    change_user,
    change_group, change_groups,
    change_file_creation_mask,
    change_working_directory,
    change_root_directory,
    redirect_standard_io,
    close_all_open_files,
    zero_core_dump_limits,
    should_detach,
)
from .util.process import  daemon_fork

def compose_all_tasks(settings):
    """ Compose all of the tasks into one task. """
    tasks = [
        set_owner,
        set_creation_mask,
        optional_chroot_directory,
        set_working_directory,
        redirect_and_sweep_io,
        optional_prevent_core_dump,
        detach_or_continue_process,
    ]
    return defer(run_all, settings, tasks)

def set_owner(userid = os.getuid(), initgroups = False, groupid = os.getgid()):
    """ Set the effective userid of the process, then set the effective group
        or groups of the process.
        """
    change_user(userid)
    change_groups(userid, groupid) if initgroups else change_group(groupid)

def set_creation_mask(usermask = 0):
    """ Set file creation mask when creating a new file. """
    change_file_creation_mask(usermask)

def set_working_directory(working_directory = "/"):
    """ Change the working directory of the process to the specified directory.
        """
    change_working_directory(working_directory)

def optional_chroot_directory(chroot_directory = None):
    """ Change the root directory of the process to the specified directory """
    if chroot_directory:
        change_root_directory(chroot_directory)

def redirect_and_sweep_io(
    files_preserve = [],
    stdin = None,
    stdout = None,
    stderr = None,
    ):
        """ Redirect standard io to nothing, or whatever it has been overridden
            to. Then close all file descriptors associated with the process
            except the redirected io descriptors, and any explicitly specified
            ones in the files_preserve list.
            """
        io_descriptors = redirect_standard_io(stdin, stdout, stderr)
        
        exclude = files_preserve + io_descriptors
        close_all_open_files(exclude)

def optional_prevent_core_dump(prevent_core_dump = True):
    """ Prevent the sysem from making a core dump, unless overridden. """
    if prevent_core_dump:
        zero_core_dump_limits()

def detach_or_continue_process(detach = should_detach()):
    """ Detach from the current process unless we are already detached. """
    if detach:
        daemon_fork()
