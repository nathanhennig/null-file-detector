# -*- coding: utf-8 -*-

from config import read_config
from scan import create_workers, scan, scan_target
from options import parse_args
from multiprocessing import JoinableQueue
from multiprocessing import freeze_support
from file import File
from sortprint import sort_print
import sys
import os
import time


def main():

    config_dict = read_config()

    config_dict = parse_args(config_dict, sys.argv[1:])

    # create timestamp string for logging to file(s)
    # yyyymmddhhmm (eg. 201610041359)
    config_dict['timestamp'] = time.strftime('%Y%m%d%H%M')

    # initialize worker threads
    work = JoinableQueue()
    results = JoinableQueue()
    worker_list = create_workers(
        work, results, config_dict['null_char'])

    # begin scanning
    print("Scanning files...")
    if not os.path.isdir(config_dict['start_directory']):
        print("Error: {} is not a directory".format(
            config_dict['start_directory']))
        sys.exit()

    scanned_files = []
    files = []
    directories = []

    # use target if available or the start_directory value,
    # which is guarenteed to have a value
    if config_dict.get('target'):
        directories.append(config_dict['target'])
    else:
        directories.append(config_dict['start_directory'])

    # process each directory and file
    # if recursive is not true, only the first directory will be processed
    while directories:
        target_dir = directories.pop()
        files, directories = scan_target(target_dir, files, directories)
        while files:
            target_file = File(files.pop())
            target_file.null_count = scan(
                target_file.name, work, results)
            scanned_files.append(target_file)

        if config_dict['recursive'] is False:
            break

    # output results
    sort_print(scanned_files, config_dict)

    # wait for input before closing
    # (prevents console window from auto closing when opened from a gui)
    print('')
    print('Press enter to close.')
    raw_input()

if __name__ == '__main__':
    freeze_support()
    main()
