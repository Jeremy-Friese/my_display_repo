'''Email and other functions dealing with notifications.'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os.path import basename


def send_email(
    sender: str,
    receiver: str,
    subject: str,
    body: str,
    html: bool = True,
    file_attachment_path: str | None = None,
    file_attachment_email_name: str | None = None,
    smtprelay: str | None = None,
):
    '''Sends arbitrary email.
    Params:
        sender (str): Email account to send email from.
        receiver (str): Comma-separated list of email addresses to send to.
        subject (str): Email subject.
        body (str): Email body. Should be valid HTML if html=True.
        html (bool): True to format email as HTML, false for plain text. Defaults to True.
        file_attachment_path (str): File path to email attachment. Defaults to None.
        file_attachment_email_name (str): New name for file, will use name provided in
        'file_attachment_path' if not provided. Defaults to None.
        smtprelay (str): SMTP server to be used to send email.  If 'None' it will be defines below.
    '''
    if smtprelay == None:
        smtprelay = "smtprelay.work.com"
    try:
        # General Email variables
        msg = MIMEMultipart("alternative")
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject

        # Determine HTML email or plain text
        if html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        # Attaching a file to the email
        if file_attachment_path is not None:
            attachment = MIMEBase('application', "octet-stream")

            # Set the name of the sent file
            if file_attachment_email_name is not None and file_attachment_email_name != '':
                sent_file_name = file_attachment_email_name
            else:
                sent_file_name = basename(file_attachment_path)

            with open(file_attachment_path, "rb") as attachment_object:
                attachment.set_payload(attachment_object.read())
                encoders.encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition',
                    'attachment; filename={0}'.format(sent_file_name)
                )
                msg.attach(attachment)
                attachment_object.close()

        # SMTP server settings
        server = smtplib.SMTP(smtprelay, 25)
        body = msg.as_string()
        server.sendmail(sender, receiver.split(','), body)
        server.quit()

        # Returned Variables
        result = True
        error = ''

    except Exception as err:
        # Returned Variables
        result = True
        error = err

    return [result, error]
