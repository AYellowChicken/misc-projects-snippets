from scapy.all import *

os.system('iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP')
os.system('iptables -L')

get = 'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n'
syn_ip  = IP(src='172.24.104.56', dst='www.google.com')
syn_syn = TCP(sport = 5558, dport=80, flags='S',seq = 1000)
syn_ack = sr1(syn_ip/syn_syn,verbose=0)

if syn_ack:
    temp = syn_ack.seq
    myack  = temp + 1
    ack_packet = TCP(sport=5558,dport=80,flags='A',seq=syn_ack.ack,ack=myack)
    send(syn_ip/ack_packet,verbose=0)

    payload_packet = TCP(sport=5558,dport=80,flags='A',seq=syn_ack.ack, ack=myack)
    p = syn_ip/payload_packet/get
    server_resp = sr1(p,verbose=0)
    a = sniff(iface = "eth0",filter = "tcp port 80",stop_filter=stopfilter)

    for packet in a:
        if packet.getlayer(Raw):
            l = packet.getlayer(Raw).load
            rawr=Raw(l)
            rawr.show()