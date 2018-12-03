#!/usr/bin/python

# Send downlink packets to UE address
import os

from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp

if os.getuid() != 0:
    print "Please run this script as sudo :)"
    exit()

INTF = 's205-eth3'
SRC_MAC = '00:aa:00:00:00:02'
DST_MAC = '00:00:00:00:02:05'  # leaf s205 MAC (routed packet)
SRC_ADDR = '10.0.200.1'
UE_ADDR = '17.0.0.1'
PPS = 5
PAYLOAD = ' '.join(['P4 is great!'] * 50)

pkt = Ether(src=SRC_MAC, dst=DST_MAC) / IP(src=SRC_ADDR, dst=UE_ADDR) / \
      UDP(sport=80, dport=400) / PAYLOAD

print "Sending %d UDP packets per second to destination IPv4 address %s..." \
      % (PPS, UE_ADDR)

sendp(pkt, iface=INTF, inter=1.0 / PPS, loop=True, verbose=True)
