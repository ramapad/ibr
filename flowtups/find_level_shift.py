
# This script should take as input a range of epoch times that are "reqd" and a longer range of epoch times that are baseline.
# It should also take as input the specific experiment we are interested in, specified by a directory hierarchy.
# It should also take as input the feature (ttl, iplen etc.) that we are interested in

# TODO: Find a way to test this script more thoroughly

import sys
import shlex, subprocess
from collections import defaultdict


def process_fname(fname, hourepoch):
    sys.stderr.write("Processing {0}\n".format(fname) )
    fp = open(fname)
    for line in fp:
        parts = line.strip().split()

        minute_num_within_hour = int(parts[0].strip() )
        minute_num = hourepoch + 60 * minute_num_within_hour
        
        dstport = parts[1].strip()
        ips = int(parts[ips_field_num].strip() )

        if minute_num >= begin_reqd_min and minute_num <= end_reqd_min:
            if dstport not in port_to_ips:
                port_to_ips[dstport] = defaultdict(int)
            # if minute_num not in port_to_ips[dstport]:
            #     port_to_ips[dstport][minute_num] = defaultdict(int)
            port_to_ips[dstport][minute_num] += ips

        elif minute_num >= begin_baseline_min and minute_num <= end_baseline_min:
            if dstport not in baseline_port_to_ips:
                baseline_port_to_ips[dstport] = defaultdict(int)
            # if minute_num not in baseline_port_to_ips[dstport]:
            #     baseline_port_to_ips[dstport][minute_num] = defaultdict(int)
            baseline_port_to_ips[dstport][minute_num] += ips


begin_reqd_min = int(sys.argv[1])
# Subtract 60 seconds since we are not including the end_baseline_min. That is: if we specify baseline hours to be from 2:00 to 3:00, we don't want to include the 3:00 to 3:01 minute.
end_reqd_min = int(sys.argv[2]) - 60

begin_baseline_min  = int(sys.argv[3])
# Subtract 60 seconds since we are not including the end_baseline_min. That is: if we specify baseline hours to be from 2:00 to 3:00, we don't want to include the 3:00 to 3:01 minute.
end_baseline_min = int(sys.argv[4]) - 60 

inp_path = sys.argv[5]
# Ensure there is a trailing slash at the end of the path, so that the find command can work correctly
if inp_path[-1] != '/':
    inp_path = "{0}/".format(inp_path)

fname = sys.argv[6]

# ips_field_num specifies which field in the input file is #ips. For dstport_per_minute, #ips is field 4 (3 when index is 0). For srcs24_per_minute, #ips is field 3 (2 when index is 0)
ips_field_num = int(sys.argv[7])

# min_numsrcaddr_thresh is the minimum number of source addresses for a dstport (or srcport, iplen) we need to observe during the spike for us to be concerned that this particular dstport has some particularly anomalous behavior
min_numsrcaddr_thresh = int(sys.argv[8])

reqd_minute_nums = range(begin_reqd_min, end_reqd_min)

baseline_port_to_ips = {}
port_to_ips = {}

find_cmd = 'find . -path "{0}*/{1}*"'.format(inp_path, fname)
sys.stderr.write("{0}\n".format(find_cmd))
args = shlex.split(find_cmd)
fnames = subprocess.check_output(args)
fnames_split = fnames.strip().split("\n")
for full_fname in fnames_split:

    if 'prot_dstport_' in full_fname:
        continue
    
    sys.stderr.write("Found {0}\n".format(full_fname) )    
    
    parts = full_fname.strip().split('/')

    dir_name_with_time_parts = parts[-2].strip().split('_')
    hourepoch = int(dir_name_with_time_parts[-1])
    
    # The minutes in this file will be encoded in the file's suffix
    fname = parts[-1]
    fname_parts = fname.strip().split('_')
    fname_begin_time = int(fname_parts[-3])
    fname_end_time = int(fname_parts[-1])
    # sys.stderr.write("{0} {1} {2}\n".format(full_fname, fname_begin_time, fname_end_time) )
    # If any time within this file falls within the baseline range, then we should process the file
    # Suppose the begin_baseline_min = 9:59 AM. Then we would need minute 59 from the 9 AM file
    # Suppose the end_baseline_min = 11:01 AM. Then we would need minute 1 from the 11 AM file
    # TODO: Write these comments above in a better way. Change the variable names from min_thresh and max_thresh to something better
    min_thresh = begin_baseline_min - (fname_end_time - fname_begin_time)
    max_thresh = end_baseline_min + (fname_end_time - fname_begin_time)

    if fname_begin_time >= min_thresh and fname_end_time <= max_thresh:
        process_fname(full_fname, hourepoch)

    sys.stderr.write("Length of baseline_port_to_ips: {0}\n".format(len(baseline_port_to_ips) ) )
    sys.stderr.write("Length of port_to_ips: {0}\n".format(len(port_to_ips) ) )


# Use this code for testing output against find_level_shift_given_hour.py
# def temp_write(port_to_ips, temp_op_fp):

#     for dstport in port_to_ips:
#         for minute_num in port_to_ips[dstport]:
#             temp_op_fp.write("{0} {1} {2}\n".format(dstport, minute_num, port_to_ips[dstport][minute_num]) )


# temp_op_fp_1 = open('test1', 'w')
# temp_write(port_to_ips, temp_op_fp_1)
# temp_op_fp_2 = open('test2', 'w')
# temp_write(baseline_port_to_ips, temp_op_fp_2)

    
for dstport in port_to_ips:
    avg = sum(port_to_ips[dstport].values() )/float(len(port_to_ips[dstport]) )

    # If there were some addresses sending traffic to the dstport even during baseline minutes, find if there was a significant increase towards dstport relative to baseline
    if dstport in baseline_port_to_ips:
        baseline_avg = sum(baseline_port_to_ips[dstport].values() )/float(len(baseline_port_to_ips[dstport]) )

        if avg > baseline_avg * 1.2 and avg > min_numsrcaddr_thresh:
            sys.stdout.write("{0} {1:.2f} {2:.2f}\n".format(dstport, avg, baseline_avg) )

    # If no addresses were sending traffic to the dstport during baseline minutes and if there are a significant number of addresses sending traffic during non-baseline, let's record it.
    elif avg > min_numsrcaddr_thresh:
        sys.stdout.write("{0} {1:.2f} 0\n".format(dstport, avg) )
            

        
