"""
Single thread performance test for complicated small model.
"""

import time
import numpy as np
from brian2 import (
    ufarad,
    umetre,
    siemens,
    cm,
    mV,
    msiemens,
    ms,
    log,
    exp,
    nS,
    defaultclock,
    run,
    Equations,
    NeuronGroup,
    SpikeMonitor,
    Synapses,
    codegen,
)

codegen.target = "cython"

startbuild = time.time()

# Parameters
area = 20000 * umetre**2
Cm = (1 * ufarad * cm**-2) * area
gl = (5e-5 * siemens * cm**-2) * area

El = -30.3 * mV
EK = -90 * mV
ENa = 50 * mV
g_na = (120 * msiemens * cm**-2) * area
g_kd = (36 * msiemens * cm**-2) * area
VT = -63 * mV

# Time constants
taue = 5 * ms
taui1 = 0.99 * ms
taui2 = 1 * ms
Atp = (taui1 * taui2) / (taui2 - taui1) * log(taui2 / taui1)
Afactor = -exp(-Atp / taui1) + exp(-Atp / taui2)
Afactor = 1.0 / Afactor

# Reversal potentials
Ee = 0 * mV
Ei = -75 * mV
wi = Afactor * 2 * nS  # inhibitory synaptic weight

# The model
eqs = Equations(
    """
dv/dt = (gl*(El-v)+ge*(Ee-v)+gi*(Ei-v)-
         g_na*(m*m*m)*h*(v-ENa)-
         g_kd*(n*n*n*n)*(v-EK))/Cm : volt
dm/dt = alpha_m*(1-m)-beta_m*m : 1
dn/dt = alpha_n*(1-n)-beta_n*n : 1
dh/dt = alpha_h*(1-h)-beta_h*h : 1
dge/dt = -ge*(1./taue) : siemens
gi = gi2-gi1 : siemens
dgi1/dt = -gi1*(1./taui1) : siemens
dgi2/dt = -gi2*(1./taui2) : siemens
alpha_m = 0.32*(mV**-1)*(13*mV-v+VT)/
         (exp((13*mV-v+VT)/(4*mV))-1.)/ms : Hz
beta_m = 0.28*(mV**-1)*(v-VT-40*mV)/
        (exp((v-VT-40*mV)/(5*mV))-1)/ms : Hz
alpha_h = 0.128*exp((17*mV-v+VT)/(18*mV))/ms : Hz
beta_h = 4./(1+exp((40*mV-v+VT)/(5*mV)))/ms : Hz
alpha_n = 0.032*(mV**-1)*(15*mV-v+VT)/
         (exp((15*mV-v+VT)/(5*mV))-1.)/ms : Hz
beta_n = .5*exp((10*mV-v+VT)/(40*mV))/ms : Hz

"""
)
defaultclock.dt = 0.05 * ms
P = NeuronGroup(400, model=eqs, threshold="v>25*mV", method="rk4")

Ci = Synapses(
    P,
    P,
    on_pre="""
        gi1+=wi
        gi2+=wi
    """,
)

conlist = list(np.genfromtxt("connections.ssv").astype(int))
conpairs = [([pre] * len(post), post) for pre, post in enumerate(conlist)]
pre, post = zip(*conpairs)
Ci.connect(i=np.array(pre).flatten(), j=np.array(post).flatten())
Ci.delay = "3.0*ms"

# Initialization
P.v = np.genfromtxt("volt.ssv") * mV
P.m = "alpha_m / ( alpha_m + beta_m )"
P.h = "alpha_h / ( alpha_h + beta_h )"
P.n = "alpha_n / ( alpha_n + beta_n )"
P.gi1 = "0.*nS"
P.gi2 = "0.*nS"

# Record a few traces
s_mon = SpikeMonitor(P)

endbuild = time.time()

run(500 * ms)

endsimulate = time.time()

print(f"Building time     : {(endbuild - startbuild):0.2f} s")
print(f"Simulation time   : {(endsimulate - endbuild):0.2f} s")
print(f"Time step         : {(defaultclock.dt * 1000.0):0.2f} ms")
