
import sys
import getopt
import datetime
import os
from collections import defaultdict


if __name__=="__main__":
    try:
        # opts, args = getopt.getopt(sys.argv[1:], "h:t:s:e:b:i:p:f:u", ["hourepoch=", "istimed=", "starttime=", "endtime=", "issubset=", "inputaddrfile=", "prefix=", "suffix=", "usage="])
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u", ["hourepoch=", "prefix=", "usage="])        
        
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(1)

    hourepoch = None
    pfx = None
    
    for o, a in opts:
        if o in ("-h", "--hourepoch"):
            hourepoch = int(a)
        elif o in ("-p", "--prefix"):
            pfx = a
            

    this_h_dt = datetime.datetime.utcfromtimestamp(hourepoch)
    this_h_dt_str = this_h_dt.strftime("%Y_%m_%d_%H_%M")
    mkdir_cmd = 'mkdir -p ./data/{0}/{1}_{2}/'.format(pfx, this_h_dt_str, hourepoch)
    sys.stderr.write("{0}\n".format(mkdir_cmd) )
    os.system(mkdir_cmd)

    fp = open('./data/{0}/{1}_{2}/dominantflows'.format(pfx, this_h_dt_str, hourepoch), 'w')

    line_ct = 0    

    flows = defaultdict(dict)

    for line in sys.stdin:
        line_ct += 1

        if line_ct%10000000 == 0:
            sys.stderr.write('Line ct: {}\n'.format(line_ct) )

        # # For testing
        # if line_ct%200000000 == 0:
        #     break

        if line[:24] == '# CORSARO_INTERVAL_START':
            continue

        if "|" not in line:
            continue

        parts = line.strip().split('|')
        src_ip = parts[0]
        # dst_ip = parts[1]

        src_port = int(parts[2])
        dst_port = int(parts[3])
        prot = int(parts[4])

        ip_len_val_parts = parts[7].split(',')
        val = int(ip_len_val_parts[1])

        if prot not in flows:
            flows[prot] = {}

        if dst_port not in flows[prot]:
            flows[prot][dst_port] = {}

        # if src_port not in flows[prot][dst_port]:
        #     flows[prot][dst_port][src_port] = {}

        if src_ip not in flows[prot][dst_port]:
            flows[prot][dst_port][src_ip] = 0

        flows[prot][dst_port][src_ip] += val

        
    for prot in flows:
        for dst_port in flows[prot]:
            for src_ip in flows[prot][dst_port]:
                fp.write("{0} {1} {2} {3}\n".format(prot, dst_port, src_ip, flows[prot][dst_port][src_ip]) )
            
