#! /bin/sh

#To setup the endvironment:
##curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
##pip3.6 install --user plotly
##pip3.6 install --user pandas
##python3.6 get-pip.py --user

echo "$(dirname "$0")"
cd "$(dirname "$0")"

set +e
source /cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/bz2lib/1.0.6-omkpbe2/etc/profile.d/init.sh;


#instead of source /cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python3/3.6.4/etc/profile.d/init.sh;
#I copied the commands here
test X$GCC_ROOT != X || . /cvmfs/cms.cern.ch//slc6_amd64_gcc700/external/gcc/7.0.0-omkpbe2/etc/profile.d/init.sh
test X$ZLIB_X86_64_ROOT != X || . /cvmfs/cms.cern.ch//slc6_amd64_gcc700/external/zlib-x86_64/1.2.11-omkpbe2/etc/profile.d/init.sh
test X$ZLIB_ROOT != X || . /cvmfs/cms.cern.ch//slc6_amd64_gcc700/external/zlib-x86_64/1.2.11-omkpbe2/etc/profile.d/init.sh
test X$OPENSSL_ROOT != X || . /cvmfs/cms.cern.ch//slc6_amd64_gcc700/external/openssl/1.0.2d-omkpbe2/etc/profile.d/init.sh
test X$BZ2LIB_ROOT != X || . /cvmfs/cms.cern.ch//slc6_amd64_gcc700/external/bz2lib/1.0.6-omkpbe2/etc/profile.d/init.sh
test X$EXPAT_ROOT != X || . /cvmfs/cms.cern.ch//slc6_amd64_gcc700/external/expat/2.1.0-omkpbe2/etc/profile.d/init.sh
test X$DB6_ROOT != X || . /cvmfs/cms.cern.ch//slc6_amd64_gcc700/external/db6/6.0.30-omkpbe2/etc/profile.d/init.sh
test X$GDBM_ROOT != X || . /cvmfs/cms.cern.ch//slc6_amd64_gcc700/external/gdbm/1.10-omkpbe2/etc/profile.d/init.sh
test X$SQLITE_ROOT != X || . /cvmfs/cms.cern.ch//slc6_amd64_gcc700/external/sqlite/3.22.0-omkpbe/etc/profile.d/init.sh
test X$LIBFFI_ROOT != X || . /cvmfs/cms.cern.ch//slc6_amd64_gcc700/external/libffi/3.2.1-omkpbe2/etc/profile.d/init.sh
PYTHON3_ROOT="/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python3/3.6.4"
PYTHON3_VERSION="3.6.4"
PYTHON3_REVISION="1"
PYTHON3_CATEGORY="external"
[ ! -d /cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python3/3.6.4/bin ] || export PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python3/3.6.4/bin${PATH:+:$PATH}";
[ ! -d /cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python3/3.6.4/lib ] || export LD_LIBRARY_PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python3/3.6.4/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}";
[ ! -d /cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python3/3.6.4/bin ] || export PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python3/3.6.4/bin${PATH:+:$PATH}";
[ ! -d /cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python3/3.6.4/lib ] || export LD_LIBRARY_PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python3/3.6.4/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}";
PYTHON_LIB_SITE_PACKAGES="lib/python3.6/site-packages"
PYTHONHASHSEED="random"

OPTIND=1         # Reset in case getopts has been used previously in the shell.

year=0
fill=0
while getopts "f:y:" opt; do
    case "$opt" in
    y)  echo year $OPTARG
	year=$OPTARG
        ;;
    f)  echo fill $OPTARG
	fill=$OPTARG
        ;;
    esac
done

echo $year;
echo $fill;

./IntensityCorrelation.py $@;
rm -f $fill/*txt;
cp index.html $fill/;
mv $fill /eos/home-h/hbakhshi/www/PU;
