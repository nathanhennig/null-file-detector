# -*- coding: utf-8 -*-


def sort(scanned_files, config_dict):

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

    c_d = config_dict
    cat1, cat2, cat3, cat4, cat5 = sort(scanned_files, c_d)

    null_print(cat1, c_d['category_1_name'], c_d['verbose'])
    null_print(cat2, c_d['category_2_name'], c_d['verbose'])
    null_print(cat3, c_d['category_3_name'], c_d['verbose'])
    null_print(cat4, 'NULL', c_d['verbose'])
    null_print(cat5, 'ERROR', c_d['verbose'])


def null_print(category, name, verbose):

    if category:
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
