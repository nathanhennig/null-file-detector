import ConfigParser
import binascii
import sys
import defaults


def create_default_config(config_file):
    """Sets up a default configuration file."""

    config = ConfigParser.SafeConfigParser(allow_no_value=True)

    config.add_section('General')
    config.set(
        'General', '# Null character must be a hex byte with no prefix eg. 00, a0, ff')
    config.set('General', 'null_char', binascii.hexlify(
        defaults.Default.NULL_CHAR))
    config.set(
        'General', '# When true, all subdirectories are scanned by default')
    config.set('General', 'recursive', str(defaults.Default.RECURSIVE))
    config.set(
        'General', '# Prepends all results with percent null')
    config.set('General', 'verbose', str(defaults.Default.VERBOSE))
    config.set('General', 'category_1_name', defaults.Default.CAT_1_NAME)
    config.set('General', 'category_2_name', defaults.Default.CAT_2_NAME)
    config.set('General', 'category_3_name', defaults.Default.CAT_3_NAME)

    config.add_section('Categories')
    config.set('Categories', 'cat1', str(defaults.Default.CAT_1))
    config.set('Categories', 'cat2', str(defaults.Default.CAT_2))
    config.set('Categories', 'cat3', str(defaults.Default.CAT_3))

    if sys.platform.startswith('win'):
        with open(config_file, 'wb') as configfile:
            config.write(configfile)

        # convert line endings to DOS style '\r\n'
        f = open(config_file)
        txt = f.read()
        f.close()

        f = open(config_file, 'w')
        txt = txt.replace('\n', '\r\n')
        f.write(txt)

    else:
        with open(config_file, 'wb') as configfile:
            config.write(configfile)


def read_config(config_file=defaults.Default.CONFIG_NAME):
    """Reads config file and processes into dictionary."""

    config = ConfigParser.SafeConfigParser()

    options = config.read(config_file)

    # check that config file exists
    if len(options) <= 0:
        print('Config file not found, generating default config file.')
        create_default_config(config_file)
        config.read(config_file)

    config_dict = {}

    try:
        config_dict['verbose'] = config.getboolean('General', 'verbose')
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
        print("NoOptionError: 'verbose' option missing, assuming False "
              "unless set by command line")
        config_dict['verbose'] = defaults.Default.VERBOSE
    except ValueError:
        print("ValueError: 'verbose' option not set to a boolean value")
        sys.exit()

    try:
        config_dict['null_char'] = binascii.unhexlify(
            config.get('General', 'null_char'))
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
        print("NoOptionError: 'null_char' option missing, assuming '\\x00' "
              "unless set by command line")
        config_dict['null_char'] = defaults.Default.NULL_CHAR
    except TypeError:
        print("TypeError: 'null_char' option invalid")
        sys.exit()

    try:
        config_dict['recursive'] = config.getboolean('General', 'recursive')
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
        print("NoOptionError: 'recursive' option missing, assuming False "
              "unless set by command line")
        config_dict['recursive'] = defaults.Default.RECURSIVE
    except ValueError:
        print("ValueError: 'recursive' option not set to a boolean value")
        sys.exit()

    default_names = [defaults.Default.CAT_1_NAME,
                     defaults.Default.CAT_2_NAME,
                     defaults.Default.CAT_3_NAME]
    for index, key in enumerate(['category_1_name', 'category_2_name', 'category_3_name']):
        try:
            config_dict[key] = config.get('General', key)
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            config_dict[key] = default_names[index]

    for key in config._sections:
        if key == 'General':
            continue
        config_dict[key] = {}
        for subkey in config._sections[key]:
            if subkey == '__name__':
                continue
            try:
                config_dict[key][subkey] = int(config._sections[key][subkey])
            except ValueError:
                config_dict[key][subkey] = config._sections[key][subkey]

    if 'Categories' not in config._sections:
        config_dict['Categories'] = {}
        config_dict['Categories']['cat1'] = defaults.Default.CAT_1
        config_dict['Categories']['cat2'] = defaults.Default.CAT_2
        config_dict['Categories']['cat3'] = defaults.Default.CAT_3

    # Set default start_directory value
    config_dict['start_directory'] = defaults.Default.START_DIRECTORY

    return config_dict
