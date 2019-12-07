
# from scapy.all import *
import sys
import pyshark
import pprint
import datetime
from collections import defaultdict


inp_fname = sys.argv[1]
op_fname = sys.argv[2]

num_pkts = 0

pkts = pyshark.FileCapture(inp_fname, keep_packets = False)

pkts_per_typ = defaultdict(int)

for pkt in pkts:

    num_pkts += 1    
    if num_pkts%10000 == 0:
        sys.stderr.write("Done with {0} packets at: {1}\n".format(num_pkts, str(datetime.datetime.now() ) ) )

    if num_pkts%800000 == 0:
        break

    if (pkt.highest_layer == "SIP"):
        if "method" in pkt.sip.field_names:
            pkt_typ = pkt.sip.method
        elif "status_line" in pkt.sip.field_names:
            pkt_typ = pkt.sip.status_line

        pkts_per_typ[pkt_typ] += 1

        
op_fp = open(op_fname, 'w')
for pkt_typ in pkts_per_typ:
    op_fp.write("{0}|{1}\n".format(pkt_typ, pkts_per_typ[pkt_typ]) )

        
sys.stderr.write("Number of packets: {0}\n".format(num_pkts) )
