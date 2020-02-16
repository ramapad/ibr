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

### Find level shifts

These scripts help us identify the potential cause of a burst. 

For example, consider a traffic burst like the one here for Iranian addresses at 9:02 am on Feb 15 2010:
https://ioda.caida.org/ioda/dashboard#view=inspect&entity=country/IR&lastView=overview&from=1581033600&until=1581206400

We would like to identify which protocols, dst ports, src ports etc. had unusually high traffic during the burst. 

#### find_level_shift_given_hour.py

This script takes as input a per-minute file produced by explore.py, the times at which the burst occurred, and the traffic metric that we wish to investigate (src /24 count, src ip count, pkt count). It identifies which fields from the per-minute file had particularly high traffic (for the specified metric) during the burst by comparing to non-burst minutes (which are considered to be part of the baseline). "Particularly high" is defined as traffic that saw a 20% increase.

Returning to the example above of the burst in traffic for Iranian addresses at 9:02 am on Feb 15 2020, if we wish to investigate which destination ports saw unusually high traffic from many unique source IP addresses during the minutes with the burst, here is the command:
python find_level_shift_given_hour.py ./data/iran/2020_02_15_09_00_1581757200/dstport_per_minute_1581757200_to_1581760800 2 3 3 100
- The first argument is the name of the per-minute input file (which was produced by explore.py). Since we are interested in the destination port, we specify the filename that begins with dstport_*.
- The second argument is the begin_minute of the burst within this hour. We obtain it by eyeballing the IBR time series curve in the dashboard/explorer. In this case, the burst occurred only in the 2nd minute, so the begin_minute is 2.
- The third argument is the end_minute of the burst within this hour (note: this minute is not part of the burst). Again, we obtain it by eyeballing the IODA time series curve. In this case, the burst began and ended in the 2nd minute, and so the end_minute of the burst within the hour is 3.
- The fourth argument is the position of the field in the dstport_* file that we wish to analyze (indexed from 0). The 2nd field is the count of unique source /24s, the 3rd field is the count of unique source ips, and the 4th field is the count of packets. Since we are interested in the unique source ip count (the 3rd field indexed from 0), we specified this argument to be 3
- The fifth argument specifies a minimum threshold that the field should exceed during the baseline minutes. We are likely not interested if the minutes with the burst observed 10 unique source IP addresses compared to a baseline of 2 unique source IP addresses. However, if the minutes with the burst observe 1000 unique source IP addresses compared to a baseline of 200, that's worth finding. In the example above, we specified the baseline to be 100 unique source addresses

##### The output of this script is:
22 908.00 11.46
8728 1615.00 2.35

Interpreting this output: During minute 2, port 22 observed 908 unique source IP addresses compared to an average of 11.46 unique source IP addresses during all the other minutes (which are considered to be baseline). Port 8728 observed 1615 unique source addresses compared to an average of 2.35 during baseline minutes.
