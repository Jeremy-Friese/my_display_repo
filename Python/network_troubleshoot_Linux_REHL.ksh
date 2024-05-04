#!/bin/bash
mkdir troubleshoot
cd troubleshoot


sar > sar.txt

#######################################################################################################
# This runs diagnostics on the server.
#######################################################################################################

echo "    Interface Configs" > troubleshoot.txt
/sbin/ifconfig >> troubleshoot.txt
echo "*****************************************************************" >> troubleshoot.txt
echo "    Routing Table" >>troubleshoot.txt
netstat -rn >> troubleshoot.txt
echo "*****************************************************************" >> troubleshoot.txt
echo "DNS Servers system is pointed to" >> troubleshoot.txt
cat /etc/resolv.conf >> troubleshoot.txt
echo "*****************************************************************" >> troubleshoot.txt
echo -n "    Top processes running" >> troubleshoot.txt
echo "*" >> troubleshoot.txt
ps -Ao user,uid,comm,pid,pcpu,tty --sort=-pcpu | head -n 10 >> troubleshoot.txt
echo "*****************************************************************" >> troubleshoot.txt
echo "     Processor Status" >> troubleshoot.txt
head -n 3 sar.txt >> troubleshoot.txt
tail -n 20 sar.txt >> troubleshoot.txt
echo "*****************************************************************" >> troubleshoot.txt
echo "Ping and Traceroute" >> troubleshoot.txt

cat /etc/redhat-release > red-hat

hostname > hostname.txt
netstat -an > netstat.txt

#######################################################################################################
# This creates the Python Script to ping and traceroute.
#######################################################################################################


which python > python

echo "#!" > pound

paste pound python > troubleshoot.py

echo "#####################################################################"  >> troubleshoot.py

echo "import sys" >> troubleshoot.py
echo "import os" >> troubleshoot.py
echo import time >> troubleshoot.py
echo import re >> troubleshoot.py
echo import subprocess >> troubleshoot.py
echo import datetime, threading >> troubleshoot.py
echo import socket >> troubleshoot.py



#echo "f = open('IP')" >> troubleshoot.py
#echo "hn = f.read()" >> troubleshoot.py
#echo "f.close()" >> troubleshoot.py


echo "IP = raw_input('Enter Destination IP Address or Destination Device Name:')" >> troubleshoot.py

echo "address = '%s' % IP" >> troubleshoot.py
echo "out = open('troubleshoot.txt', 'a')" >> troubleshoot.py
echo "res = subprocess.call(['ping', '-c', '4', address], stdout = out)" >> troubleshoot.py
echo "out.write('\n\n')" >> troubleshoot.py
echo "out.close()" >> troubleshoot.py


#echo "f = open('IP')" >> troubleshoot.py
#echo "hn = f.read()" >> troubleshoot.py
#echo "f.close()" >> troubleshoot.py

echo "f=open('troubleshoot.txt','a')" >> troubleshoot.py

echo "hostname='%s' % IP" >> troubleshoot.py
echo "f.write(hostname+'    :   ')" >> troubleshoot.py


echo "traceroute = subprocess.Popen(['traceroute', '-w', '10', hostname],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)" >> troubleshoot.py
echo "while (True):" >> troubleshoot.py
echo "    hop = traceroute.stdout.readline()" >> troubleshoot.py
echo "    if not hop: break" >> troubleshoot.py
echo "    f.write( hop )" >> troubleshoot.py

echo "time.sleep(5)" >> troubleshoot.py




#######################################################################################################
# This creates a Python Script and ksh script to send the email
#######################################################################################################

#Python2.4 (RHEL5)

which python > python

echo "#!" > pound

paste pound python > send.py

echo "#####################################################################"  >> send.py

echo "import sys" >> send.py
echo "import os" >> send.py
echo "import urllib" >> send.py
echo "import urllib2" >> send.py
echo "import smtplib" >> send.py
echo "from email.MIMEMultipart import MIMEMultipart" >> send.py
echo "from email.MIMEText import MIMEText" >> send.py
echo "from email.MIMEBase import MIMEBase" >> send.py
echo import time >> send.py
echo import re >> send.py
echo import subprocess >> send.py
echo import datetime, threading >> send.py
echo import socket >> send.py
echo "from email import Encoders" >> send.py


echo "f = open('hostname.txt')" >> send.py
echo "hn = f.read()" >> send.py
echo "f.close()" >> send.py

echo "msg = MIMEMultipart()" >> send.py
echo "msg['Subject'] = 'Troubleshooting Server %s' % hn" >> send.py
echo "fromaddrs = '%s@dtcc.com' % hn" >> send.py
echo "toaddrs = ''" >> send.py
echo "a = open('troubleshoot.txt', 'r')" >> send.py
echo "msg.attach(MIMEText(a.read()))" >> send.py
echo "a.close()" >> send.py

echo "attachment = MIMEBase('text', 'octet-stream')" >> send.py
echo "attachment.set_payload(open('netstat.txt', 'rb').read())" >> send.py
echo "Encoders.encode_base64(attachment)" >> send.py
echo "attachment.add_header('Content-Disposition', 'attachment')" >> send.py
echo "msg.attach(attachment)" >> send.py

echo "server = smtplib.SMTP('')" >> send.py
echo "server.sendmail(fromaddrs, toaddrs, msg.as_string())" >> send.py
echo "server.quit()" >> send.py



#Python2.6 and 2.7 (RHEL 6 and 7)


which python > python

echo "#!" > pound

paste pound python > send1.py

echo "#####################################################################"  >> send1.py

echo "import sys" >> send1.py
echo "import os" >> send1.py
echo "import urllib" >> send1.py
echo "import urllib2" >> send1.py
echo "import smtplib" >> send1.py
echo "from email.mime.multipart import MIMEMultipart" >> send1.py
echo "from email.mime.text import MIMEText" >> send1.py
echo "from email.MIMEBase import MIMEBase" >> send1.py
echo import time >> send1.py
echo import re >> send1.py
echo import subprocess >> send1.py
echo import datetime, threading >> send1.py
echo import socket >> send1.py
echo "from email import Encoders" >> send1.py

echo "f = open('hostname.txt')" >> send1.py
echo "hn = f.read()" >> send1.py
echo "f.close()" >> send1.py

echo "msg = MIMEMultipart()" >> send1.py
echo "msg['Subject'] = 'Troubleshooting Server %s' % hn" >> send1.py
echo "fromaddrs = '%s@thecompany.com' % hn" >> send1.py
echo "toaddrs = 'networkTeam@thecompany.com'" >> send1.py

echo "a = open('troubleshoot.txt', 'r')" >> send1.py
echo "msg.attach(MIMEText(a.read()))" >> send1.py
echo "a.close()" >> send1.py

echo "attachment = MIMEBase('text', 'octet-stream')" >> send1.py
echo "attachment.set_payload(open('netstat.txt', 'rb').read())" >> send1.py
echo "Encoders.encode_base64(attachment)" >> send1.py
echo "attachment.add_header('Content-Disposition', 'attachment')" >> send1.py
echo "msg.attach(attachment)" >> send1.py

echo "server = smtplib.SMTP('')" >> send1.py
echo "server.sendmail(fromaddrs, toaddrs, msg.as_string())" >> send1.py
echo "server.quit()" >> send1.py



chmod +x troubleshoot.py
chmod +x send.py
chmod +x send1.py

./troubleshoot.py

#######################################################################################################
# This determines which script to use to send the email.
#######################################################################################################



if grep -c "Tikanga" red-hat
then
    ./send.py
else
    ./send1.py
fi


cd ..
#rm -r troubleshoot
