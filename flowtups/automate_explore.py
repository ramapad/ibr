
import sys
import shlex, subprocess
import datetime
import getopt


if __name__=="__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:t:s:e:b:i:p:n:u", ["hourepoch=", "istimed=", "starttime=", "endtime=", "issubset=", "inputaddrfile=", "prefix=", "numprocs=", "usage="])
        
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(1)

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
        elif o in ("-n", "--numprocs"):
            numprocs = int(a)
        else:
            assert False, "unhandled option"
    
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
    
    # os.system("cors2ascii swift://data-telescope-meta-flowtuple/datasource=ucsd-nt/year={0}/month={1}/day={2}/ucsd-nt.{3}.flowtuple.cors.gz | python explore.py --hourepoch {3} --istimed 1 --issubset 1 --inputaddrfile {4} --prefix {5} --suffix {6}".format(reqd_year, reqd_month, reqd_day, hourepoch, inputaddrfile, pfx, suf) )


    max_secs = endtime - starttime
    binsize = max_secs/numprocs

    proc_num = 0

    if issubset == 0:
        for this_t in range(starttime, endtime, binsize):
            suf = "{0}_to_{1}".format(this_t, this_t + binsize)        
            sys.stdout.write("cors2ascii swift://data-telescope-meta-flowtuple/datasource=ucsd-nt/year={0}/month={1}/day={2}/ucsd-nt.{3}.flowtuple.cors.gz | python explore.py --hourepoch {3} --istimed 1 --starttime {4} --endtime {5} --prefix {6} --suffix {7} > {8}stdout{9} 2>{8}stderr{9} \n".format(reqd_year, reqd_month, reqd_day, hourepoch, this_t, this_t + binsize, pfx, suf, this_dir, proc_num) )
            proc_num += 1
    else:
        for this_t in range(starttime, endtime, binsize):
            suf = "{0}_to_{1}".format(this_t, this_t + binsize)
            sys.stdout.write("cors2ascii swift://data-telescope-meta-flowtuple/datasource=ucsd-nt/year={0}/month={1}/day={2}/ucsd-nt.{3}.flowtuple.cors.gz | python explore.py --hourepoch {3} --istimed 1 --starttime {4} --endtime {5} --issubset 1 --inputaddrfile {6} --prefix {7} --suffix {8} > {9}stdout{10} 2>{9}stderr{10} \n".format(reqd_year, reqd_month, reqd_day, hourepoch, this_t, this_t + binsize, inputaddrfile, pfx, suf, this_dir, proc_num) )
            proc_num += 1            
