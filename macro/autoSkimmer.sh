mkdir out
for f in ../test/scales/*.root
do
   ln -s $f
   base=`basename $f`
   echo $f $base
   ./skimtree dir Hamb mc $base Mode Opt
    echo "\tOpt done"
    rm -f $base
    mv out/Hamb$base $base
    ./skimtree dir Hamb mc $base Mode mHcut
    rm -f $base
    echo "\tmHcut done"
done
