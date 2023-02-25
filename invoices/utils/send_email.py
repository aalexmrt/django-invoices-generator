import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import environ
import os
from django.conf import settings
from django.conf.urls.static import static

env = environ.Env()
environ.Env.read_env()


GMAIL = env("GMAIL_ACCOUNT")
PASSWORD = env("GMAIL_ACCOUNT_PWD")
TODO_CC = ""

PATH = "media/invoices_pdf"


def prepare_msg(client, company, files):
    client_name = client.name.capitalize()

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
            """.format(client_name)

    text = """\
            Buenas {},\n
            Te adjunto en este correo la última factura.\n
            Un saludo.\n
            """.format(client_name)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg_alternative = MIMEMultipart('alternative')
    msg_alternative.attach(part1)
    msg_alternative.attach(part2)

    msg_mixed = MIMEMultipart('mixed')
    msg_mixed.attach(msg_alternative)

    add_attachment(company, files, msg_mixed)

    msg_mixed['From'] = GMAIL
    msg_mixed['To'] = client.email
    msg_mixed['Cc'] = TODO_CC
    msg_mixed['Subject'] = 'Nueva factura de {}'.format(
        company.name)

    return msg_mixed


def add_attachment(company, files, msg_mixed):
    for pdf in files:
        original_filename = pdf.__str__()
        # 2023-0010 Company name S.L.pdf
        corporate_filename = "{} {}.pdf".format(original_filename.split(
            "_")[0], company.name)
        path = os.path.join(settings.MEDIA_ROOT,
                            "invoices_pdf", original_filename)
        with open(path, "rb") as attachment:
            attachment = MIMEApplication(attachment.read(), _subtype="pdf")
            attachment.add_header(
                'Content-Disposition', 'attachment', filename=corporate_filename)

            msg_mixed.attach(attachment)

    return msg_mixed


def config_mail_server():

    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(GMAIL, PASSWORD)

        return server

    except:
        print("Error configuring the server")


def send_invoice_mail(client, company, files):

    msg_mixed = prepare_msg(client, company, files)
    receiver_email = [client.email, TODO_CC]

    try:
        server = config_mail_server()
        server.sendmail(msg_mixed['From'],
                        receiver_email, msg_mixed.as_string())
        server.set_debuglevel(1)
    except Exception as err:
        # Print any error messages to stdout
        print(err)
    finally:
        server.quit()
