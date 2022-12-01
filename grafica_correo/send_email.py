import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params
rrdpath = '/Users/zul/Documents/escuela/Admin Servicios en Red/practicas/practica2/grafica_correo/rrd/'
imgpath = '/Users/zul/Documents/escuela/Admin Servicios en Red/practicas/practica2/grafica_correo/img/'
fname = 'trend.rrd'

mailsender = "dummycuenta3@gmail.com"
mailreceip = "cuam2502@gmail.com"
mailserver = 'smtp.gmail.com:587'
password = 'dvduuffmlhspbmjj'

def send_alert_attached(subject, elemento):
    """ Envía un correo electrónico adjuntando la imagen en IMG
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(imgpath+'deteccion-' + elemento + '.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()