import email.message
import smtplib

def send(target_email, title, content):
    '''@content unicode'''
    co = smtplib.SMTP('some mail server',587)
    co.login('some login', 'some password')

    emsg = email.message.Message()
    emsg.add_header('From', 'Administracja Bellum<admin@thebellum.pl>')
    emsg.add_header('Subject', title)
    emsg.add_header('To', '<'+target_email+'>')
    emsg.set_payload(content.encode('utf-8'), 'UTF-8')

    co.sendmail('admin@thebellum.pl', target_email, emsg.as_string())
    co.quit()