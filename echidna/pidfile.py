"""
Copyright (c) 2016 Kickback Rewards Systems

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
import errno
from contextlib import contextmanager

class PIDFileError(Exception):
    pass

@contextmanager
def pidfile(path):
    write_pidfile(path)
    yield
    remove_pidfile(path)

def write_pidfile(path):
    if os.path.isfile(path):
        raise PIDFileError('PID file already exists')
    
    with open(path, 'w', 0o644) as file:
        file.write('{:d}'.format(os.getpid()))

def remove_pidfile(path):
    if not os.path.isfile(path):
        raise PIDFileError('PID file does not exist.')
    
    if not os.getpid() == read_pidfile(path):
        raise PIDFileError('The PID file is not for this process.')
    
    os.remove(path)

def read_pidfile(path):
    with open(path, 'r') as file:
        return int(file.readline().strip())
