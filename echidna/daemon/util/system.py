import os
import pwd
import sys
import errno
import socket
import resource
#import psutil
from contextlib import contextmanager

from ..errors import DaemonOSEnvironmentError

@contextmanager
def error_wrapper(message):
    """ Provide a context to allow a set of code to throw a
        DaemonOSEnvironmentError if an exception occurs, without
        having to put the messy exception handling in every function.
        """
    try:
        yield
    except Exception as exc:
        raise DaemonOSEnvironmentError(message.format(exc = exc)) from exc

def change_user(userid):
    """ Set the effective user id of the current process. """
    with error_wrapper("Unable to set the user ({exc})"):
        os.setuid(userid)

def change_file_creation_mask(mask):
    """ Set the file creation mask used by the current process. """
    with error_wrapper("Unalbe to change file creation mask ({exc})"):
        os.umask(mask)

def change_group(groupid):
    """ Set the effective group id of the current process. """
    with error_wrapper("Unable to change process group ({exc})"):
        os.setgid(groupid)

def get_username(userid):
    """ Get the username associated with the given userid. """
    return pwd.getpwuid(userid).pw_name

def change_groups(userid, groupid):
    """ Set the effective groups of the current process to the groupid and,
        and all of the groups that userid is member of.
        """
    with error_wrapper("Unable to change process groups ({exc})"):
        os.initgroups(get_username(userid), groupid)

def started_by_init_process():
    """ If the pid is 1, the process was started by the `init` user. """
    return os.getpid() == 1

def is_socket(fd):
    """ Returns `True` if the file descriptor passed is a socket. """
    # TODO: find better way of checking if fd is a socket
    file_socket = socket.fromfd(fd, socket.AF_INET, socket.SOCK_RAW)
    
    try:
        file_socket.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE)
        return True
    except socket.error as exc:
        return errno.ENOTSOCK is not exc.args[0]
    except: pass

    return False

def started_by_inet_supervisor():
    """ Return true if the current process was started by the internet
        supervisor.
        
        If the process was started by the internet supervisor process, then the
        sys.__stdin__ attribute parameter will be a socket.
        """
    return is_socket(sys.__stdin__.fileno())

def should_detach():
    """ Return `True` if the process was not started by the init process or the
        internet supervisor. Otherwise the process is already detached, and
        should not detach again.
        """
    return not started_by_init_process() or started_by_inet_supervisor()

def get_file_descriptor(stream):
    """ Return the file descriptor for the passed stream. """
    if stream is None:
        return os.open(os.devnull, os.O_RDWR)
    return stream.fileno()

def get_file_descriptors(*streams):
    """ Return a list of file descriptors for each stream passed into the
        function.
        """
    return [get_file_descriptor(stream) for stream in streams]

def redirect_stream(system_fd, target_fd):
    """ Duplicate the target descriptor, closing the system descriptor first.
        """
    os.dup2(target_fd, system_fd)

def redirect_streams(redirects):
    """ Redirect each stream to a target based on the list of tuples in the
        format (stream, target)
        """
    for stream,target in redirects:
        redirect_stream(stream, target)

def redirect_standard_io(stdin, stdout, stderr):
    """ Redirect the standard io to the passed in io. Or os.devnull. """
    with error_wrapper("Unable to redirect standard io ({exc})"):
        std_io = get_file_descriptors(sys.stdin, sys.stdout, sys.stderr)
        new_io = get_file_descriptors(stdin, stdout, stderr)
        redirects = zip(std_io, new_io)
        redirect_streams(redirects)
        return new_io

def change_working_directory(working_directory):
    """ Change the working directory of the current process. """
    with error_wrapper("Unable to change working directory ({exc})"):
        os.chdir(working_directory)

def change_root_directory(root_directory):
    """ Lock the current process to a specific folder, defaults to "/". """
    with error_wrapper("Unable to change root directory ({exc})"):
        os.chdir(root_directory)
        os.chroot(root_directory)

def close_file_descriptor_if_open(fd):
    """ Close a given file descriptor. """
    with error_wrapper("Could not close file descriptor ({exc})"):
        os.close(fd)

def get_maximum_file_descriptors(maxfd = 2048):
    """ Get the maximum number of file descriptors that the current process can
        create. Or return the default value. """
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    if hard == resource.RLIM_INFINITY:
        return maxfd
    return hard

def is_descriptor_open(fd):
    """ Determine if a file descriptor is currently open or not. """
    try:
        os.fstat(fd)
    except EnvironmentError as exc:
        return not exc.errno == errno.EBADF
    except:
        pass
    return True

def all_open_descriptors():
    # TODO: Find a reliable way to determine which descriptors are open instead
    #       of just assuming that all file descriptors possible to open are
    #       in fact open...
    # TODO: Research why the reference code reversed this list originally
    candidates = range(get_maximum_file_descriptors())
    return [fd for fd in candidates if is_descriptor_open(fd)]
    # NOTE: This is basically a brute force resolution to finding the active
    #       file descriptors.
    #       * "loop through ALL POSSIBLE descriptors"
    #       * "check if each is an active descriptor"
    # NOTE: psutil doesn't return the sys.stdin,out,err or for some reason any
    #       sockets along with it. The connections function will let me get the
    #       sockets that are open, and I assume I can append to the list of
    #       file sockets. But I still need a way to get all valid open file
    #       descriptors .
    """
    process = psutil.Process()
    open_files = process.open_files()
    connections = process.connections(kind="all")
    print("open_files: {}".format(open_files))
    print("connections: {}".format(connections))
    """

def get_target_descriptors(exclude = []):
    """ Return a list of descriptors excluding the list of descriptors passed
        in.
        """
    return [fd for fd in all_open_descriptors() if fd not in exclude]

def close_all_open_files(exclude = []):
    """ Close all open file descriptors, excluding the list of descriptors
        passed in. """
    for file_descriptor in get_target_descriptors(exclude):
        close_file_descriptor_if_open(file_descriptor)

def zero_core_dump_limits():
    """ Set the core dump limits to 0, effectively preventing the OS from being
        able to write a core dump.
        """
    with error_wrapper("Unable to set resource limit to 0 ({exc})"):
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
