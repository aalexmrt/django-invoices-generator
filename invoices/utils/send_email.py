import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import os

PATH = "media/invoices_pdf"


def prepare_msg(contact_name, contact_email, sender_name, email_account, cc_emails_list, files_list):
    contact_name = contact_name.capitalize()

    html = """\
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
            <p>Buenas {},<br><br>Te adjunto en este correo la última factura.<br><br>Un saludo.</p>
            </body>
            </html>
            """.format(contact_name)

    text = """\
            Buenas {},\n
            Te adjunto en este correo la última factura.\n
            Un saludo.\n
            """.format(contact_name)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg_alternative = MIMEMultipart('alternative')
    msg_alternative.attach(part1)
    msg_alternative.attach(part2)

    msg_mixed = MIMEMultipart('mixed')
    msg_mixed.attach(msg_alternative)

    add_attachment(sender_name, files_list, msg_mixed)

    msg_mixed['From'] = email_account
    msg_mixed['To'] = contact_email
    msg_mixed['Cc'] = cc_emails_list
    # msg_mixed['Cc'] = ""
    msg_mixed['Subject'] = 'Nueva factura de {}'.format(
        sender_name)

    return msg_mixed


def add_attachment(sender_name, files_list, msg_mixed):
    print(files_list)
    for pdf in files_list:
        original_filename = pdf.__str__()
        # e.g 2023-0010 Company name S.L.pdf
        corporate_filename = "{} {}.pdf".format(original_filename.split(
            "_")[0], sender_name)
        file_path = os.path.join(PATH, original_filename)
        with open(file_path, "rb") as attachment:
            attachment = MIMEApplication(attachment.read(), _subtype="pdf")
            attachment.add_header(
                'Content-Disposition', 'attachment', filename=corporate_filename)

            msg_mixed.attach(attachment)

    return msg_mixed


def config_mail_server(email_account, email_pwd):

    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(email_account, email_pwd)

        return server

    except:
        print("Error configuring the server")


def send_invoice_email(email_account, email_pwd, sender_name, contact_email, contact_name, cc_emails_list, files_list):
    cc_emails_list = ",".join(cc_emails_list)
    msg_mixed = prepare_msg(contact_name, contact_email,
                            sender_name, email_account, cc_emails_list, files_list)
    receiver_email = [contact_email, cc_emails_list]
    msg_status = None
    try:
        server = config_mail_server(email_account, email_pwd)
        server.sendmail(msg_mixed['From'],
                        receiver_email, msg_mixed.as_string())
        server.set_debuglevel(1)
        msg_status = True
        print("succeed")
    except Exception as err:
        # Print any error messages to stdout
        print(err)
        msg_status = False
    finally:
        server.quit()

    return msg_status
