
# This script explores flow tuples

import sys
import getopt
import datetime
import os
from collections import defaultdict


def flush_prev_minute(prev_minute_num, pkts, fp, src_ports_per_min, src_ports_fp, dst_ports_per_min, dst_ports_fp, prots_per_min, prots_fp, src_s24s_per_min, src_s24s_fp, dst_s24s_per_min, dst_s24s_fp, ip_lens_per_min, ip_lens_fp, ttls_per_min, ttls_fp, pkts_per_min, pkts_per_min_fp, src_ips_per_min, src_ips_fp):
    
    # for prot in pkts:
    #     for dst_port in pkts[prot]:
    #         for src_s24 in pkts[prot][dst_port]:
    #             this_d = pkts[prot][dst_port][src_s24]
    #             fp.write("{} {} {} {} {} {}\n".format(prev_minute_num, prot, dst_port, src_s24, len(this_d["ips"]), this_d["pkts"]) )

    for prot in pkts:
        for dst_port in pkts[prot]:
            for src_port in pkts[prot][dst_port]:
                for ip_len in pkts[prot][dst_port][src_port]:
                    this_d = pkts[prot][dst_port][src_port][ip_len]
                    fp.write("{0} {1} {2} {3} {4} {5} {6} {7}\n".format(prev_minute_num, prot, dst_port, src_port, ip_len, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"]) )

    for src_port in src_ports_per_min:
        this_d = src_ports_per_min[src_port]
        src_ports_fp.write("{} {} {} {} {}\n".format(prev_minute_num, src_port, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )

    for dst_port in dst_ports_per_min:
        this_d = dst_ports_per_min[dst_port]
        dst_ports_fp.write("{} {} {} {} {}\n".format(prev_minute_num, dst_port, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )

    for prot in prots_per_min:
        this_d = prots_per_min[prot]
        prots_fp.write("{} {} {} {} {}\n".format(prev_minute_num, prot, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )

    for src_s24 in src_s24s_per_min:
        this_d = src_s24s_per_min[src_s24]
        src_s24s_fp.write("{} {} {} {}\n".format(prev_minute_num, src_s24, len(this_d["ips"]), this_d["pkts"] ) )

    for dst_s24 in dst_s24s_per_min:
        this_d = dst_s24s_per_min[dst_s24]
        dst_s24s_fp.write("{} {} {} {}\n".format(prev_minute_num, dst_s24, len(this_d["ips"]), this_d["pkts"] ) )

    for ip_len in ip_lens_per_min:
        this_d = ip_lens_per_min[ip_len]
        ip_lens_fp.write("{} {} {} {} {}\n".format(prev_minute_num, ip_len, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )

    for ttl in ttls_per_min:
        this_d = ttls_per_min[ttl]
        ttls_fp.write("{} {} {} {} {}\n".format(prev_minute_num, ttl, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )

    pkts_per_min_fp.write("{} {}\n".format(prev_minute_num, pkts_per_min) )
    src_ips_fp.write("{} {}\n".format(prev_minute_num, len(src_ips_per_min) ) )

    # Re-initialize everything

    src_ports_per_min = {}
    dst_ports_per_min = {}
    prots_per_min = {}
    src_s24s_per_min = {}
    dst_s24s_per_min = {}
    ip_lens_per_min = {}
    ttls_per_min = {}        
    src_ips_per_min = set()
    pkts_per_min = 0

    pkts = defaultdict(dict)

    return src_ports_per_min, dst_ports_per_min, prots_per_min, src_s24s_per_min, dst_s24s_per_min,  ip_lens_per_min, ttls_per_min, src_ips_per_min, pkts_per_min, pkts


if __name__=="__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:t:s:e:b:i:p:f:u", ["hourepoch=", "istimed=", "starttime=", "endtime=", "issubset=", "inputaddrfile=", "prefix=", "suffix=", "usage="])
        
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(1)

    hourepoch = None
    istimed = 0
    starttime = None
    endtime = None
    issubset = 0
    inputaddrfile = None
    pfx = None
    suf = None

    for o, a in opts:
        if o in ("-h", "--hourepoch"):
            hourepoch = int(a)
        elif o in ("-t", "--istimed"):
            istimed = int(a)
        elif o in ("-s", "--starttime"):
            starttime = int(a)
        elif o in ("-e", "--endtime"):
            endtime = int(a)
        elif o in ("-b", "--issubset"):
            issubset = int(a)
        elif o in ("-i", "--inputaddrfile"):
            inputaddrfile = a            
        elif o in ("-p", "--prefix"):
            pfx = a
        elif o in ("-f", "--suffix"):
            suf = a
        else:
            assert False, "unhandled option"


    # print issubset
    # print inputaddrfile
    # print suf

    
    if issubset == 1:
        reqd_addrs = set()
        inp_fp = open(inputaddrfile)
        for line in inp_fp:
            reqd_addrs.add(line[:-1])

    # sys.exit(1)

    this_h_dt = datetime.datetime.utcfromtimestamp(hourepoch)
    this_h_dt_str = this_h_dt.strftime("%Y_%m_%d_%H_%M")
    mkdir_cmd = 'mkdir -p ./data/{0}/{1}_{2}/'.format(pfx, this_h_dt_str, hourepoch)
    sys.stderr.write("{0}\n".format(mkdir_cmd) )
    os.system(mkdir_cmd)
    
    fp = open('./data/{0}/{1}_{3}/prot_dstport_srcs24_per_minute_{2}'.format(pfx, this_h_dt_str, suf, hourepoch), 'w')
    src_ports_fp = open('./data/{0}/{1}_{3}/srcport_per_minute_{2}'.format(pfx, this_h_dt_str, suf, hourepoch), 'w')
    dst_ports_fp = open('./data/{0}/{1}_{3}/dstport_per_minute_{2}'.format(pfx, this_h_dt_str, suf, hourepoch), 'w')
    prots_fp = open('./data/{0}/{1}_{3}/prot_per_minute_{2}'.format(pfx, this_h_dt_str, suf, hourepoch), 'w')
    src_s24s_fp = open('./data/{0}/{1}_{3}/srcs24_per_minute_{2}'.format(pfx, this_h_dt_str, suf, hourepoch), 'w')
    dst_s24s_fp = open('./data/{0}/{1}_{3}/dsts24_per_minute_{2}'.format(pfx, this_h_dt_str, suf, hourepoch), 'w')
    ip_lens_fp = open('./data/{0}/{1}_{3}/iplens_per_minute_{2}'.format(pfx, this_h_dt_str, suf, hourepoch), 'w')
    ttls_fp = open('./data/{0}/{1}_{3}/ttls_per_minute_{2}'.format(pfx, this_h_dt_str, suf, hourepoch), 'w')
    src_ips_fp = open('./data/{0}/{1}_{3}/srcips_per_minute_{2}'.format(pfx, this_h_dt_str, suf, hourepoch), 'w')
    pkts_per_min_fp = open('./data/{0}/{1}_{3}/pkts_per_minute_{2}'.format(pfx, this_h_dt_str, suf, hourepoch), 'w')
    
    line_ct = 0
    must_collect_stats_this_min = 0 # Specifies whether we should process this minute or not
    must_flush = 0 # Specifies whether we should flush collected stats from the previous minute to all the files

    src_ports_per_min = {}
    dst_ports_per_min = {}
    prots_per_min = {}
    src_s24s_per_min = {}
    dst_s24s_per_min = {}
    ip_lens_per_min = {}
    ttls_per_min = {}
    src_ips_per_min = set()
    pkts_per_min = 0

    pkts = defaultdict(dict)

    
    for line in sys.stdin:
        line_ct += 1

        if line_ct%10000000 == 0:
            sys.stderr.write('Line ct: {}\n'.format(line_ct) )

        if line[:24] == '# CORSARO_INTERVAL_START':
            # Flush aggregate stats from the last minute
            # print line

            parts = line.strip().split()
            minute_num = int(parts[2])

            # If the previous minute was a minute for which we collected stats, flush stats to disk
            # Note: I am only setting must_collect_stats_this_min for *this minute* later. So the value in the variable currently refers to the value for the previous minute
            if must_collect_stats_this_min == 1:
                must_flush = 1
            else:
                must_flush = 0

            if must_flush == 1:
                # Since we are printing stats for the previous minute, we should subtract 1 from this minute_num            
                prev_minute_num = minute_num - 1
                src_ports_per_min, dst_ports_per_min, prots_per_min, src_s24s_per_min, dst_s24s_per_min,  ip_lens_per_min, ttls_per_min, src_ips_per_min, pkts_per_min, pkts = flush_prev_minute(prev_minute_num, pkts, fp, src_ports_per_min, src_ports_fp, dst_ports_per_min, dst_ports_fp, prots_per_min, prots_fp, src_s24s_per_min, src_s24s_fp, dst_s24s_per_min, dst_s24s_fp, ip_lens_per_min, ip_lens_fp, ttls_per_min, ttls_fp, pkts_per_min, pkts_per_min_fp, src_ips_per_min, src_ips_fp)

            # Decide whether we should collect stats for *this minute*
            if istimed == 1:
                minute_epoch = hourepoch + minute_num * 60            
                if ( (minute_epoch >= starttime) and (minute_epoch < endtime) ):
                    must_collect_stats_this_min = 1
                    sys.stderr.write("{0} {1} {2}\n".format(minute_epoch, endtime, must_collect_stats_this_min) )
                else:
                    must_collect_stats_this_min = 0
                    sys.stderr.write("{0} {1} {2}\n".format(minute_epoch, endtime, must_collect_stats_this_min) )                    
                    if minute_epoch >= endtime:
                        # We are done.
                        break
            else:
                must_collect_stats_this_min = 1
            

        if "|" not in line:
            continue

        if must_collect_stats_this_min == 0:
            continue

        parts = line.strip().split('|')
        src_ip = parts[0]

        if issubset == 1:
            if src_ip not in reqd_addrs:
                continue
        
        src_s24 = src_ip[:src_ip.rfind('.')]
        dst_ip = parts[1]
        dst_s24 = dst_ip[:dst_ip.rfind('.')]
        src_port = int(parts[2])
        dst_port = int(parts[3])
        prot = int(parts[4])
        ttl = parts[5]
        # tcp_flags = parts[6]
        ip_len_val = parts[7]
        ip_len_val_parts = parts[7].split(',')
        ip_len = ip_len_val_parts[0]
        val = int(ip_len_val_parts[1])

        if prot not in pkts:
            pkts[prot] = {}

        if dst_port not in pkts[prot]:
            pkts[prot][dst_port] = {}

        if src_port not in pkts[prot][dst_port]:
            pkts[prot][dst_port][src_port] = {}

        if ip_len not in pkts[prot][dst_port][src_port]:
            pkts[prot][dst_port][src_port][ip_len] = {"s24s" : set(), "ips" : set(), "pkts" : 0}

        pkts[prot][dst_port][src_port][ip_len]["s24s"].add(src_s24)        
        pkts[prot][dst_port][src_port][ip_len]["ips"].add(src_ip)
        pkts[prot][dst_port][src_port][ip_len]["pkts"] += val

        # if src_s24 not in pkts[prot][dst_port]:
        #     pkts[prot][dst_port][src_s24] = {"ips" : set(), "pkts" : 0}

        # pkts[prot][dst_port][src_s24]["ips"].add(src_ip)
        # pkts[prot][dst_port][src_s24]["pkts"] += val

        if dst_port not in dst_ports_per_min:
            dst_ports_per_min[dst_port] = {"s24s" : set(), "ips" : set(), "pkts" : 0}
        dst_ports_per_min[dst_port]["s24s"].add(src_s24)    
        dst_ports_per_min[dst_port]["ips"].add(src_ip)
        dst_ports_per_min[dst_port]["pkts"] += val    

        if src_port not in src_ports_per_min:
            src_ports_per_min[src_port] = {"s24s" : set(), "ips" : set(), "pkts" : 0}
        src_ports_per_min[src_port]["s24s"].add(src_s24)    
        src_ports_per_min[src_port]["ips"].add(src_ip)
        src_ports_per_min[src_port]["pkts"] += val

        if prot not in prots_per_min:
            prots_per_min[prot] = {"s24s" : set(), "ips" : set(), "pkts" : 0}
        prots_per_min[prot]["s24s"].add(src_s24)    
        prots_per_min[prot]["ips"].add(src_ip)
        prots_per_min[prot]["pkts"] += val

        if src_s24 not in src_s24s_per_min:
            src_s24s_per_min[src_s24] = {"ips" : set(), "pkts" : 0}
        src_s24s_per_min[src_s24]["ips"].add(src_ip)
        src_s24s_per_min[src_s24]["pkts"] += val    

        if dst_s24 not in dst_s24s_per_min:
            dst_s24s_per_min[dst_s24] = {"ips" : set(), "pkts" : 0}
        dst_s24s_per_min[dst_s24]["ips"].add(src_ip)
        dst_s24s_per_min[dst_s24]["pkts"] += val

        if ip_len not in ip_lens_per_min:
            ip_lens_per_min[ip_len] = {"s24s" : set(), "ips" : set(), "pkts" : 0}
        ip_lens_per_min[ip_len]["s24s"].add(src_s24)    
        ip_lens_per_min[ip_len]["ips"].add(src_ip)
        ip_lens_per_min[ip_len]["pkts"] += val

        if ttl not in ttls_per_min:
            ttls_per_min[ttl] = {"s24s" : set(), "ips" : set(), "pkts" : 0}
        ttls_per_min[ttl]["s24s"].add(src_s24)    
        ttls_per_min[ttl]["ips"].add(src_ip)
        ttls_per_min[ttl]["pkts"] += val

        src_ips_per_min.add(src_ip)
        pkts_per_min += val


    # Flush last minute if necessary

    if must_collect_stats_this_min == 1:
        must_flush = 1
    else:
        must_flush = 0
    
    if must_flush == 1:    
        prev_minute_num += 1
        src_ports_per_min, dst_ports_per_min, prots_per_min, src_s24s_per_min, dst_s24s_per_min,  ip_lens_per_min, ttls_per_min, src_ips_per_min, pkts_per_min, pkts = flush_prev_minute(prev_minute_num, pkts, fp, src_ports_per_min, src_ports_fp, dst_ports_per_min, dst_ports_fp, prots_per_min, prots_fp, src_s24s_per_min, src_s24s_fp, dst_s24s_per_min, dst_s24s_fp, ip_lens_per_min, ip_lens_fp, ttls_per_min, ttls_fp, pkts_per_min, pkts_per_min_fp, src_ips_per_min, src_ips_fp)        





