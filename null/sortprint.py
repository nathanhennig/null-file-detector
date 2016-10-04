# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import sys


def sort(scanned_files, config_dict):
    """Sort scanned files into categories."""

    cat1 = []
    cat2 = []
    cat3 = []
    cat4 = []
    cat5 = []

    for target_file in scanned_files:
        if type(target_file.null_count) is int:
            t1, t2, t3 = threshold(target_file.suffix, config_dict)

            try:
                null_percent = (target_file.null_count
                                * 1.0
                                / target_file.size
                                * 100)
            except ZeroDivisionError:
                null_percent = 0

            if null_percent < t1:
                cat1.append(target_file)
            elif t2 != 0 and t1 < null_percent < t2:
                cat2.append(target_file)
            elif t3 != 0 and t2 < null_percent < t3:
                cat3.append(target_file)
            else:
                cat4.append(target_file)

        else:
            cat5.append(target_file)

    return cat1, cat2, cat3, cat4, cat5


def threshold(suffix, config_dict):
    """Determines null percent thresholds for categories based on suffix."""

    if suffix in config_dict:
        t1 = config_dict[suffix]['cat1']
        t2 = config_dict[suffix]['cat2']
        t3 = config_dict[suffix]['cat3']
    else:
        t1 = config_dict['Categories']['cat1']
        t2 = config_dict['Categories']['cat2']
        t3 = config_dict['Categories']['cat3']

    return t1, t2, t3


def sort_print(scanned_files, config_dict):
    """
    Sorts scanned files, then outputs to stdout or file(s) as selected."""

    c_d = config_dict
    cat1, cat2, cat3, cat4, cat5 = sort(scanned_files, c_d)

    xml = config_dict.get('xml_log')

    if xml:
        xml_print([cat1, cat2, cat3, cat4, cat5], c_d)
    else:
        null_print(cat1, c_d['category_1_name'], c_d)
        null_print(cat2, c_d['category_2_name'], c_d)
        null_print(cat3, c_d['category_3_name'], c_d)
        null_print(cat4, 'NULL', c_d)
        null_print(cat5, 'ERROR', c_d)


def null_print(category, name, config_dict):
    """Prints sorted results to std or files."""

    files = config_dict.get('files')
    verbose = config_dict.get('verbose')

    if category and files:
        file_name = config_dict['timestamp'] + name + '.txt'

        with open(file_name, 'w') as logfile:
            for target_file in category:
                if verbose and name != 'ERROR':
                    try:
                        null_percent = (target_file.null_count
                                        * 1.0
                                        / target_file.size
                                        * 100)
                    except ZeroDivisionError:
                        null_percent = 0

                    logfile.write('{0:.2f} {1}\n'.format(
                        round(null_percent, 2), target_file.name))
                else:
                    logfile.write('{}\n'.format(target_file.name))

        if sys.platform.startswith('win'):
            convert_line_end_dos(file_name)

    elif category:
        print(name)
        for target_file in category:
            if verbose and name != 'ERROR':
                try:
                    null_percent = (target_file.null_count
                                    * 1.0
                                    / target_file.size
                                    * 100)
                except ZeroDivisionError:
                    null_percent = 0

                print('{0:.2f} {1}'.format(
                    round(null_percent, 2), target_file.name))
            else:
                print('{}'.format(target_file.name))

# Separated from null_print() because XML tree for all
# categories must be built in one pass.
def xml_print(category_list, config_dict):
    """Saves results to XML file."""

    c_d = config_dict
    verbose = config_dict.get('verbose')
    file_name = config_dict['timestamp'] + 'log.xml'

    root = ET.Element('log')

    cat_names = [c_d['category_1_name'],
                 c_d['category_2_name'],
                 c_d['category_3_name'],
                 'NULL',
                 'ERROR']

    for index, category in enumerate(category_list):

        if category:

            cat = ET.SubElement(root, cat_names[index])
            

            for target_file in category:
                file_entry = ET.SubElement(cat, "file")
                if verbose and cat_names[index] != 'ERROR':
                    try:
                        null_percent = (target_file.null_count
                                        * 1.0
                                        / target_file.size
                                        * 100)
                    except ZeroDivisionError:
                        null_percent = 0

                    ET.SubElement(file_entry, "path").text = target_file.name
                    ET.SubElement(file_entry, "null_percent").text = str(
                        round(null_percent, 2))
                else:
                    ET.SubElement(file_entry, "path").text = target_file.name

            tree = ET.ElementTree(root)
            tree.write(file_name)


def convert_line_end_dos(file):
    """Convert line endings to DOS style '\r\n'."""
    f = open(file)
    txt = f.read()
    f.close()

    f = open(file, 'w')
    txt = txt.replace('\n', '\r\n')
    f.write(txt)
