import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
# Own modules
from config_parser import get_configuration

# Configuring logger
logger = logging.getLogger('ip_logger.mailer')

class MailSender:
    
    def __init__(self) -> None:
        ''' Initializes Mail Sender '''

        self.read_conf()
    
    def read_conf(self):
        ''' Reads configuration file and saves variables into self. '''

        logger.info("-Reading configuration.")
        self.conf = get_configuration()
        
    def send_message(self, ip_address):
        ''' Sends a message about changed IP address. '''

        data = self.conf
        logger.info("-Building the message.")
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = data.sender_address
        message['To'] = data.receiver_address
        #The subject line
        message['Subject'] = data.subject_line
        # Inserting the changed IP address into the mail content.
        mail_content = data.mail_content.replace('<IP ADDRESS>', ip_address)
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        try:        
            #Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(data.sender_address, data.sender_pass) #login with mail_id and password
            text = message.as_string()
            # Sending email
            session.sendmail(data.sender_address, data.receiver_address, text)
            session.quit()
            logger.info("-Email successfully sent!")
        except smtplib.SMTPException as ex:
            # Logging exception
            logger.warning("-Exception occured when sending message.")
            logger.error(ex)
   