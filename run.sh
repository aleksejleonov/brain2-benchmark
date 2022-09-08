#!/bin/bash

# exit when any command fails
set -e

echo "CPU info"
cat /proc/cpuinfo

echo ""
echo "*****************************"
echo "*****************************"
echo "*****************************"
echo ""

echo "Benchmark"
echo ""
cd brian2_benchmark
for benchmark_file in simple_large.py simple_large_omp.py complicated_small.py complicated_small_omp.py
do
  echo "*****************************"
  echo "Testing 10 times with $benchmark_file..."
  echo ""

  for i in {0..9}
  do
    python3 $benchmark_file
    echo ""
  done

  echo "*****************************"
  echo ""
done
