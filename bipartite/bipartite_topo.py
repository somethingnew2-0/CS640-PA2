#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from argparse import ArgumentParser

# Parse arguments
parser = ArgumentParser(description="Bipartite Topology")
parser.add_argument('-n',
                    dest="half_switches",
                    type=int,
                    action="store",
                    help="Number of switches on each side of the bipartite topology",
                    required=True)

parser.add_argument('-b',
                    dest="bandwidth",
                    type=float,
                    action="store",
                    help="Bandwidth of network link",
                    default=10)
parser.add_argument('-d',
                    dest="delay",
                    type=float,
                    help="Delay in milliseconds of host links",
                    default=0)
parser.add_argument('-l',
                    dest="loss",
                    type=float,
                    action="store",
                    help="Packet loss percentage",
                    default=0)

parser.add_argument('-q',
                    dest="max_queue",
                    type=int,
                    action="store",
                    help="Max buffer size of network interface in packets",
                    default=100)

# Bipartite parameters
args = parser.parse_args()

class BipartiteTopo(Topo):
    # Bipartite topology
    def __init__(self, n=args.half_switches*4, bw_net=args.bandwidth, delay='%sms' % args.delay, maxq=args.max_queue, loss=None):
        super(BipartiteTopo, self ).__init__()

        switches = []
        for i in range(n/2):
            switches.append(self.addSwitch('s'+str(i+1)))

        # Link up switches in complete bipartite fashion
        for i in range(n/4):
            for j in range(n/4):
                self.addLink(switches[i], switches[j+n/4])

        # Create hosts and add links to switches
        hosts = []
        for i in range(n):
            hosts.append(self.addHost('h'+str(i+1)))
            self.addLink(switches[i/2], hosts[i])

def test():
    topo = BipartiteTopo()
    net = Mininet(topo=topo, link=TCLink, host=CPULimitedHost)
    net.start()
    dumpNodeConnections(net.hosts)
    dumpNodeConnections(net.switches)
    CLI(net)
    net.stop()
    
#def connectAllHosts():
if __name__ == '__main__':
    test()
