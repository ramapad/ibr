# ibr
Scripts to analyze data collected at the UCSD network telescope

## To explore flow tuple records and find interesting traffic patterns:

Flow tuple records are aggregated per hour. We often need to see traffic variation (in terms of unique source /24s, unique source IPs and packet-counts) across various fields present in the flow tuple records (protocols, source ports, destination ports, ttls, ip lengths etc.).

### explore.py

This script churns through the flow tuple record for an hour and produces files containing statistics-per-minute. Each file contains the number of unique source /24s, unique source IPs, and packet-counts per minute for different values in a flow-tuple record field. For example the prot_per_minute_<> file will list the per-minute values for TCP, UDP, ICMP (and other observed protocols).

#### To explore flow tuple records for all addresses in a specified hour with a single process

The script takes many optional arguments but here is a fairly straightforward way to run it:
cors2ascii swift://data-telescope-meta-flowtuple/datasource=ucsd-nt/year=2019/month=11/day=5/ucsd-nt.1572984000.flowtuple.cors.gz | python explore.py --hourepoch 1572984000 --fnameprefix all

--hourepoch is used in naming conventions for output files. It specifies which hour's flow tuple records we are investigating. 
--fnameprefix is used in naming conventions for output files. It specifies whether we are investigating flow tuple records for all addresses (in which case the adopted convention is 'all') or a specific subset of addresses (such as addresses geolocating to Iran).

Since we will churn through the entire flow tuple record, this script will take around 8 to 10 hours to run, depending upon the hour. There are options to speed things up: see below.

We can then examine the number of unique source IP addresses that sent TCP packets per minute as follows:
awk '{if ($2 == 6) print $1, $4}' ./data/all/2019_11_05_20_00_1572984000/prot_per_minute_1572984000_to_1572987600 | less

If we want to examine the packet count of TCP packets per minute:
awk '{if ($2 == 6) print $1, $5}' ./data/all/2019_11_05_20_00_1572984000/prot_per_minute_1572984000_to_1572987600 | less

If we want to examine the number of unique source /24s that sent packets to destination port 23 per minute:
awk '{if ($2 == 23) print $1, $4}' ./data/all/2019_11_05_20_00_1572984000/dstport_per_minute_1572984000_to_1572987600 | less

#### To explore flow tuple records for a specific subset of addresses in a specified hour

Often, we would want to analyze the flow tuple records for a specific subset of addresses, such as addresses geolocating to Iran, or addresses belonging to Comcast. 

In this case, we would first use geolocation databases and/or pfx2as to place in a file the set of addresses that we are interested in. This file is then passed as an input argument to explore.py

Suppose we have found the list of Iranian addresses and the file is called all_iran_addresses. Then we would run explore.py as follows:

cors2ascii swift://data-telescope-meta-flowtuple/datasource=ucsd-nt/year=2020/month=2/day=15/ucsd-nt.1581757200.flowtuple.cors.gz | python explore.py --hourepoch 1581757200 --issubset 1 --inputaddrfile all_iran_addresses --fnameprefix iran

--issubset 1 indicates to the script that we wish to analyze only a subset of addresses
--inputaddrfile specifies the filename containing the specific subset of addresses we wish to analyze.
