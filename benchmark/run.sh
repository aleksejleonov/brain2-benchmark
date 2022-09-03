#!/bin/bash

echo "CPU info"
cat /proc/cpuinfo

echo ""
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo ""

echo "Benchmark"
echo ""
for benchmark_file in $(ls *.py)
do
  echo "*****************************"
  echo "Testing 10 times with $benchmark_file..."
  echo ""

  for i in {0..9}
  do
    rm -fR ${benchmark_file%%.py} ~/.cython
    python3 $benchmark_file
    echo ""
  done

  echo "*****************************"
  echo ""
done