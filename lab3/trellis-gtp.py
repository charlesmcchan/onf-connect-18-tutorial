#!/usr/bin/python

import argparse
import sys

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo

sys.path.append('..')

from utils.bmv2 import ONOSBmv2Switch
from utils.trellislib import RoutedHost


class TrellisGtp(Topo):
    """Trellis basic topology"""

    def __init__(self, *args, **kwargs):
        Topo.__init__(self, *args, **kwargs)

        # Spines
        s226 = self.addSwitch('s226', cls=ONOSBmv2Switch,
                              netcfg=False, grpcport=50226)
        s227 = self.addSwitch('s227', cls=ONOSBmv2Switch,
                              netcfg=False, grpcport=50227)

        # Leaves
        s204 = self.addSwitch('s204', cls=ONOSBmv2Switch,
                              netcfg=False, grpcport=50204)
        s205 = self.addSwitch('s205', cls=ONOSBmv2Switch,
                              netcfg=False, grpcport=50205)

        # Switch Links
        self.addLink(s226, s204)
        self.addLink(s226, s205)
        self.addLink(s227, s204)
        self.addLink(s227, s205)

        # IPv4 Hosts
        eNodeB = self.addHost('enodeb', cls=RoutedHost, mac='00:aa:00:00:00:01',
                              ips=['10.0.100.1/24'], gateway='10.0.100.254')
        pdn = self.addHost('pdn', cls=RoutedHost, mac='00:aa:00:00:00:02',
                           ips=['10.0.200.1/24'], gateway='10.0.200.254')

        self.addLink(eNodeB, s204)
        self.addLink(pdn, s205)


topos = {'trellis-gtp': TrellisGtp}


def main(argz):
    topo = TrellisGtp()
    controller = RemoteController('c0', ip=argz.onos_ip)

    net = Mininet(topo=topo, controller=None)
    net.addController(controller)

    net.start()
    CLI(net)
    net.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Trellis Mininet script with BMv2 (2x2 fabric)')
    parser.add_argument('--onos-ip', help='ONOS controller IP address',
                        type=str, action="store", required=True)
    args = parser.parse_args()
    setLogLevel('info')

    main(args)
