
from scapy.all import *
import pprint
import datetime


inp_fname = sys.argv[1]


num_pkts = 0
# pkts = rdpcap(inp_fname) 
# for pkt in pkts:

for (pkt_data, pkt_metadata,) in RawPcapReader(inp_fname):

    num_pkts += 1    
    if num_pkts%10000 == 0:
        sys.stderr.write("Done with {0} packets at: {1}\n".format(num_pkts, str(datetime.datetime.now() ) ) )

    # pprint.pprint(pkt_data)
    # print("Done with data")
    # pprint.pprint(pkt_metadata)
    # sys.exit(1)

    

sys.stderr.write("Number of packets: {0}\n".format(num_pkts) )
