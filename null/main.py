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
import defaults


def main():

    config_dict = read_config()

    config_dict = parse_args(config_dict, sys.argv[1:])

    # Create timestamp string for logging to file(s)
    # yyyymmddhhmm (eg. 201610041359)
    config_dict['timestamp'] = time.strftime('%Y%m%d%H%M')

    # Initialize worker threads
    work = JoinableQueue()
    results = JoinableQueue()
    worker_list = create_workers(
        work, results, config_dict['null_char'])

    # Begin scanning
    if not config_dict['batch']:
        print("Scanning files...")
    if not os.path.isdir(config_dict['start_directory']):
        print("Error: {} is not a directory".format(
            config_dict['start_directory']))
        sys.exit()

    scanned_files = []
    files = []
    directories = []

    # Use target if available or the start_directory value,
    # which is guarenteed to have a value
    if config_dict.get('target'):
        directories.append(config_dict['target'])
    else:
        directories.append(config_dict['start_directory'])

    try:
        directories[0] = directories[0].decode('unicode-escape')
    except UnicodeEncodeError:
        pass

    # Process each directory and file
    # If recursive is not true, only the first directory will be processed
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

    # Output results
    sort_print(scanned_files, config_dict)

    # Wait for input before closing
    # (prevents console window from auto closing when opened from a gui)
    if not config_dict['batch']:
        print('')
        print('Press enter to close.')
        raw_input()

if __name__ == '__main__':

    # Record directory that script is located in so that config and log files
    # are generated and read from that directory
    defaults.Default.EXEC_DIRECTORY = os.path.dirname(
        os.path.realpath(__file__))

    freeze_support()
    main()
