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



def main():

    config_dict = read_config()

    config_dict = parse_args(config_dict, sys.argv[1:])

    # initialize worker threads
    work = JoinableQueue()
    results = JoinableQueue()
    worker_list = create_workers(
        work, results, config_dict['null_char'])

    # begin scanning
    if not os.path.isdir(config_dict['start_directory']):
        print("Error: {} is not a directory")
        sys.exit()

    scanned_files = []
    files = []
    directories = []

    if config_dict.get('target') and len(config_dict['target']) > 0:
        while config_dict['target']:
            target = config_dict['target'].pop()
            files, directories = scan_target(target_dir, files, directories)
    else:
        directories.append(config_dict['start_directory'])

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

if __name__ == '__main__':
    freeze_support()
    main()
