import os
import sys

from .util.task import run_all
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

def run_tasks(settings):
    """ Compose all of the tasks into one task. """
    """ I am using is a task oriented approach. If any element of the task
        must happen in order, the task is consolidated. Some tasks do multiple
        things, but all do as little as possible. Using this design principle,
        it should be possible to put each task in its own thread and not worry
        about which completes first. There's some questionable features of the
        detach_or_continue_process that I am not sure would work in their own
        thread, but everything else in the list should work.
        
        Since I am dealing directly with the OS, I actually need the side
        effects of the process altering its behavior. Every function called by
        each task is essentially required to have side effects. Because of this
        it can't be totally pure, but the functions that orchestrate the tasks
        themselves can be.
        """
    run_all(settings, [
        set_owner,
        set_creation_mask,
        set_directories,
        redirect_and_sweep_io,
        optional_prevent_core_dump,
        detach_or_continue_process,
    ])

def set_owner(userid = os.getuid(), initgroups = False, groupid = os.getgid(), **kwargs):
    """ Set the effective userid of the process, then set the effective group
        or groups of the process.
        """
    change_groups(userid, groupid) if initgroups else change_group(groupid)
    change_user(userid)
    return kwargs

def set_creation_mask(usermask = 0, **kwargs):
    """ Set file creation mask when creating a new file. """
    change_file_creation_mask(usermask)
    return kwargs

def set_directories(working_directory = "/", chroot_directory = None, **kwargs):
    """ Change the root directory, and then the working directory for the
        current process.
        """
    if chroot_directory:
        change_root_directory(chroot_directory)
    change_working_directory(working_directory)
    return kwargs

def redirect_and_sweep_io(
    files_preserve = [],
    stdin = None,
    stdout = None,
    stderr = None,
    **kwargs
    ):
        """ Redirect standard io to nothing, or whatever it has been overridden
            to. Then close all file descriptors associated with the process
            except the redirected io descriptors, and any explicitly specified
            ones in the files_preserve list.
            """
        io_descriptors = redirect_standard_io(stdin, stdout, stderr)
        
        exclude = files_preserve + io_descriptors
        close_all_open_files(exclude)
        return kwargs

def optional_prevent_core_dump(prevent_core_dump = True, **kwargs):
    """ Prevent the sysem from making a core dump, unless overridden. """
    if prevent_core_dump:
        zero_core_dump_limits()
    return kwargs

def detach_or_continue_process(detach = should_detach(), **kwargs):
    """ Detach from the current process unless we are already detached. """
    if detach:
        daemon_fork()
    return kwargs
