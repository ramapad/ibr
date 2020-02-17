
import sys
import shlex, subprocess
import datetime
import dateutil
from dateutil.parser import parse
import getopt
import calendar


if __name__=="__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:h:t:s:e:b:i:p:n:u", ["hourstr=", "hourepoch=", "istimed=", "starttime=", "endtime=", "issubset=", "inputaddrfile=", "fnameprefix=", "numprocs=", "usage="])
        
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(1)

    hourstr = None
    hourepoch = None
    istimed = None
    starttime = None
    endtime = None
    issubset = 0
    inputaddrfile = None
    pfx = None
    suf = None
    numprocs = 1

    for o, a in opts:
        if o in ("-h", "--hourepoch"):
            hourepoch = int(a)
        elif o in ("-s", "--hourstr"):
            hourstr = a
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
        elif o in ("-p", "--fnameprefix"):
            pfx = a
        elif o in ("-n", "--numprocs"):
            numprocs = int(a)
        else:
            assert False, "unhandled option"

    # If the reqd hour has been specified as a string, convert to epoch time
    if hourstr != None:
        # sys.stdout.write("{0}\n".format(hourstr) )        
        hour_struct = dateutil.parser.parse(hourstr)
        hourepoch = int(calendar.timegm(hour_struct.utctimetuple()))

    # sys.stdout.write("{0}\n".format(hourepoch) )
    # sys.exit(1)
    
    this_h_dt = datetime.datetime.utcfromtimestamp(hourepoch)
    reqd_year = this_h_dt.year
    reqd_month = this_h_dt.month
    reqd_day = this_h_dt.day

    if istimed == 0:
        starttime = hourepoch
        endtime = hourepoch + 3600
        
    this_h_dt_str = this_h_dt.strftime("%Y_%m_%d_%H_%M")
    this_dir = './data/{0}/{1}_{2}/'.format(pfx, this_h_dt_str, hourepoch)
    mkdir_cmd = 'mkdir -p {0}'.format(this_dir)
    sys.stderr.write("{0}\n".format(mkdir_cmd) )
    args = shlex.split(mkdir_cmd)
    # print args
    subprocess.call(args)
    
    # os.system("cors2ascii swift://data-telescope-meta-flowtuple/datasource=ucsd-nt/year={0}/month={1}/day={2}/ucsd-nt.{3}.flowtuple.cors.gz | python explore.py --hourepoch {3} --istimed 1 --issubset 1 --inputaddrfile {4} --fnameprefix {5} --fnamesuffix {6}".format(reqd_year, reqd_month, reqd_day, hourepoch, inputaddrfile, pfx, suf) )


    max_secs = endtime - starttime
    binsize = max_secs/numprocs

    proc_num = 0

    if issubset == 0:
        for this_t in range(starttime, endtime, binsize):
            suf = "{0}_to_{1}".format(this_t, this_t + binsize)        
            sys.stdout.write("cors2ascii swift://data-telescope-meta-flowtuple/datasource=ucsd-nt/year={0}/month={1}/day={2}/ucsd-nt.{3}.flowtuple.cors.gz | python explore.py --hourepoch {3} --istimed 1 --starttime {4} --endtime {5} --fnameprefix {6} --fnamesuffix {7} > {8}stdout{9} 2>{8}stderr{9} \n".format(reqd_year, reqd_month, reqd_day, hourepoch, this_t, this_t + binsize, pfx, suf, this_dir, proc_num) )
            proc_num += 1
    else:
        for this_t in range(starttime, endtime, binsize):
            suf = "{0}_to_{1}".format(this_t, this_t + binsize)
            sys.stdout.write("cors2ascii swift://data-telescope-meta-flowtuple/datasource=ucsd-nt/year={0}/month={1}/day={2}/ucsd-nt.{3}.flowtuple.cors.gz | python explore.py --hourepoch {3} --istimed 1 --starttime {4} --endtime {5} --issubset 1 --inputaddrfile {6} --fnameprefix {7} --fnamesuffix {8} > {9}stdout{10} 2>{9}stderr{10} \n".format(reqd_year, reqd_month, reqd_day, hourepoch, this_t, this_t + binsize, inputaddrfile, pfx, suf, this_dir, proc_num) )
            proc_num += 1            
