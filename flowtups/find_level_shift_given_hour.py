
import sys
from collections import defaultdict


fp = open(sys.argv[1], 'r')

baseline_port_to_ips = {}
port_to_ips = {}

begin_min = int(sys.argv[2])
end_min = int(sys.argv[3])

# ips_field_num specifies which field in the input file is #ips. For dstport_per_minute, #ips is field 4 (3 when index is 0). For srcs24_per_minute, #ips is field 3 (2 when index is 0)
ips_field_num = int(sys.argv[4])

# min_numsrcaddr_thresh is the minimum number of source addresses for a dstport (or srcport, iplen) we need to observe during the spike for us to be concerned that this particular dstport has some particularly anomalous behavior
min_numsrcaddr_thresh = int(sys.argv[5])

delta_thresh = 20
if len(sys.argv) == 7: # We've specified a different delta threshold
    delta_thresh = int(sys.argv[6])
delta_multiplier = 1 + delta_thresh/float(100)
    
# print len(sys.argv)
# sys.exit(1)


reqd_minute_nums = range(begin_min, end_min)

for line in fp:
    parts = line.strip().split()

    minute_num = int(parts[0].strip() )
    dstport = parts[1].strip()
    ips = int(parts[ips_field_num].strip() )

    # if minute_num >= reqd_minute_nums[0] and minute_num <= reqd_minute_nums[-1]:
    if minute_num >= begin_min and minute_num < end_min:    
        
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


# Use this code for testing find_level_shift.py
# def temp_write(port_to_ips, temp_op_fp):

#     for dstport in port_to_ips:
#         for minute_num in port_to_ips[dstport]:
#             minute_num_within_hour = int(minute_num)
#             # minute_num_epoch = 1570791600 + 60 * minute_num_within_hour # Oct 11 2019 11:00
#             # minute_num_epoch = 1570795200 + 60 * minute_num_within_hour # Oct 11 2019 12:00
#             minute_num_epoch = 1570798800 + 60 * minute_num_within_hour # Oct 11 2019 12:00            
#             temp_op_fp.write("{0} {1} {2}\n".format(dstport, minute_num_epoch, port_to_ips[dstport][minute_num]) )


# temp_op_fp_1 = open('temp1', 'w')
# temp_write(port_to_ips, temp_op_fp_1)
# temp_op_fp_2 = open('temp2', 'w')
# temp_write(baseline_port_to_ips, temp_op_fp_2)
        
        
for dstport in port_to_ips:
    avg = sum(port_to_ips[dstport].values() )/float(len(port_to_ips[dstport]) )

    # If there were some addresses sending traffic to the dstport even during baseline minutes, find if there was a significant increase towards dstport relative to baseline
    if dstport in baseline_port_to_ips:
        baseline_avg = sum(baseline_port_to_ips[dstport].values() )/float(len(baseline_port_to_ips[dstport]) )

        # if avg > baseline_avg * 1.2 and avg > min_numsrcaddr_thresh:
        if avg > baseline_avg * delta_multiplier and avg > min_numsrcaddr_thresh:            
            sys.stdout.write("{0} {1:.2f} {2:.2f}\n".format(dstport, avg, baseline_avg) )

    # If no addresses were sending traffic to the dstport during baseline minutes and if there are a significant number of addresses sending traffic during non-baseline, let's record it.
    elif avg > min_numsrcaddr_thresh:
        sys.stdout.write("{0} {1:.2f} 0\n".format(dstport, avg) )
            
    
    
