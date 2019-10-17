
import sys
from collections import defaultdict

# MIN_NUMSRCADDR_THRESH is the minimum number of source addresses for a dstport (or srcport, iplen) we need to observe during the spike for us to be concerned that this particular dstport has some particularly anomalous behavior
MIN_NUMSRCADDR_THRESH = 1000

fp = open(sys.argv[1], 'r')

baseline_port_to_ips = {}
port_to_ips = {}

begin_min = int(sys.argv[2])
end_min = int(sys.argv[3])

reqd_minute_nums = range(begin_min, end_min)

for line in fp:
    parts = line.strip().split()

    minute_num = int(parts[0].strip() )
    dstport = int(parts[1].strip() )
    ips = int(parts[3].strip() )

    if minute_num >= reqd_minute_nums[0] and minute_num <= reqd_minute_nums[-1]:
        if dstport not in port_to_ips:
            port_to_ips[dstport] = defaultdict(int)
        # if minute_num not in port_to_ips[dstport]:
        #     port_to_ips[dstport][minute_num] = defaultdict(int)
        port_to_ips[dstport][minute_num] += ips

    else:
        if dstport not in baseline_port_to_ips:
            baseline_port_to_ips[dstport] = defaultdict(int)
        # if minute_num not in baseline_port_to_ips[dstport]:
        #     baseline_port_to_ips[dstport][minute_num] = defaultdict(int)
        baseline_port_to_ips[dstport][minute_num] += ips


for dstport in port_to_ips:
    avg = sum(port_to_ips[dstport].values() )/float(len(port_to_ips[dstport]) )

    if dstport in baseline_port_to_ips:
        baseline_avg = sum(baseline_port_to_ips[dstport].values() )/float(len(baseline_port_to_ips[dstport]) )

        if avg > baseline_avg * 1.2 and avg > MIN_NUMSRCADDR_THRESH:
            sys.stdout.write("{0} {1:.2f} {2:.2f}\n".format(dstport, avg, baseline_avg) )
    
