import smtplib
from email.mime.text import MIMEText

smtp_server = 'smtp.mail.yahoo.com'
smtp_port = 465
email_user = 'yetty_agbalu@yahoo.com'
email_password = 'Zahrah@11'

msg = MIMEText('This is a test email')
msg['Subject'] = 'Test'
msg['From'] = email_user
msg['To'] = 'eniolaagbalu@gmail.com'

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, 'eniolaagbalu@gmail.com', msg.as_string())
    server.quit()
    print('Email sent successfully')
except Exception as e:
    print(f'Failed to send email: {e}')
