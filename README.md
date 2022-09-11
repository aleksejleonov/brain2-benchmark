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

1. MacBook Pro 14" M1 Max 10CPU 32GPU (2021, 64GB RAM)
  - M1 Max
    - 10 cores (8 performance, 2 efficient)
    - CPU TDP ~30W
  - VM, Docker for Mac 4.12.0, configured to 10 Cores, 16GB RAM, `virtualization.framework`
  - macOS Monterey 12.5.1
2. MacBook Air M2 8CPU 10GPU (2022, 24GB RAM)
  - M2
    - 8 cores (4 performance, 4 efficient)
    - CPU TDP ~15W, passive cooling
  - VM, Docker for Mac 4.12.0, configured to 8 Cores, 8GB RAM, `virtualization.framework`
  - macOS Monterey 12.5.1
3.  FrameWork i7-1165G7 (2021, 64GB RAM)
  - 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz
    - 4 cores / 8 threads
    - CPU TDP Turbo 60W
  - Docker version 20.10.14, build a224086
  - Pop!_OS 22.04 LTS

## Tests

1. 5000 Leaky Integrate-and-File neurons in a sparsely connected network.
2. 500 Hodgkin-Huxly neurons with double-exponential synapses and random connections

## Results

### Single thread performance

Test #1, 10 times: simple_large.py
Task | i7-1165G7 | m1_max | m2
:- | -: | -: | -:
Building time<br>Simulation time | `19.72 s`<br>`25.52 s` | `17.42 s`<br>`22.58 s` | `15.82 s`<br>`20.49 s`
Building time<br>Simulation time | `19.94 s`<br>`26.18 s` | `17.38 s`<br>`22.56 s` | `15.86 s`<br>`20.48 s`
Building time<br>Simulation time | `22.16 s`<br>`28.13 s` | `17.42 s`<br>`22.60 s` | `15.81 s`<br>`20.44 s`
Building time<br>Simulation time | `22.01 s`<br>`27.94 s` | `17.43 s`<br>`22.59 s` | `15.86 s`<br>`20.48 s`
Building time<br>Simulation time | `21.96 s`<br>`27.96 s` | `17.49 s`<br>`22.62 s` | `15.84 s`<br>`20.46 s`
Building time<br>Simulation time | `21.94 s`<br>`27.92 s` | `17.53 s`<br>`22.67 s` | `15.84 s`<br>`20.52 s`
Building time<br>Simulation time | `22.04 s`<br>`27.93 s` | `17.56 s`<br>`22.71 s` | `15.80 s`<br>`20.42 s`
Building time<br>Simulation time | `22.03 s`<br>`27.87 s` | `17.59 s`<br>`23.07 s` | `15.89 s`<br>`20.58 s`
Building time<br>Simulation time | `22.01 s`<br>`27.89 s` | `17.80 s`<br>`23.17 s` | `15.85 s`<br>`20.55 s`
Building time<br>Simulation time | `22.00 s`<br>`27.90 s` | `17.78 s`<br>`22.87 s` | `15.86 s`<br>`20.53 s`

Test #2, 10 times: complicated_small.py
Task | i7-1165G7 | m1_max | m2
:- | -: | -: | -:
Building time<br>Simulation time | `4.62 s`<br>`10.32 s` | `3.30 s`<br>`8.36 s` | `2.95 s`<br>`7.53 s`
Building time<br>Simulation time | `4.04 s`<br>`10.45 s` | `3.30 s`<br>`8.36 s` | `2.95 s`<br>`7.51 s`
Building time<br>Simulation time | `4.04 s`<br>`10.48 s` | `3.30 s`<br>`8.36 s` | `2.97 s`<br>`7.63 s`
Building time<br>Simulation time | `4.03 s`<br>`10.50 s` | `3.30 s`<br>`8.34 s` | `2.97 s`<br>`7.53 s`
Building time<br>Simulation time | `4.04 s`<br>`10.53 s` | `3.27 s`<br>`8.33 s` | `2.96 s`<br>`7.60 s`
Building time<br>Simulation time | `4.04 s`<br>`10.51 s` | `3.29 s`<br>`8.33 s` | `2.96 s`<br>`7.53 s`
Building time<br>Simulation time | `4.02 s`<br>`10.53 s` | `3.26 s`<br>`8.33 s` | `2.97 s`<br>`7.55 s`
Building time<br>Simulation time | `4.04 s`<br>`10.54 s` | `3.26 s`<br>`8.31 s` | `2.96 s`<br>`7.54 s`
Building time<br>Simulation time | `4.03 s`<br>`10.56 s` | `3.28 s`<br>`8.26 s` | `2.96 s`<br>`7.53 s`
Building time<br>Simulation time | `4.05 s`<br>`10.51 s` | `3.25 s`<br>`8.30 s` | `2.96 s`<br>`7.54 s`

### Multithread tests in OpenMP standalone mode

Test #1, 10 times : simple_large_omp.py
Task | i7-1165G7 | m1_max | m2
:- | -: | -: | -:
Building time<br>Simulation time | `3.58 s`<br>`5.99 s` | `2.58 s`<br>`3.27 s` | `2.27 s`<br>`3.53 s`
Building time<br>Simulation time | `4.42 s`<br>`5.96 s` | `2.55 s`<br>`3.38 s` | `2.26 s`<br>`3.25 s`
Building time<br>Simulation time | `4.17 s`<br>`5.90 s` | `2.56 s`<br>`3.49 s` | `2.25 s`<br>`3.37 s`
Building time<br>Simulation time | `4.18 s`<br>`5.97 s` | `2.57 s`<br>`3.34 s` | `2.31 s`<br>`3.24 s`
Building time<br>Simulation time | `4.15 s`<br>`6.09 s` | `2.54 s`<br>`3.29 s` | `2.26 s`<br>`3.35 s`
Building time<br>Simulation time | `4.07 s`<br>`5.93 s` | `2.56 s`<br>`3.30 s` | `2.30 s`<br>`3.46 s`
Building time<br>Simulation time | `4.22 s`<br>`5.98 s` | `2.57 s`<br>`3.26 s` | `2.25 s`<br>`3.30 s`
Building time<br>Simulation time | `4.14 s`<br>`5.99 s` | `2.57 s`<br>`3.32 s` | `2.27 s`<br>`3.25 s`
Building time<br>Simulation time | `4.14 s`<br>`6.04 s` | `2.57 s`<br>`3.29 s` | `2.27 s`<br>`3.34 s`
Building time<br>Simulation time | `4.12 s`<br>`5.96 s` | `2.55 s`<br>`3.39 s` | `2.27 s`<br>`3.25 s`

Test #2, 10 times: complicated_small_omp.py
Task | i7-1165G7 | m1_max | m2
:- | -: | -: | -:
Building time<br>Simulation time | `0.12 s`<br>`3.41 s` | `0.08 s`<br>`1.84 s` | `0.07 s`<br>`1.88 s`
Building time<br>Simulation time | `0.17 s`<br>`3.65 s` | `0.08 s`<br>`1.91 s` | `0.07 s`<br>`1.89 s`
Building time<br>Simulation time | `0.17 s`<br>`3.65 s` | `0.08 s`<br>`1.87 s` | `0.07 s`<br>`1.88 s`
Building time<br>Simulation time | `0.17 s`<br>`3.58 s` | `0.08 s`<br>`1.86 s` | `0.07 s`<br>`1.85 s`
Building time<br>Simulation time | `0.17 s`<br>`3.56 s` | `0.08 s`<br>`1.88 s` | `0.07 s`<br>`1.84 s`
Building time<br>Simulation time | `0.17 s`<br>`3.55 s` | `0.08 s`<br>`1.88 s` | `0.07 s`<br>`1.88 s`
Building time<br>Simulation time | `0.17 s`<br>`3.59 s` | `0.08 s`<br>`1.87 s` | `0.07 s`<br>`1.85 s`
Building time<br>Simulation time | `0.17 s`<br>`3.54 s` | `0.08 s`<br>`1.91 s` | `0.07 s`<br>`1.88 s`
Building time<br>Simulation time | `0.17 s`<br>`3.55 s` | `0.08 s`<br>`1.85 s` | `0.07 s`<br>`1.85 s`
Building time<br>Simulation time | `0.18 s`<br>`3.60 s` | `0.08 s`<br>`1.89 s` | `0.07 s`<br>`1.85 s`
