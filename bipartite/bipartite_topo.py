#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import output, debug
from mininet.util import dumpNetConnections
from mininet.cli import CLI

import os
import re
import signal
from argparse import ArgumentParser
from time import sleep

class BipartiteTopo(Topo):
    # Bipartite topology
    def __init__(self, n, bw_net, delay, maxq, loss):
        super(BipartiteTopo, self ).__init__()

        switches = []
        for i in range(n/2):
            switches.append(self.addSwitch('s'+str(i+1)))

        # Link up switches in complete bipartite fashion
        for i in range(n/4):
            self.addLink(switches[0], switches[i+n/4])

        for i in range(1,n/4):
            self.addLink(switches[n/4], switches[i])

        # Create hosts and add links to switches
        hosts = []
        for i in range(n):
            hosts.append(self.addHost('h'+str(i+1)))
            self.addLink(switches[i/2], hosts[i])

def dumpNodeAddresses( nodes ):
    "Dump addresses to/from nodes."

    for node in nodes:
        output("Host "+node.name+" has IP address "+node.IP()+" and MAC address "+node.MAC()+"\n")

def dumpNetAddresses( net ):
    "Dump addresses in network"
    nodes = net.controllers + net.switches + net.hosts
    dumpNodeAddresses( nodes )

def _parsePerf( perfOutput ):
    """Parse perf output and return bandwidth.
       perfOutput: string
       returns: result string"""
    r = r'([\d\.]+ \w+/sec)'
    m = re.findall( r, perfOutput )
    if m:
        return m[-1]
    else:
        # was: raise Exception(...)
        error( 'could not parse perf output: ' + perfOutput )
        return ''


def perf( net, hosts=None ):
    """Performance between all specified hosts.
       hosts: list of hosts"""
    if not hosts:
        hosts = net.hosts
        output( '*** Perf: testing performance\n' )
    for node in hosts:
        output( '%s -> ' % node.name )
        node.cmd( 'killall -9 iperf' )
        node.sendCmd('./iperf.sh s', printPid=True)
        nodeLastPid = 0
        while node.lastPid is None:
            node.monitor()
        nodeLastPid = node.lastPid
        for dest in hosts:
            if node != dest:
                while 'Connected' not in dest.cmd('sh -c "echo A | telnet -e A %s 5001"' % node.IP()):
                    #output( 'waiting %s %s\n' % (node.name, dest.name ))
                    sleep(.5)
                result = dest.cmd('./iperf.sh c %s' % (node.IP()) )
                output(('%s: %s ' % (dest.name,_parsePerf(result))) if result else 'X ' )
        output( '\n' )
        os.kill(nodeLastPid, signal.SIGKILL)
        node.waitOutput()
        node.cmd( 'killall -9 iperf' )

def test():
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
                    default=3)
    parser.add_argument('-l',
                    dest="loss",
                    type=float,
                    action="store",
                    help="Packet loss percentage",
                    default=5)

    parser.add_argument('-q',
                    dest="max_queue",
                    type=int,
                    action="store",
                    help="Max buffer size of network interface in packets",
                    default=100)

    # Bipartite parameters
    args = parser.parse_args()


    topo = BipartiteTopo(n=args.half_switches*4, bw_net=args.bandwidth, delay='%sms' % args.delay, maxq=args.max_queue, loss=None)
    net = Mininet(topo=topo, link=TCLink, host=CPULimitedHost)
    #for switch in net.switches:
    #    switch.setIP('10.1.0.'+str(net.switches.index(switch)+1))
    net.start()
    dumpNetConnections(net)
    dumpNodeAddresses(net.hosts)
    #dumpNodeAddresses(net.switches)
    net.pingAll()
    perf(net)
    CLI(net)
    net.stop()
    
if __name__ == '__main__':
    test()

topos = { 'bipartitetopo': ( lambda n, b=10, d=3, q=100, l=5: BipartiteTopo(n=n*4, bw_net=b, delay='%sms' % d, maxq=q, loss=l) ) }
