import os
import errno

class PIDFileError(Exception):
    pass

class PIDFile():
    def __init__(self, path):
        self.path = os.path.abspath(path)

    def __enter__(self):
        return self.create()

    def __exit__(self, *exception):
        self.destroy()

    def create(self):
        try:
            write_pidfile(self.path)
        except OSError as err:
            if err.errno == errno.EEXIST:
                raise PIDFileError('PID File Already Exists')
            else:
                raise PIDFileError('Could not create PID file')
        else:
            return self

    def destroy(self):
        if not os.path.exists(self.path):
            raise PIDFileError('PID File does not exist')
        if not (os.getpid() == read_pidfile(self.path)):
            raise PIDFileError('The PID file is not to this process')
        remove_pidfile(self.path)

def write_pidfile(path):
    open_flags = (os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    open_mode = 0o644
    pidfile_fd = os.open(path, open_flags, open_mode)
    pidfile = os.fdopen(pidfile_fd, 'w')

    # FHS 3.0 section 3.15.2 on /run and PID file formats
    pid = os.getpid()
    pidfile.write('{:d}\n'.format(pid))
    pidfile.close()


def read_pidfile(path):
    pid = None
    try:
        pidfile = open(path, 'r')
    except IOError:
        pass
    else:
        line = pidfile.readline().strip()
        try:
            pid = int(line)
        except ValueError:
            pass
        pidfile.close()
    return pid

def remove_pidfile(path):
    try:
        os.remove(path)
    except OSError as exception:
        if exception.errno == errno.ENOENT:
            pass
        else:
            raise

