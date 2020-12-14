import smtplib 
from email.message import EmailMessage
import getpass

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
except:
    print("Something went wrong")

#this makes the connection secure
server.starttls()

mypwd = getpass.getpass('Enter your password: ')

sender_email = "205finalproject2001@gmail.com"

msg = EmailMessage()

msg['Subject'] = "Your New Image"
msg['From'] = sender_email
msg['To'] = "dleonard@csumb.edu"
msg.set_content("Hello!")

# 'with' in a for loop allows us to send multiple images 
with open('warframe.jpg', 'rb') as fp:
    img_data = fp.read()


msg.add_attachment(img_data, maintype='image', subtype='png')

server.login(sender_email, mypwd)

server.send_message(msg)
server.quit()

