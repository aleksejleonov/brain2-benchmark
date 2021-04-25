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
  echo "Testing 5 times with $benchmark_file..."
  echo ""

  for i in {0..4}
  do
    python3 $benchmark_file
    echo ""
  done

  echo "*****************************"
  echo ""
done