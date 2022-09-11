"""
Multithread tests in OpenMP standalone mode test for simple large model.
"""

import time
import os
import sys
import numpy as np

from brian2 import (
    ms,
    second,
    defaultclock,
    prefs,
    set_device,
    run,
    NeuronGroup,
    SpikeGeneratorGroup,
    SpikeMonitor,
    Synapses,
    device,
)

set_device("cpp_standalone", directory=sys.argv[0][:-3])
prefs.devices.cpp_standalone.openmp_threads = os.cpu_count()

startbuild = time.time()

Ne, Ni, Ns = 4000, 1000, 500

excw, excd = 0.009, 0.8
inhw, inhd = -0.050, 2.1
stmw, stmd = 0.025, 0.5
inspk = np.genfromtxt("input.ssv")

tau = 10 * ms
EQS = """
dv/dt  = -v/tau : 1 (unless refractory)
"""

defaultclock.dt = 0.1 * ms

E = NeuronGroup(
    Ne, EQS, threshold="v>1.", reset="v = 0", method="linear", refractory=5.01 * ms
)
E.v = 0
I = NeuronGroup(
    Ni, EQS, threshold="v>1.", reset="v = 0", method="linear", refractory=5.01 * ms
)
I.v = 0
S = SpikeGeneratorGroup(Ns, inspk[:, 1].astype(int), inspk[:, 0] * ms)


Cee = Synapses(E, E, on_pre="v_post += excw ")
prepost = np.genfromtxt("ee.ssv").astype(int)
Cee.connect(i=prepost[:, 0], j=prepost[:, 1])
Cee.delay = excd * ms

Cei = Synapses(E, I, on_pre="v_post += excw ")
prepost = np.genfromtxt("ei.ssv").astype(int)
Cei.connect(i=prepost[:, 0], j=prepost[:, 1])
Cei.delay = excd * ms

Cie = Synapses(I, E, on_pre="v_post += inhw ")
prepost = np.genfromtxt("ie.ssv").astype(int)
Cie.connect(i=prepost[:, 0], j=prepost[:, 1])
Cie.delay = inhd * ms

Cii = Synapses(I, I, on_pre="v_post += inhw ")
prepost = np.genfromtxt("ii.ssv").astype(int)
Cii.connect(i=prepost[:, 0], j=prepost[:, 1])
Cii.delay = inhd * ms

Cse = Synapses(S, E, on_pre="v_post += stmw ")
prepost = np.genfromtxt("se.ssv").astype(int)
Cse.connect(i=prepost[:, 0], j=prepost[:, 1])
Cse.delay = stmd * ms


e_mon = SpikeMonitor(E)
i_mon = SpikeMonitor(I)
s_mon = SpikeMonitor(S)

endbuild = time.time()

run(1 * second)

endsimulate = time.time()

print(f"Building time     : {(endbuild - startbuild):0.2f} s")
print(f"Simulation time   : {(endsimulate - endbuild):0.2f} s")
print(f"Time step         : {(defaultclock.dt * 1000.0):0.2f} ms")

device.delete(force=True)
