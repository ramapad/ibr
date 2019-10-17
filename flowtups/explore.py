
import sys
from collections import defaultdict

line_ct = 0

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

hour_idx_epoch = sys.argv[1]
fp = open('./data/prot_dstport_srcs24_per_minute_{0}'.format(hour_idx_epoch), 'w')
src_ports_fp = open('./data/srcport_per_minute_{0}'.format(hour_idx_epoch), 'w')
dst_ports_fp = open('./data/dstport_per_minute_{0}'.format(hour_idx_epoch), 'w')
prots_fp = open('./data/prot_per_minute_{0}'.format(hour_idx_epoch), 'w')
src_s24s_fp = open('./data/srcs24_per_minute_{0}'.format(hour_idx_epoch), 'w')
dst_s24s_fp = open('./data/dsts24_per_minute_{0}'.format(hour_idx_epoch), 'w')
ip_lens_fp = open('./data/iplens_per_minute_{0}'.format(hour_idx_epoch), 'w')
ttls_fp = open('./data/ttls_per_minute_{0}'.format(hour_idx_epoch), 'w')
src_ips_fp = open('./data/srcips_per_minute_{0}'.format(hour_idx_epoch), 'w')
pkts_per_min_fp = open('./data/pkts_per_minute_{0}'.format(hour_idx_epoch), 'w')

for line in sys.stdin:
    line_ct += 1

    if line_ct%10000000 == 0:
        sys.stdout.write('Line ct: {}\n'.format(line_ct) )

    if line[:24] == '# CORSARO_INTERVAL_START':
        # Flush aggregate stats from the last minute
        # print line

        parts = line.strip().split()
        # Since we are printing stats for the previous minute, we should subtract 1 from this minute_num
        minute_num = int(parts[2]) - 1 

        # for prot in pkts:
        #     for dst_port in pkts[prot]:
        #         for src_s24 in pkts[prot][dst_port]:
        #             this_d = pkts[prot][dst_port][src_s24]
        #             fp.write("{} {} {} {} {} {}\n".format(minute_num, prot, dst_port, src_s24, len(this_d["ips"]), this_d["pkts"]) )

        for prot in pkts:
            for dst_port in pkts[prot]:
                for src_port in pkts[prot][dst_port]:
                    for ip_len in pkts[prot][dst_port][src_port]:
                        this_d = pkts[prot][dst_port][src_port][ip_len]
                        fp.write("{0} {1} {2} {3} {4} {5} {6} {7}\n".format(minute_num, prot, dst_port, src_port, ip_len, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"]) )
                    
        for src_port in src_ports_per_min:
            this_d = src_ports_per_min[src_port]
            src_ports_fp.write("{} {} {} {} {}\n".format(minute_num, src_port, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )
            
        for dst_port in dst_ports_per_min:
            this_d = dst_ports_per_min[dst_port]
            dst_ports_fp.write("{} {} {} {} {}\n".format(minute_num, dst_port, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )
            
        for prot in prots_per_min:
            this_d = prots_per_min[prot]
            prots_fp.write("{} {} {} {} {}\n".format(minute_num, prot, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )
            
        for src_s24 in src_s24s_per_min:
            this_d = src_s24s_per_min[src_s24]
            src_s24s_fp.write("{} {} {} {}\n".format(minute_num, src_s24, len(this_d["ips"]), this_d["pkts"] ) )
            
        for dst_s24 in dst_s24s_per_min:
            this_d = dst_s24s_per_min[dst_s24]
            dst_s24s_fp.write("{} {} {} {}\n".format(minute_num, dst_s24, len(this_d["ips"]), this_d["pkts"] ) )
            
        for ip_len in ip_lens_per_min:
            this_d = ip_lens_per_min[ip_len]
            ip_lens_fp.write("{} {} {} {} {}\n".format(minute_num, ip_len, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )

        for ttl in ttls_per_min:
            this_d = ttls_per_min[ttl]
            ttls_fp.write("{} {} {} {} {}\n".format(minute_num, ttl, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )
            
        pkts_per_min_fp.write("{} {}\n".format(minute_num, pkts_per_min) )
        src_ips_fp.write("{} {}\n".format(minute_num, len(src_ips_per_min) ) )
        
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
        
        # fp.flush()
        # if line_ct > 10000:
        #     sys.exit(1)

    if "|" not in line:
        continue

    parts = line.strip().split('|')
    src_ip = parts[0]
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

    
# Flush last minute    
minute_num += 1 

# for prot in pkts:
#     for dst_port in pkts[prot]:
#         for src_s24 in pkts[prot][dst_port]:
#             this_d = pkts[prot][dst_port][src_s24]
#             fp.write("{} {} {} {} {} {}\n".format(minute_num, prot, dst_port, src_s24, len(this_d["ips"]), this_d["pkts"]) )

for prot in pkts:
    for dst_port in pkts[prot]:
        for src_port in pkts[prot][dst_port]:
            for ip_len in pkts[prot][dst_port][src_port]:
                this_d = pkts[prot][dst_port][src_port][ip_len]
                fp.write("{0} {1} {2} {3} {4} {5} {6} {7}\n".format(minute_num, prot, dst_port, src_port, ip_len, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"]) )

for src_port in src_ports_per_min:
    this_d = src_ports_per_min[src_port]
    src_ports_fp.write("{} {} {} {} {}\n".format(minute_num, src_port, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )

for dst_port in dst_ports_per_min:
    this_d = dst_ports_per_min[dst_port]
    dst_ports_fp.write("{} {} {} {} {}\n".format(minute_num, dst_port, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )

for prot in prots_per_min:
    this_d = prots_per_min[prot]
    prots_fp.write("{} {} {} {} {}\n".format(minute_num, prot, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )

for src_s24 in src_s24s_per_min:
    this_d = src_s24s_per_min[src_s24]
    src_s24s_fp.write("{} {} {} {}\n".format(minute_num, src_s24, len(this_d["ips"]), this_d["pkts"] ) )

for dst_s24 in dst_s24s_per_min:
    this_d = dst_s24s_per_min[dst_s24]
    dst_s24s_fp.write("{} {} {} {}\n".format(minute_num, dst_s24, len(this_d["ips"]), this_d["pkts"] ) )

for ip_len in ip_lens_per_min:
    this_d = ip_lens_per_min[ip_len]
    ip_lens_fp.write("{} {} {} {} {}\n".format(minute_num, ip_len, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )

for ttl in ttls_per_min:
    this_d = ttls_per_min[ttl]
    ttls_fp.write("{} {} {} {} {}\n".format(minute_num, ttl, len(this_d["s24s"]), len(this_d["ips"]), this_d["pkts"] ) )
            
pkts_per_min_fp.write("{} {}\n".format(minute_num, pkts_per_min) )
src_ips_fp.write("{} {}\n".format(minute_num, len(src_ips_per_min) ) )


