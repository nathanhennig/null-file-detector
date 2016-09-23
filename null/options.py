# -*- coding: utf-8 -*-
#
import argparse
import binascii
import os


def parse_args(options_dict, args):

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
    parser.add_argument("-r", "--recursive", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-s", "--start-directory", default='.',
                        help="starting directory, defaults to current working "
                        "directory")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    stored_args = parser.parse_args(args)

    return process_args(options_dict, stored_args)


def process_args(options_dict, stored_args):

    for key in stored_args.__dict__:
        if stored_args.__dict__[key] == None:
            continue
        elif key == 'null_character':
            options_dict['null_char'] = stored_args.__dict__[key][0]
        elif key in ['verbose', 'recursive']:
            options_dict[key] = stored_args.__dict__[key]
        elif key == 'start_directory':
            if os.path.isdir(stored_args.__dict__[key]):
                options_dict[key] = stored_args.__dict__[key]
            else:
                raise ValueError
        elif key == 'categories':
            options_dict['Categories'] = {}
            options_dict['Categories']['cat1'] = stored_args.__dict__[key][0]
            options_dict['Categories']['cat2'] = stored_args.__dict__[key][1]
            options_dict['Categories']['cat3'] = stored_args.__dict__[key][2]
        elif key == 'category_extension':
            for ce in stored_args.__dict__[key]:
                ext = ce[0]
                options_dict[ext] = {}
                options_dict[ext]['cat1'] = int(ce[1])
                options_dict[ext]['cat2'] = int(ce[2])
                options_dict[ext]['cat3'] = int(ce[3])
        elif key == 'c1':
            if not options_dict.get('Categories'):
                options_dict['Categories'] = {'cat1': 1, 'cat2': 2, 'cat3': 5}
            options_dict['Categories']['cat1'] = stored_args.__dict__[key][0]
        elif key == 'c2':
            if not options_dict.get('Categories'):
                options_dict['Categories'] = {'cat1': 1, 'cat2': 2, 'cat3': 5}
            options_dict['Categories']['cat2'] = stored_args.__dict__[key][0]
        elif key == 'c3':
            if not options_dict.get('Categories'):
                options_dict['Categories'] = {'cat1': 1, 'cat2': 2, 'cat3': 5}
            options_dict['Categories']['cat3'] = stored_args.__dict__[key][0]

    return options_dict
