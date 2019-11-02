
import sys
from collections import defaultdict

fp = open(sys.argv[1], 'r')

# ips_field_num specifies which field in the input file is #ips. For dstport_per_minute, #ips is field 4 (3 when index is 0). For srcs24_per_minute, #ips is field 3 (2 when index is 0)
ips_field_num = int(sys.argv[2])

port_to_ips = defaultdict(int)

for line in fp:
    parts = line.strip().split()

    minute_num = int(parts[0].strip() )
    dstport = int(parts[1].strip() )
    ips = int(parts[ips_field_num].strip() )    

    port_to_ips[dstport] += ips


for dstport in port_to_ips:
    sys.stdout.write("{0} {1:.1f}\n".format(dstport, port_to_ips[dstport]/float(60) ) )
    
