import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import Config

TEMPLATE_PATH = Config.TEMPLATE_PATH
SMTP_ADDRESS = Config.SMTP_ADDRESS
SMTP_PASSWORD = Config.SMTP_PASSWORD
SMTP_HOST = Config.SMTP_HOST
SMTP_PORT = Config.SMTP_PORT


def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_recovery_letter(email, recovery_code, name):
    message_template = read_template(TEMPLATE_PATH + '/recovery_message_ru.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
    s.starttls()
    s.login(SMTP_ADDRESS, SMTP_PASSWORD)

    msg = MIMEMultipart()  # create a message

    # add in the actual person name to the message template
    message = message_template.substitute(NAME=name, RECOVERY_CODE=recovery_code)

    # setup the parameters of the message
    msg['From'] = SMTP_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Password Reset Request"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()
