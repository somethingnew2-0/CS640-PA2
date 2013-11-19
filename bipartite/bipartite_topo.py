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
    def __init__(self, n, bw, delay, maxq, loss):
        super(BipartiteTopo, self ).__init__()
        switches = []
        for i in range(n/2):
            switches.append(self.addSwitch('s'+str(i+1)))

        # Link up switches in loop-free bipartite fashion
        for i in range(n/4):
            self.addLink(switches[i], switches[i+n/4], bw=bw, delay=delay, max_queue_size=maxq, loss=loss)
        for i in range(n/4, n/2-1):
            self.addLink(switches[i], switches[i-(n/4)+1], bw=bw, delay=delay, max_queue_size=maxq, loss=loss)

        # Create hosts and add links to switches
        hosts = []
        for i in range(n):
            hosts.append(self.addHost('h'+str(i+1)))
            self.addLink(switches[i/2], hosts[i], bw=bw, delay=delay, max_queue_size=maxq, loss=loss)

def dumpLinks( topo ):
    "Dump the link connections and their bandwidths."
    output("Links:\n")
    links = topo.links()
    for li in links:
        output('('+li[0]+","+li[1]+") with bandwidth "+str(topo.linkInfo(li[0],li[1])['bw'])+"Mbps\n")

def dumpNodeIPs( nodes ):
    "Dump IP addresses of nodes"
    
    for node in nodes:
        output(node.name+" has IP address "+node.IP()+"\n")

def dumpNodeAddresses( nodes ):
    "Dump IP and MAC addresses of nodes."

    for node in nodes:
        output(node.name+" has IP address "+node.IP()+" and MAC address "+node.MAC()+"\n")

def dumpNetAddresses( net ):
    "Dump addresses in network"
    output("Nodes:\n")
    nodes = net.controllers + net.switches
    dumpNodeIPs(nodes)
    dumpNodeAddresses(net.hosts)

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
    for node in hosts[:-1]:
        output( '%s -> ' % node.name )
        node.cmd( 'killall -9 iperf' )
        node.sendCmd('./iperf.sh s', printPid=True)
        nodeLastPid = 0
        while node.lastPid is None:
            node.monitor()
        nodeLastPid = node.lastPid
        for dest in hosts:
            if hosts.index(node) < hosts.index(dest):
                while 'Connected' not in dest.cmd('sh -c "echo A | telnet -e A %s 5001"' % node.IP()):
                    #output( 'waiting %s %s\n' % (node.name, dest.name ))
                    sleep(.5)
                result = dest.cmd('./iperf.sh c %s' % (node.IP()) )
                output(('%s: %s ' % (dest.name,_parsePerf(result))) if result else 'X ' )
        output( '\n' )
        os.kill(nodeLastPid, signal.SIGKILL)
        node.waitOutput()
        node.cmd( 'killall -9 iperf' )

def perfSetup( net ):
    "Set up iperf servers on all hosts"
    hosts = net.hosts
    for node in hosts[:-1]:
        node.cmd('iperf -s -w 16m -p 5001 -i 1 >> iperf-recv.txt &')
        node.cmd('echo "" > iperf-recv.txt')
    hosts[-1].cmd('iperf -s -w 16m -p 5001 -i 1 >> iperf-recv.txt &')

def perfTakedown( net ):
    "kill all iperf servers running"
    hosts = net.hosts
    for node in hosts:
        node.cmd('killall -9 iperf')

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


    topo = BipartiteTopo(n=args.half_switches*4, bw=args.bandwidth, delay='%sms' % args.delay, maxq=args.max_queue, loss=args.loss)
    net = Mininet(topo=topo, link=TCLink, host=CPULimitedHost)
    #for switch in net.switches:
    #    switch.setIP('10.1.0.'+str(net.switches.index(switch)+1))
    net.start()
    net.pingAll()
    dumpLinks(net.topo)
    dumpNetAddresses(net)
    perfSetup(net)
    #perf(net)
    CLI(net)
    perfTakedown(net)
    net.stop()
    
if __name__ == '__main__':
    test()

topos = { 'bipartitetopo': ( lambda n, b=10, d=3, q=100, l=5: BipartiteTopo(n=n*4, bw=b, delay='%sms' % d, maxq=q, loss=l) ) }
