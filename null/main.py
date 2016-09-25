# -*- coding: utf-8 -*-
#

from config import read_config
from scan import create_workers
from options import parse_args
from multiprocessing import JoinableQueue
import sys


def main():

    config_dict = read_config()

    config_dict = parse_args(config_dict, sys.argv[1:])

    # initialize worker threads
    work = JoinableQueue()
    results = JoinableQueue()
    worker_list = create_workers(work, results, config_dict['null_char'])

    # begin scanning


if __name__ == '__main__':
    main()

# check for config file
#   if not present create default config file
#   load values from config file

# load command options


# output results


#
# --Categories={5,20,85}" or "-C0=5 -C2=75"
# Logging - Default output should be to STDOUT as follows:
# {Category Name}
# Full path to files, one file per line. <==[if Verbose, prefix the line path with the %null]
# <Repeat for each category>
