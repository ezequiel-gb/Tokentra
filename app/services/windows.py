"""Native installation safety and taskbar identity, without a single-instance restriction."""
import sys
from app.identity import WINDOWS_MUTEX, APP_USER_MODEL_ID

_mutex_handle = None


def initialise_windows():
    global _mutex_handle
    if sys.platform != "win32" or _mutex_handle is not None:
        return
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.windll.kernel32
    kernel.CreateMutexW.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
    kernel.CreateMutexW.restype = wintypes.HANDLE
    _mutex_handle = kernel.CreateMutexW(None, False, WINDOWS_MUTEX)
    if not _mutex_handle:
        raise RuntimeError("Windows could not create the Tokentra installation-safety handle.")
    # Windows releases this process-owned handle on exit. Other Tokentra
    # instances may open the same mutex; installers refuse while any remain.
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_USER_MODEL_ID)
