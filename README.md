# Benchmarking with brian2

```bash
# Build
docker build -t brian2-benchmark .

# Run
docker run -t --rm brian2-benchmark

# To debug
docker run -it --rm brian2-benchmark /bin/bash

# Get results on first machine
docker run -t --rm brian2-benchmark > results/cpu1.txt
# Get results on second machine
docker run -t --rm brian2-benchmark > results/cpu2.txt
# ...
# Format results in Markdown
ruby format_results.rb results/*
```

Brian-2 benchmarks are taken from the [ModelDB record #222725](https://senselab.med.yale.edu/ModelDB/showmodel?model=222725#tabs-1) and associated with the paper [Software for Brain Network Simulations: A Comparative Study](https://www.frontiersin.org/articles/10.3389/fninf.2017.00046/full)

## Hardware platforms

1. MacBook Pro 13" M1 (2020, 16GB RAM)
  - M1
    - 8 cores (4 performance, 4 efficient)
    - CPU TDP 15W (?)
  - VM, Docker for Mac 4.12.0, configured to 8 Cores, 8GB RAM, `virtualization.framework`
  - macOS Monterey 12.5.1
2. MacBook Pro 14" M1 Max 10CPU 32GPU (2021, 64GB RAM)
  - M1 Max
    - 10 cores (8 performance, 2 efficient)
    - CPU TDP ~30W (?)
  - VM, Docker for Mac 4.12.0, configured to 10 Cores, 16GB RAM, `virtualization.framework`
  - macOS Monterey 12.5.1
3. MacBook Air M2 8CPU 10GPU (2022, 24GB RAM)
  - M2
    - 8 cores (4 performance, 4 efficient)
    - CPU TDP 15W (?), passive cooling
  - VM, Docker for Mac 4.12.0, configured to 8 Cores, 8GB RAM, `virtualization.framework`
  - macOS Monterey 12.5.1

## Tests

1. 5000 Leaky Integrate-and-File neurons in a sparsely connected network.
2. 500 Hodgkin-Huxly neurons with double-exponential synapses and random connections

## Results

### Single thread performance

Test #1, 10 times: SimpleLarge.py
Task | m1 | m1_max | m2
:- | -: | -: | -:
Building time<br>Simulation time | `16.00 s`<br>`20.17 s` | `15.72 s`<br>`19.85 s` | `13.56 s`<br>`17.34 s`
Building time<br>Simulation time | `3.45 s`<br>`0.71 s` | `3.16 s`<br>`0.71 s` | `2.50 s`<br>`0.56 s`
Building time<br>Simulation time | `3.14 s`<br>`0.70 s` | `3.16 s`<br>`0.71 s` | `2.44 s`<br>`0.56 s`
Building time<br>Simulation time | `3.23 s`<br>`0.73 s` | `3.13 s`<br>`0.70 s` | `2.54 s`<br>`0.57 s`
Building time<br>Simulation time | `3.15 s`<br>`0.72 s` | `3.11 s`<br>`0.71 s` | `2.55 s`<br>`0.56 s`
Building time<br>Simulation time | `3.15 s`<br>`0.73 s` | `3.17 s`<br>`0.70 s` | `2.47 s`<br>`0.55 s`
Building time<br>Simulation time | `3.15 s`<br>`0.72 s` | `3.18 s`<br>`0.70 s` | `2.55 s`<br>`0.56 s`
Building time<br>Simulation time | `3.16 s`<br>`0.72 s` | `3.18 s`<br>`0.69 s` | `2.55 s`<br>`0.56 s`
Building time<br>Simulation time | `3.14 s`<br>`0.74 s` | `3.14 s`<br>`0.71 s` | `2.56 s`<br>`0.56 s`
Building time<br>Simulation time | `3.14 s`<br>`0.73 s` | `3.15 s`<br>`0.70 s` | `2.55 s`<br>`0.56 s`


Test #2, 10 times: ComplicatedSmall.py
Task | m1 | m1_max | m2
:- | -: | -: | -:
Building time<br>Simulation time | `3.53 s`<br>`8.68 s` | `3.47 s`<br>`8.61 s` | `3.06 s`<br>`7.56 s`
Building time<br>Simulation time | `0.15 s`<br>`1.02 s` | `0.15 s`<br>`1.01 s` | `0.13 s`<br>`0.89 s`
Building time<br>Simulation time | `0.15 s`<br>`1.01 s` | `0.15 s`<br>`1.01 s` | `0.13 s`<br>`0.90 s`
Building time<br>Simulation time | `0.15 s`<br>`1.01 s` | `0.15 s`<br>`1.01 s` | `0.13 s`<br>`0.90 s`
Building time<br>Simulation time | `0.15 s`<br>`1.02 s` | `0.15 s`<br>`1.01 s` | `0.13 s`<br>`0.90 s`
Building time<br>Simulation time | `0.15 s`<br>`1.02 s` | `0.15 s`<br>`1.02 s` | `0.13 s`<br>`0.89 s`
Building time<br>Simulation time | `0.15 s`<br>`1.01 s` | `0.15 s`<br>`1.01 s` | `0.13 s`<br>`0.89 s`
Building time<br>Simulation time | `0.15 s`<br>`1.00 s` | `0.15 s`<br>`1.02 s` | `0.13 s`<br>`0.90 s`
Building time<br>Simulation time | `0.15 s`<br>`1.00 s` | `0.15 s`<br>`1.00 s` | `0.13 s`<br>`0.89 s`
Building time<br>Simulation time | `0.15 s`<br>`1.01 s` | `0.15 s`<br>`1.01 s` | `0.13 s`<br>`0.90 s`

### Multithread tests in OpenMP standalone mode

Test #1, 10 times : SimpleLarge-omp.py
Task | m1 | m1_max | m2
:- | -: | -: | -:
Building time<br>Simulation time | `3.04 s`<br>`4.29 s` | `3.06 s`<br>`3.44 s` | `2.45 s`<br>`3.57 s`
Building time<br>Simulation time | `3.10 s`<br>`1.09 s` | `3.02 s`<br>`1.25 s` | `2.47 s`<br>`1.10 s`
Building time<br>Simulation time | `3.06 s`<br>`1.12 s` | `3.05 s`<br>`1.27 s` | `2.43 s`<br>`1.01 s`
Building time<br>Simulation time | `3.16 s`<br>`2.47 s` | `3.09 s`<br>`1.27 s` | `2.45 s`<br>`1.02 s`
Building time<br>Simulation time | `3.07 s`<br>`1.16 s` | `3.09 s`<br>`1.28 s` | `2.46 s`<br>`1.04 s`
Building time<br>Simulation time | `3.07 s`<br>`1.11 s` | `3.07 s`<br>`1.25 s` | `2.46 s`<br>`1.00 s`
Building time<br>Simulation time | `3.10 s`<br>`1.09 s` | `3.06 s`<br>`1.27 s` | `2.35 s`<br>`0.96 s`
Building time<br>Simulation time | `3.09 s`<br>`1.09 s` | `3.06 s`<br>`1.24 s` | `2.46 s`<br>`0.97 s`
Building time<br>Simulation time | `3.06 s`<br>`1.12 s` | `3.06 s`<br>`1.28 s` | `2.45 s`<br>`0.98 s`
Building time<br>Simulation time | `3.08 s`<br>`1.12 s` | `3.08 s`<br>`1.32 s` | `2.41 s`<br>`0.98 s`


Test #2, 10 times: ComplicatedSmall-omp.py
Task | m1 | m1_max | m2
:- | -: | -: | -:
Building time<br>Simulation time | `0.08 s`<br>`2.39 s` | `0.08 s`<br>`1.92 s` | `0.08 s`<br>`1.93 s`
Building time<br>Simulation time | `0.08 s`<br>`0.93 s` | `0.08 s`<br>`0.91 s` | `0.07 s`<br>`0.80 s`
Building time<br>Simulation time | `0.08 s`<br>`0.92 s` | `0.08 s`<br>`0.92 s` | `0.07 s`<br>`0.94 s`
Building time<br>Simulation time | `0.08 s`<br>`0.93 s` | `0.08 s`<br>`0.92 s` | `0.07 s`<br>`0.78 s`
Building time<br>Simulation time | `0.08 s`<br>`0.93 s` | `0.08 s`<br>`0.92 s` | `0.07 s`<br>`0.84 s`
Building time<br>Simulation time | `0.08 s`<br>`0.94 s` | `0.08 s`<br>`0.93 s` | `0.07 s`<br>`0.79 s`
Building time<br>Simulation time | `0.08 s`<br>`0.90 s` | `0.08 s`<br>`0.93 s` | `0.07 s`<br>`0.83 s`
Building time<br>Simulation time | `0.08 s`<br>`0.91 s` | `0.08 s`<br>`0.93 s` | `0.08 s`<br>`0.80 s`
Building time<br>Simulation time | `0.08 s`<br>`0.93 s` | `0.08 s`<br>`0.93 s` | `0.07 s`<br>`0.82 s`
Building time<br>Simulation time | `0.08 s`<br>`0.93 s` | `0.08 s`<br>`0.93 s` | `0.07 s`<br>`0.79 s`
