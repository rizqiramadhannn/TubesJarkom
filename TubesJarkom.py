	#!/usr/bin/env python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from mininet.log import setLogLevel
import os

if '__main__' == __name__:
	setLogLevel('info')
	net = Mininet(link=TCLink)
	value = 0
	os.system('mn -c')

	#add host and router
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')
	r1 = net.addHost('r1')
	r2 = net.addHost('r2')
	r3 = net.addHost('r3')
	r4 = net.addHost('r4')

	#set variabel bandwidth
	bw1={'bw':1}
	bw2={'bw':0.5}

	#add link 
	net.addLink(r1, h1, max_queue_size=20, intfName1 = 'r1-eth0', intfName2 = 'h1-eth0', cls=TCLink, **bw1)
	net.addLink(r2, h1, max_queue_size=20, intfName1 = 'r2-eth1', intfName2 = 'h1-eth1', cls=TCLink, **bw1)
	net.addLink(r3, h2, max_queue_size=20, intfName1 = 'r3-eth0', intfName2 = 'h2-eth0', cls=TCLink, **bw1)
	net.addLink(r4, h2, max_queue_size=20, intfName1 = 'r4-eth1', intfName2 = 'h2-eth1', cls=TCLink, **bw1)
	net.addLink(r1, r3, max_queue_size=20, intfName1 = 'r1-eth1', intfName2 = 'r3-eth1', cls=TCLink, **bw2)
	net.addLink(r1, r4, max_queue_size=20, intfName1 = 'r1-eth2', intfName2 = 'r4-eth2', cls=TCLink, **bw1)
	net.addLink(r2, r4, max_queue_size=20, intfName1 = 'r2-eth0', intfName2 = 'r4-eth0', cls=TCLink, **bw1)
	net.addLink(r2, r3, max_queue_size=20, intfName1 = 'r2-eth2', intfName2 = 'r3-eth2', cls=TCLink, **bw2)
	net.build()

	#host config 1
	h1.cmd("ifconfig h1-eth0 0")
	h1.cmd("ifconfig h1-eth1 0")
	h1.cmd("ifconfig h1-eth0 192.168.10.1 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 192.168.60.2 netmask 255.255.255.0")
	
	#host config 2
	h2.cmd("ifconfig h2-eth0 0")
	h2.cmd("ifconfig h2-eht1 0")
	h2.cmd("ifconfig h2-eth0 192.168.30.2 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 192.168.40.1 netmask 255.255.255.0") 
	
	#router config
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 2 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 3 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 4 > /proc/sys/net/ipv4/ip_forward")
	
	#config router 1
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	r1.cmd("ifconfig r1-eth0 192.168.10.2 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 192.168.20.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 192.168.70.1 netmask 255.255.255.0")

	#config router 2
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	r2.cmd("ifconfig r2-eth0 192.168.50.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.60.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 192.168.80.1 netmask 255.255.255.0")

	#config router 3
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	r3.cmd("ifconfig r3-eth0 192.168.30.1 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.20.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 192.168.80.2 netmask 255.255.255.0")

	#config router 4
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	r4.cmd("ifconfig r4-eth0 192.168.50.1 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.40.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 192.168.70.2 netmask 255.255.255.0")

	
	#Membuat routing static
  #h1
	h1.cmd("ip rule add from 192.168.10.1 table 1")
	h1.cmd("ip rule add from 192.168.60.2 table 2")
	h1.cmd("ip route add 192.168.10.0/24 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 192.168.10.2 dev h1-eth0 table 1")
	h1.cmd("ip route add 192.168.60.0/24 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 192.168.60.1 dev h1-eth1 table 2")
	h1.cmd("ip route add default scope global nexthop via 192.168.10.2 dev h1-eth0")
	h1.cmd("ip route add default scope global nexthop via 192.168.60.1 dev h1-eth1")

  #h2
	h2.cmd("ip rule add from 192.168.30.2 table 1")
	h2.cmd("ip rule add from 192.168.40.1 table 2")
	h2.cmd("ip route add 192.168.30.0/24 dev h2-eth0 scope link table 1")
	h2.cmd("ip route add default via 192.168.30.1 dev h2-eth0 table 1")
	h2.cmd("ip route add 192.168.40.0/24 dev h2-eth1 scope link table 2")
	h2.cmd("ip route add default via 192.168.40.2 dev h2-eth1 table 2")
	h2.cmd("ip route add default scope global nexthop via 192.168.30.1 dev h2-eth0")
	h2.cmd("ip route add default scope global nexthop via 192.168.40.2 dev h2-eth1")
		
	#router 1
	r1.cmd("route add -net 192.168.50.0/24 gw 192.168.70.2")
	r1.cmd("route add -net 192.168.80.0/24 gw 192.168.20.2")
	r1.cmd("route add -net 192.168.60.0/24 gw 192.168.70.2")
	r1.cmd("route add -net 192.168.30.0/24 gw 192.168.20.2")
	r1.cmd("route add -net 192.168.40.0/24 gw 192.168.70.2")

  #router 2
	r2.cmd("route add -net 192.168.20.0/24 gw 192.168.80.2")
	r2.cmd("route add -net 192.168.70.0/24 gw 192.168.50.1")
	r2.cmd("route add -net 192.168.30.0/24 gw 192.168.80.2")
	r2.cmd("route add -net 192.168.40.0/24 gw 192.168.50.1")
	r2.cmd("route add -net 192.168.10.0/24 gw 192.168.80.2")

  #router 3
	r3.cmd("route add -net 192.168.10.0/24 gw 192.168.20.1")
	r3.cmd("route add -net 192.168.60.0/24 gw 192.168.80.1")
	r3.cmd("route add -net 192.168.70.0/24 gw 192.168.20.1")
	r3.cmd("route add -net 192.168.50.0/24 gw 192.168.80.1")
	r3.cmd("route add -net 192.168.40.0/24 gw 192.168.80.1")

  #router 4
	r4.cmd("route add -net 192.168.60.0/24 gw 192.168.50.2")
	r4.cmd("route add -net 192.168.10.0/24 gw 192.168.70.1")
	r4.cmd("route add -net 192.168.20.0/24 gw 192.168.70.1")
	r4.cmd("route add -net 192.168.30.0/24 gw 192.168.70.1")
	r4.cmd("route add -net 192.168.80.0/24 gw 192.168.50.2")


	#menjalankan iPerf di background process
	h2.cmd('iperf -s &')
	h1.cmd('iperf -t 10 -c 192.168.30.2 &')
	
	CLI(net)
	net.stop()
