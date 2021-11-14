# Benchmarking with brian2

```bash
# Build
docker build -t brian2-benchmark .

# Run
docker run -t --rm brian2-benchmark

# To debug
docker run -it --rm brian2-benchmark /bin/bash
```

Brian-2 benchmarks are taken from the [ModelDB record #222725](https://senselab.med.yale.edu/ModelDB/showmodel?model=222725#tabs-1) and associated with the paper [Software for Brain Network Simulations: A Comparative Study](https://www.frontiersin.org/articles/10.3389/fninf.2017.00046/full)

## Hardware platforms
1. Mac mini (Late 2018, Intel i7 3.2 GHz, 64GB RAM)
  - Intel® Core™ i7-8700B
    - 6 cores, 12 threads
    - Base 3.20 GHz, Turbo 4.60 GHz
    - TDP 65W
  - VM, Docker for Mac 3.3.1, configured to 12 Cores 16GB RAM
  - macOS Big Sur 11.2.3
2. MacBook Pro 16" (2020, 64GB RAM)
  - Intel® Core™ i9-9980HK
    - 8 cores, 16 threads
    - Base 2.40 GHz, Turbo 5.00 GHz
    - TDP 45 W
  - VM, Docker for Mac 3.3.1, configured to 16 Cores 16GB RAM
  - macOS Big Sur 11.2.3
3. MacBook Pro 13" M1 (2020, 16GB RAM)
  - M1
    - 8 cores (4 performance, 4 efficient)
    - TDP 10W to 15W (?)
  - VM, Docker for Mac 3.3.1, configured to 8 Cores 10GB RAM, `virtualization.framework`
  - macOS Big Sur 11.2.3
3. MacBook Pro 14" M1 Max 10CPU 32GPU (2021, 64GB RAM)
  - M1 Max
    - 10 cores (8 performance, 2 efficient)
    - CPU TDP ~30W (?)
  - VM, Docker for Mac 4.2.0, configured to 10 Cores 32GB RAM, `virtualization.framework`
  - macOS Monterey 12.0.1
4. Desktop Ryzen 9 3950x (64GB RAM, CPU water cooling)
  - Ryzen 9 3950x
    - 16 cores, 32 threads
    - Base 3.50 GHz, Turbo 4.70 GHz
    - TDP 105W
  - Native, Docker 20.10.6, no limits
  - Ubuntu 21.04
  - Infinity Fabric overclocked to 1800

## Tests
1. 5000 Leaky Integrate-and-File neurons in sparsely connected network.
2. 500 Hodgkin-Huxly neurons with double-exponential synapses, and random connections
## Results

### Single thread performance

Test #1, 10 times: SimpleLarge.py
Task | i7-1165G7 | i7-8700B | i9-9980HK | m1 | m1max | ryzen_9_3950x
:- | -: | -: | -: | -: | -: | -:
Building time<br>Simulation time | `18.80 s`<br>`21.13 s` | `26.21 s`<br>`28.83 s` | `21.83 s`<br>`25.54 s` | `17.17 s`<br>`19.69 s` | `15.75 s`<br>`18.02 s` | `19.45 s`<br>`21.62 s`
Building time<br>Simulation time | `18.46 s`<br>`2.86 s` | `26.18 s`<br>`11.66 s` | `21.92 s`<br>`8.45 s` | `17.18 s`<br>`14.71 s` | `3.46 s`<br>`7.18 s` | `5.04 s`<br>`11.91 s`
Building time<br>Simulation time | `4.09 s`<br>`2.84 s` | `7.04 s`<br>`3.88 s` | `4.75 s`<br>`3.37 s` | `3.56 s`<br>`2.37 s` | `3.49 s`<br>`8.44 s` | `19.56 s`<br>`2.84 s`
Building time<br>Simulation time | `4.22 s`<br>`4.42 s` | `7.06 s`<br>`3.86 s` | `4.70 s`<br>`3.36 s` | `3.51 s`<br>`2.36 s` | `15.78 s`<br>`2.24 s` | `4.99 s`<br>`5.32 s`
Building time<br>Simulation time | `4.23 s`<br>`14.13 s` | `7.10 s`<br>`13.38 s` | `4.68 s`<br>`13.83 s` | `3.54 s`<br>`2.36 s` | `3.48 s`<br>`2.29 s` | `4.98 s`<br>`2.87 s`
Building time<br>Simulation time | `4.12 s`<br>`2.85 s` | `7.12 s`<br>`3.87 s` | `4.72 s`<br>`3.37 s` | `3.58 s`<br>`2.35 s` | `3.47 s`<br>`2.26 s` | `5.02 s`<br>`2.92 s`
Building time<br>Simulation time | `4.75 s`<br>`2.85 s` | `7.03 s`<br>`1.38 s` | `4.75 s`<br>`3.40 s` | `3.51 s`<br>`0.63 s` | `3.45 s`<br>`2.27 s` | `5.05 s`<br>`2.85 s`
Building time<br>Simulation time | `4.13 s`<br>`2.83 s` | `7.10 s`<br>`3.85 s` | `4.62 s`<br>`3.39 s` | `3.53 s`<br>`2.37 s` | `3.46 s`<br>`2.25 s` | `4.89 s`<br>`1.04 s`
Building time<br>Simulation time | `4.13 s`<br>`2.87 s` | `7.04 s`<br>`3.88 s` | `4.67 s`<br>`1.21 s` | `3.48 s`<br>`0.63 s` | `3.51 s`<br>`2.26 s` | `4.84 s`<br>`2.84 s`
Building time<br>Simulation time | `4.65 s`<br>`0.96 s` | `7.04 s`<br>`1.40 s` | `4.76 s`<br>`3.37 s` | `3.49 s`<br>`2.36 s` | `3.49 s`<br>`2.25 s` | `4.78 s`<br>`1.00 s`


Test #2, 10 times: ComplicatedSmall.py
Task | i7-1165G7 | i7-8700B | i9-9980HK | m1 | m1max | ryzen_9_3950x
:- | -: | -: | -: | -: | -: | -:
Building time<br>Simulation time | `3.86 s`<br>`9.01 s` | `5.45 s`<br>`13.19 s` | `4.68 s`<br>`11.70 s` | `3.64 s`<br>`8.54 s` | `3.30 s`<br>`7.83 s` | `4.02 s`<br>`10.11 s`
Building time<br>Simulation time | `0.13 s`<br>`2.85 s` | `5.05 s`<br>`5.43 s` | `4.50 s`<br>`8.95 s` | `3.47 s`<br>`3.15 s` | `0.08 s`<br>`5.30 s` | `3.85 s`<br>`7.87 s`
Building time<br>Simulation time | `3.47 s`<br>`6.24 s` | `0.18 s`<br>`4.43 s` | `0.15 s`<br>`3.77 s` | `0.09 s`<br>`5.74 s` | `0.08 s`<br>`2.97 s` | `0.14 s`<br>`3.51 s`
Building time<br>Simulation time | `0.13 s`<br>`3.66 s` | `0.18 s`<br>`9.13 s` | `0.16 s`<br>`3.82 s` | `0.09 s`<br>`2.40 s` | `0.08 s`<br>`2.28 s` | `0.14 s`<br>`3.56 s`
Building time<br>Simulation time | `0.12 s`<br>`2.85 s` | `0.18 s`<br>`4.43 s` | `0.15 s`<br>`3.80 s` | `0.09 s`<br>`2.38 s` | `0.08 s`<br>`2.29 s` | `0.14 s`<br>`3.45 s`
Building time<br>Simulation time | `0.13 s`<br>`2.77 s` | `0.19 s`<br>`4.43 s` | `0.15 s`<br>`3.77 s` | `0.09 s`<br>`2.39 s` | `3.13 s`<br>`2.23 s` | `0.14 s`<br>`3.49 s`
Building time<br>Simulation time | `0.14 s`<br>`3.21 s` | `0.18 s`<br>`4.44 s` | `0.15 s`<br>`3.82 s` | `0.09 s`<br>`2.39 s` | `0.08 s`<br>`2.28 s` | `0.14 s`<br>`3.53 s`
Building time<br>Simulation time | `0.15 s`<br>`3.13 s` | `0.19 s`<br>`4.47 s` | `0.15 s`<br>`3.76 s` | `0.09 s`<br>`2.39 s` | `0.08 s`<br>`2.28 s` | `0.14 s`<br>`3.56 s`
Building time<br>Simulation time | `0.14 s`<br>`3.09 s` | `0.18 s`<br>`4.40 s` | `0.15 s`<br>`3.82 s` | `0.09 s`<br>`2.41 s` | `0.08 s`<br>`2.27 s` | `0.13 s`<br>`3.45 s`
Building time<br>Simulation time | `0.14 s`<br>`3.07 s` | `0.18 s`<br>`4.44 s` | `0.15 s`<br>`3.72 s` | `0.09 s`<br>`2.39 s` | `0.08 s`<br>`2.29 s` | `0.13 s`<br>`3.48 s`


### Multithread tests in OpenMP standalone mode

Test #1, 10 times : SimpleLarge-omp.py
Task | i7-1165G7 | i7-8700B | i9-9980HK | m1 | m1max | ryzen_9_3950x
:- | -: | -: | -: | -: | -: | -:
Building time<br>Simulation time | `4.11 s`<br>`5.51 s` | `7.05 s`<br>`4.60 s` | `4.75 s`<br>`3.99 s` | `3.43 s`<br>`3.88 s` | `3.37 s`<br>`3.15 s` | `4.94 s`<br>`3.31 s`
Building time<br>Simulation time | `5.10 s`<br>`5.30 s` | `7.03 s`<br>`5.49 s` | `4.68 s`<br>`4.62 s` | `3.46 s`<br>`4.50 s` | `3.46 s`<br>`3.81 s` | `4.70 s`<br>`4.04 s`
Building time<br>Simulation time | `4.16 s`<br>`5.90 s` | `7.06 s`<br>`5.51 s` | `4.72 s`<br>`4.62 s` | `3.58 s`<br>`4.24 s` | `3.41 s`<br>`3.83 s` | `4.86 s`<br>`4.05 s`
Building time<br>Simulation time | `4.58 s`<br>`5.87 s` | `7.04 s`<br>`5.12 s` | `4.58 s`<br>`4.23 s` | `3.47 s`<br>`4.41 s` | `3.40 s`<br>`3.60 s` | `4.93 s`<br>`4.13 s`
Building time<br>Simulation time | `5.66 s`<br>`6.15 s` | `6.99 s`<br>`5.37 s` | `4.64 s`<br>`4.62 s` | `3.46 s`<br>`4.30 s` | `3.44 s`<br>`3.31 s` | `4.70 s`<br>`4.13 s`
Building time<br>Simulation time | `4.87 s`<br>`4.67 s` | `7.04 s`<br>`5.53 s` | `4.74 s`<br>`4.65 s` | `3.47 s`<br>`4.35 s` | `3.41 s`<br>`3.92 s` | `5.01 s`<br>`4.12 s`
Building time<br>Simulation time | `4.71 s`<br>`6.19 s` | `7.01 s`<br>`4.43 s` | `4.59 s`<br>`4.19 s` | `3.47 s`<br>`4.42 s` | `3.43 s`<br>`3.65 s` | `5.01 s`<br>`4.05 s`
Building time<br>Simulation time | `4.84 s`<br>`5.95 s` | `7.07 s`<br>`5.18 s` | `4.57 s`<br>`4.89 s` | `3.47 s`<br>`3.75 s` | `3.42 s`<br>`3.62 s` | `4.91 s`<br>`3.86 s`
Building time<br>Simulation time | `4.58 s`<br>`5.56 s` | `7.00 s`<br>`5.11 s` | `4.69 s`<br>`5.80 s` | `3.58 s`<br>`4.55 s` | `3.49 s`<br>`3.83 s` | `4.75 s`<br>`4.09 s`
Building time<br>Simulation time | `4.49 s`<br>`5.88 s` | `7.08 s`<br>`5.28 s` | `4.67 s`<br>`3.95 s` | `3.45 s`<br>`4.07 s` | `3.43 s`<br>`3.89 s` | `4.98 s`<br>`4.02 s`


Test #2, 10 times: ComplicatedSmall-omp.py
Task | i7-1165G7 | i7-8700B | i9-9980HK | m1 | m1max | ryzen_9_3950x
:- | -: | -: | -: | -: | -: | -:
Building time<br>Simulation time | `0.13 s`<br>`2.71 s` | `0.19 s`<br>`3.70 s` | `0.15 s`<br>`3.06 s` | `0.09 s`<br>`2.36 s` | `0.08 s`<br>`1.91 s` | `0.14 s`<br>`2.45 s`
Building time<br>Simulation time | `0.13 s`<br>`2.65 s` | `0.18 s`<br>`3.79 s` | `0.15 s`<br>`3.42 s` | `0.08 s`<br>`2.30 s` | `0.07 s`<br>`2.08 s` | `0.14 s`<br>`2.75 s`
Building time<br>Simulation time | `0.12 s`<br>`2.55 s` | `0.20 s`<br>`3.78 s` | `0.15 s`<br>`3.18 s` | `0.09 s`<br>`2.36 s` | `0.07 s`<br>`2.06 s` | `0.14 s`<br>`2.75 s`
Building time<br>Simulation time | `0.12 s`<br>`2.66 s` | `0.19 s`<br>`4.05 s` | `0.15 s`<br>`3.05 s` | `0.09 s`<br>`2.27 s` | `0.07 s`<br>`2.15 s` | `0.14 s`<br>`2.77 s`
Building time<br>Simulation time | `0.15 s`<br>`2.98 s` | `0.18 s`<br>`3.67 s` | `0.15 s`<br>`3.15 s` | `0.08 s`<br>`2.34 s` | `0.07 s`<br>`2.04 s` | `0.14 s`<br>`2.76 s`
Building time<br>Simulation time | `0.12 s`<br>`2.44 s` | `0.18 s`<br>`3.72 s` | `0.15 s`<br>`3.04 s` | `0.09 s`<br>`2.34 s` | `0.07 s`<br>`2.08 s` | `0.14 s`<br>`2.76 s`
Building time<br>Simulation time | `0.12 s`<br>`2.63 s` | `0.18 s`<br>`3.80 s` | `0.15 s`<br>`2.99 s` | `0.09 s`<br>`2.37 s` | `0.07 s`<br>`2.07 s` | `0.14 s`<br>`2.75 s`
Building time<br>Simulation time | `0.13 s`<br>`2.68 s` | `0.18 s`<br>`3.75 s` | `0.15 s`<br>`2.96 s` | `0.09 s`<br>`2.27 s` | `0.07 s`<br>`2.01 s` | `0.13 s`<br>`2.73 s`
Building time<br>Simulation time | `0.13 s`<br>`2.59 s` | `0.18 s`<br>`3.84 s` | `0.15 s`<br>`2.93 s` | `0.09 s`<br>`2.29 s` | `0.07 s`<br>`2.08 s` | `0.14 s`<br>`2.71 s`
Building time<br>Simulation time | `0.13 s`<br>`2.64 s` | `0.18 s`<br>`3.74 s` | `0.15 s`<br>`3.11 s` | `0.09 s`<br>`2.31 s` | `0.07 s`<br>`2.17 s` | `0.13 s`<br>`2.69 s`

