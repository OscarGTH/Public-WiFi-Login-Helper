import configargparse


def get_configuration():
    p = configargparse.ArgParser(
        default_config_files=['/etc/app/conf.d/*.conf', '~/.my_settings'])
    p.add('-c', '--my-config', required=True,
          is_config_file=True, help='config file path')
    p.add('-a', '--configure_account', required=False, action='store_true',
          help='Argument used for creating account configuration file.')
    p.add('--receiver_address', required=True, help='Email address of receiver.')
    p.add('--sender_address', required=True,
          help='Email address of email sender.')
    p.add('--sender_pass', required=True,
          help='Email address password of email sender.')
    p.add('--mail_content', required=True,
          help='Email message content. Must contain "<IP ADDRESS>" substring.')
    p.add('--subject_line', required=True,
          help='Email subject line.')
    p.add('--wifi_checking_page', required=True,
          help='Page which can be accessed to promt the public WiFi login page.')
    p.add('--wifi_user', required=True,
          help='Public WiFi login username.')
    p.add('--wifi_pass', required=True,
          help='Public WiFi login password.')
    p.add('--wifi_name', required=True,
          help='Name of the open WiFi to connect to.')
    p.add('--os', required=True,
          help='Operating system in which the program is being run in.')

    options = p.parse_args()

    return options