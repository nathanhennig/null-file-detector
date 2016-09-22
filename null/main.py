# -*- coding: utf-8 -*-
#
import argparse
from config import read_config
from scan import create_workers
import binascii
from multiprocessing import JoinableQueue


def main():

    config_dict = read_config()

    parser = argparse.ArgumentParser()

    category = parser.add_argument_group('Categories')
    category.add_argument('-c', '--categories', nargs=3,
                          metavar=('XX', 'YY', 'ZZ'), type=int,
                          help=('null character percentages that control '
                                "default categorization of files."))
    category.add_argument('-ce', '--category-extension', nargs=4,
                          metavar=('EXT', 'XX', 'YY', 'ZZ'), action='append',
                          help=('null character percentages that control '
                                "categorization of files for specified "
                                "EXTension (eg. txt, mp4, zip)"))
    category.add_argument('-c1', nargs=1, type=int, metavar='XX',
                          help=('files with null character percentage less '
                                'than this are GOOD'))
    category.add_argument('-c2', nargs=1, type=int, metavar='XX',
                          help=('files with null character percentage less '
                                'than this are DAMAGED, set to 0 to disable '
                                'this category'))
    category.add_argument('-c3', nargs=1, type=int, metavar='XX',
                          help=('files with null character percentage less '
                                'than this are BAD, set to 0 to disable '
                                'this category'))

    parser.add_argument('-n', '--null-character', nargs=1, metavar='XX',
                        type=binascii.unhexlify,
                        help="null character to scan for, must be two hex "
                        "digits (eg. 00, a1, ff)")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    args = parser.parse_args()

    for key in args.__dict__:
        if args.__dict__[key] == None:
            continue
        elif key == 'null_character':
            config_dict['null_char'] = args.__dict__[key][0]
        elif key == 'verbose':
            config_dict['verbose'] = True
        elif key == 'categories':
            config_dict['Categories']['cat1'] = args.__dict__[key][0]
            config_dict['Categories']['cat2'] = args.__dict__[key][1]
            config_dict['Categories']['cat3'] = args.__dict__[key][2]
        elif key == 'category_extension':
            for ce in args.__dict__[key]:
                ext = ce[0]
                config_dict[ext] = {}
                config_dict[ext]['cat1'] = ce[1]
                config_dict[ext]['cat2'] = ce[2]
                config_dict[ext]['cat3'] = ce[3]

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
