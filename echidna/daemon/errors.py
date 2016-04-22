
class DaemonError(Exception): pass
class DaemonOSEnvironmentError(DaemonError, OSError): pass
class DaemonProcessDetachError(DaemonError, OSError): pass
