import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import os

PATH = "media/"


def get_template_msg(contact_name, multiple=False):
    message = "las últimas facturas" if multiple else "la última factura"

    html = f"""\
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body>
        <p>Buenas {contact_name},<br><br>Te adjunto en este correo {message}.<br><br>Un saludo.</p>
        </body>
        </html>
        """

    text = f"""\
        Buenas {contact_name},\n
        Te adjunto en este correo {message}.\n
        Un saludo.\n
        """

    return html, text


def prepare_msg(contact_name, contact_email, sender_name, email_account, cc_emails_list, files_queryset):
    html, text = '', ''
    count = files_queryset.count()

    if count > 1:
        html, text = get_template_msg(contact_name, multiple=True)
    elif count == 1:
        html, text = get_template_msg(contact_name)

    contact_name = contact_name.capitalize()

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg_alternative = MIMEMultipart('alternative')
    msg_alternative.attach(part1)
    msg_alternative.attach(part2)

    msg_mixed = MIMEMultipart('mixed')
    msg_mixed.attach(msg_alternative)

    add_attachment(sender_name, files_queryset, msg_mixed)

    msg_mixed['From'] = email_account
    msg_mixed['To'] = contact_email
    msg_mixed['Cc'] = cc_emails_list
    msg_mixed['Subject'] = f'Nueva factura de {sender_name}'

    return msg_mixed


def add_attachment(sender_name, files_queryset, msg_mixed):
    for pdf in files_queryset:
        # e.g ('2023', 5, 'invoices_pdf/2023-5_Ventura-Peixos-SL_2023-04-12.pdf')
        print(pdf)
        original_filename = pdf[2]
        # e.g 2023-0010 Company name S.L.pdf
        corporate_filename = f"{pdf[0]}-{pdf[1]:04d} {sender_name}.pdf"
        file_path = os.path.join(PATH, original_filename)
        with open(file_path, "rb") as attachment:
            attachment = MIMEApplication(attachment.read(), _subtype="pdf")
            attachment.add_header('Content-Disposition',
                                  'attachment', filename=corporate_filename)
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

    except Exception as e:
        print("Error configuring the server:", str(e))


def send_invoice_email(email_account, email_pwd, sender_name, contact_email, contact_name, cc_emails_list, files_queryset):
    if cc_emails_list is None:
        cc_emails_list = ""

    cc_emails_list = cc_emails_list.replace(" ", "")
    msg_mixed = prepare_msg(contact_name, contact_email,
                            sender_name, email_account, cc_emails_list, files_queryset)
    receiver_email = cc_emails_list.split(",") + [contact_email]
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
