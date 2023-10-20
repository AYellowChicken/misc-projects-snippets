from socket import inet_aton, inet_ntoa
import struct

def ip2long(ip):
    print(ip)
    packed = inet_aton(ip)
    lng = struct.unpack("!L", packed)[0]
    return lng

def long2ip(lng):
    packed = struct.pack("!L", lng)
    ip=inet_ntoa(packed)
    return ip

filename = "signing.txt"
filetoparse = open(filename, "r")
thestring = filetoparse.read()

hosts = thestring.split("\n")

long_list = []
for h in hosts:
    long_list.append(ip2long(h))

long_list.sort()
final_list = []
for l in long_list:
    final_list.append(long2ip(l))

for ip in final_list:
    print(ip)

filetoparse.close()