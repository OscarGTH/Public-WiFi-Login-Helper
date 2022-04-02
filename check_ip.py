from urllib import request
import json
from mailer import MailSender
import logging
import sys

# Configuring logger.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ip_logger.ip_checker')

def check_if_ip_changed(current_ip):
    ''' Reads last saved IP address from a JSON file. 
        Returns boolean value if ip has changed.
    '''
    try:
        # Reading JSON file which contains previously seen IP address
        with open('ip_data.json', 'r') as f:
            data = json.load(f)
            # If JSON contains correct key and the value does not match current ip
            if 'ip' in data and data['ip'] != current_ip:
                # IP has changed, so returning True.
                return True
            else:
                # IP has not changed.
                return False
    except json.decoder.JSONDecodeError as exc:
        logger.warning("-Error while reading JSON file.")
        logger.error(exc)
        # Exiting program if there was an error.
        sys.exit(0)

def update_ip(new_ip):
    ''' Updates IP address to JSON file. '''
    try:
        logger.info('-Updating IP to JSON file.')
        # Opening ip_data.json file and writing new ip into it.
        with open('ip_data.json', 'w') as f:
            new_data = json.dumps({"ip": new_ip})
            logger.info('-Writing JSON file.')
            f.write(new_data)
            return True
    except FileNotFoundError as ex:
        logger.error(ex)
        return False

def run_ip_checker():
    # Getting current ip address
    external_ip = request.urlopen('https://ident.me').read().decode('utf8')
    # Checking if IP had changed.
    if check_if_ip_changed(external_ip):
        logger.info("-IP had changed.")
        logger.info("-New IP is " + str(external_ip))
        # Writing updated ip to file.
        success = update_ip(external_ip)
        if success:
            # Creating instance of Mail Sender
            mailer = MailSender()
            # Sending message about the updated IP.
            mailer.send_message(external_ip)
        else:
            logger.error("-Email not sent about updated IP.")
    else:
        logger.info("-IP hadn't changed.")
    

if __name__ == "__main__":
    run_ip_checker()