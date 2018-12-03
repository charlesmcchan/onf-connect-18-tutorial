#!/usr/bin/python
from ptf.packet import IP
from scapy.layers.inet import UDP
from scapy.sendrecv import sniff

if os.getuid() != 0:
    print "Please run this script as sudo :)"
    exit()

INTF = 's204-eth3'
UE_ADDR = '17.0.0.1'
ENODEB_ADDR = '10.0.100.1'
GTP_PORT = 2152

pkt_count = 0


def print_pkt(pkt):
    if IP not in pkt or UDP not in pkt[IP]:
        return
    ipDst = pkt[IP].dst
    if ipDst != UE_ADDR and ipDst != ENODEB_ADDR:
        return
    global pkt_count
    pkt_count = pkt_count + 1
    ipSrc = pkt[IP].src
    if pkt[UDP].dport == GTP_PORT:
        gtp = "TRUE :)"
    else:
        gtp = "FALSE :("

    print "[%d] Received packet of %d bytes: %s -> %s, gtpEncap=%s" \
          % (pkt_count, len(pkt), ipSrc, ipDst, gtp)


print "Will print a line for every UDP packet to IP %s or %s..." \
      % (ENODEB_ADDR, UE_ADDR)

sniff(iface=INTF, count=0, store=False, prn=lambda x: print_pkt(x))
