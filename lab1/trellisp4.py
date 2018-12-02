#!/usr/bin/python

import argparse

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo

from utils.bmv2 import ONOSBmv2Switch
from utils.routinglib import RoutedHost
from utils.trellislib import TaggedRoutedHost

PIPECONF_ID = 'org.onosproject.pipelines.fabric'


class Trellis(Topo):
    """Trellis basic topology"""

    def __init__(self, *args, **kwargs):
        Topo.__init__(self, *args, **kwargs)

        # Spines
        s226 = self.addSwitch('s226', cls=ONOSBmv2Switch, pipeconf=PIPECONF_ID)
        s227 = self.addSwitch('s227', cls=ONOSBmv2Switch, pipeconf=PIPECONF_ID)

        # Leaves
        s204 = self.addSwitch('s204', cls=ONOSBmv2Switch, pipeconf=PIPECONF_ID)
        s205 = self.addSwitch('s205', cls=ONOSBmv2Switch, pipeconf=PIPECONF_ID)

        # Switch Links
        self.addLink(s226, s204)
        self.addLink(s226, s205)
        self.addLink(s227, s204)
        self.addLink(s227, s205)

        # NOTE avoid using 10.0.1.0/24 which is the default subnet of quaggas
        # NOTE avoid using 00:00:00:00:00:xx which is the default mac of host
        # behind upstream router
        # IPv4 Hosts
        h1 = self.addHost('h1', cls=RoutedHost, mac='00:aa:00:00:00:01',
                          ips=['10.0.100.1/24'], gateway='10.0.100.254')
        h2 = self.addHost('h2', cls=TaggedRoutedHost, mac='00:aa:00:00:00:02',
                          ips=['10.0.100.2/24'], gateway='10.0.100.254', vlan=100)
        h3 = self.addHost('h3', cls=RoutedHost, mac='00:aa:00:00:00:03',
                          ips=['10.0.200.1/24'], gateway='10.0.200.254')
        h4 = self.addHost('h4', cls=TaggedRoutedHost, mac='00:aa:00:00:00:04',
                          ips=['10.0.200.2/24'], gateway='10.0.200.254', vlan=200)

        self.addLink(h1, s204)
        self.addLink(h2, s204)
        self.addLink(h3, s205)
        self.addLink(h4, s205)


topos = {'trellis': Trellis}


def main(argz):
    topo = Trellis()
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
