# -*- coding: utf-8 -*-

from functools import partial
from multiprocessing import Process
import multiprocessing as mp
import sys
import os
import platform

# https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
# Module multiprocessing is organized differently in Python 3.4+
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

bit64 = platform.architecture()[0].startswith('64')

if sys.platform.startswith('win') and bit64:
    # First define a modified version of Popen.
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen

def read_in_chunks(file_object, chunk_size=4 * 1024 * 1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def do_work(in_queue, out_queue, null_char):

    while True:
        null = 0
        item = in_queue.get()
        # process
        for byte in item:
            if byte == null_char:
                null = null + 1
        out_queue.put(null)
        in_queue.task_done()


def scan(name, work_queue, result_queue):

    # produce data
    try:
        with open(name, 'rb') as f:
            for i in read_in_chunks(f):
                work_queue.put(i)
    except IOError:
        return 'Error'
    else:
        work_queue.join()

        # get the results
        null_count = sum([result_queue.get()
                          for i in range(result_queue.qsize())])

        return null_count


def create_workers(work_queue, result_queue, null_char=b'\x00'):

    num_workers = mp.cpu_count() - 1
    if num_workers < 1:
        num_workers = 1

    # start workers
    worker_list = []
    for i in range(num_workers):
        t = Process(target=do_work, args=(work_queue, result_queue, null_char))
        worker_list.append(t)
        t.daemon = True
        t.start()

    return worker_list

def scan_target(path, files, directories):

    path = os.path.abspath(path)

    if not os.path.isdir(path):
        files.append(path)
        return files, directories

    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            directories.append(entry_path)
        else:
            files.append(entry_path)

    return files, directories
