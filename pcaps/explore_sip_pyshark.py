
# from scapy.all import *
import sys
import pyshark
import pprint
import datetime


inp_fname = sys.argv[1]

num_pkts = 0

pkts = pyshark.FileCapture(inp_fname)

for pkt in pkts:

    num_pkts += 1    
    if num_pkts%10000 == 0:
        sys.stderr.write("Done with {0} packets at: {1}\n".format(num_pkts, str(datetime.datetime.now() ) ) )

    # print(pkt)
    # pkt.pretty_print()
    # sys.exit(1)
    
    # if 
    # if (pkt.highest_layer == "DATA"):
    #     pkt.pretty_print()
    #     sys.exit(1)
    # pprint.pprint(pkt)
    # print("Done with data")
    # pprint.pprint(pkt_metadata)
    # sys.exit(1)

    # We are primarily interested in UDP SIP packets
    # if UDP not in pkt:
    #     continue

    # udp_pkt = pkt[UDP]
    # # udp_pkt = pkt_data[UDP]
    # if udp_pkt.dport != 5060:
    #     continue

    # udp_pkt.show()
    # pprint.pprint(str(udp_pkt.payload))
    

sys.stderr.write("Number of packets: {0}\n".format(num_pkts) )
