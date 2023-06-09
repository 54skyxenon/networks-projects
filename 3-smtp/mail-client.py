#!/usr/local/bin/python3
# mail-client.py

from socket import *

import base64
import ssl
import sys
import warnings

class SMTPMessage:
    client_socket = None
    
    def __init__(self, command=None, expected=None):
        self.command = command
        self.expected = expected
        self.execute()

    def execute(self):
        if self.command is not None:
            if isinstance(self.command, str):
                self.command = self.command.encode()

            print(f'C: {self.command.decode()}')
            SMTPMessage.client_socket.send(self.command)
    
        if self.expected is not None:
            recv = SMTPMessage.client_socket.recv(1024).decode()
            print(recv)
            if recv[:3] != self.expected:
                print(f'{self.expected} reply not received from server.')

def main():
    # YOLO!
    warnings.filterwarnings('ignore', category=DeprecationWarning)

    if len(sys.argv) < 4:
        exit('Usage: ./mail-client.py <gmail-sender-address> <gmail-password> <receiver-address> <image path (Optional)>')

    my_email, my_password, to_email = sys.argv[1:4]
    
    # Call Google mail server `mailserver` (DO NOT use smtp.google.com)
    mailserver = ('smtp.gmail.com', 587)

    # Create socket called client_socket and establish a TCP connection with mailserver
    SMTPMessage.client_socket = socket(AF_INET, SOCK_STREAM)
    SMTPMessage.client_socket.connect(mailserver)

    SMTPMessage(expected='220')

    # Send HELO command and print server response.
    SMTPMessage(command='HELO Brandon\r\n', expected='250')

    # Start the TLS encryption, Optional Exercise
    SMTPMessage(command='STARTTLS\r\n', expected='220')
    SMTPMessage.client_socket = ssl.wrap_socket(SMTPMessage.client_socket)

    # Authenticate
    SMTPMessage(command='AUTH LOGIN\r\n', expected='334')

    # Send username
    username = base64.b64encode(my_email.encode())
    SMTPMessage(command=username + '\r\n'.encode(), expected='334')

    # Send password
    password = base64.b64encode(my_password.encode())
    SMTPMessage(command=password + '\r\n'.encode(), expected='235')

    # Send MAIL FROM command and print server response.
    SMTPMessage(command=f'MAIL FROM: <{my_email}>\r\n', expected='250')

    # Send RCPT TO command and print server response.
    SMTPMessage(command=f'RCPT TO: <{to_email}>\r\n', expected='250')

    # Send DATA command and print server response.
    SMTPMessage(command='DATA\r\n', expected='354')

    # Send message data.
    subject = 'Some Wisdom'
    plaintext_mime = 'Content-Type: text/plain\r\n\r\n'

    # Send headers first
    SMTPMessage(command=f'Subject: {subject}\n')
    SMTPMessage(command=f'To: {to_email}\n')
    SMTPMessage(command=f'Reply-To: {my_email}\n')

    # Embed an image in email, Optional Exercise
    if len(sys.argv) > 4:
        SMTPMessage(command=f'MIME-Version: 1.0\n')
        boundary = 'simple boundary'
        boundary_start = f'--{boundary}\r\n'
        SMTPMessage(command=f'Content-Type: multipart/mixed; boundary="{boundary}"\r\n\r\n')

        # Form the text part
        SMTPMessage(command=boundary_start)
        SMTPMessage(command=plaintext_mime)
        SMTPMessage(command="I'd rather trust and regret, than doubt and regret.\r\n")

        # Form the image part: read the image file and encode it in base64
        image_path = sys.argv[4]
        with open(image_path, 'rb') as f:
            SMTPMessage(command=boundary_start)
            SMTPMessage(command=f'Content-Type: image/png; name="{image_path}"\r\n')
            SMTPMessage(command='Content-Transfer-Encoding: base64\r\n')
            SMTPMessage(command=f'Content-Disposition: attachment; filename="{image_path}"\r\n\r\n')
            image_data = f.read()
            SMTPMessage(command=f'{base64.b64encode(image_data).decode()}\r\n\r\n')

        SMTPMessage(command=f'--{boundary}--\r\n')
    else:
        SMTPMessage(command=plaintext_mime)
        SMTPMessage(command='Shawty\'s like a melody in my head!!')

    # Message ends with a single period.
    SMTPMessage(command='\r\n.\r\n', expected='250')

    # Send QUIT command and get server response.
    SMTPMessage(command='QUIT\r\n', expected='221')

if __name__ == '__main__':
    main()