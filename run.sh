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
for benchmark_file in SimpleLarge.py SimpleLarge-omp.py ComplicatedSmall.py ComplicatedSmall-omp.py
do
  echo "*****************************"
  echo "Testing 10 times with $benchmark_file..."
  echo ""

  for i in {0..9}
  do
    poetry run python3 $benchmark_file
    echo ""
  done

  echo "*****************************"
  echo ""
done
