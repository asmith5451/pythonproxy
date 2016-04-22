import os
import pwd
import sys
import errno
import socket

def get_username(userid):
    return pwd.getpwuid(userid).pw_name

def should_detach():
    """ Return `True` if the process was not started by the init process or the
        internet supervisor. Otherwise the process is already detached, and
        should not detach again.
        """
    return not (started_by_init_process() or started_by_inet_supervisor())

def started_by_init_process():
    return os.getpid() == 1

def started_by_inet_supervisor():
    return is_socket(sys.__stdin__.fileno())

def is_socket(fd):
    # TODO: find better way of checking if fd is a socket
    file_socket = socket.fromfd(fd, socket.AF_INET, socket.SOCK_RAW)
    
    try:
        file_socket.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE)
        return True
    except socket.error as exc:
        return errno.ENOTSOCK is not exc.args[0]
    except: pass

    return False
