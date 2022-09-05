import time, os
import numpy as np
#import matplotlib
#matplotlib.rcParams["savefig.directory"] = ""
from brian2 import *

set_device('cpp_standalone', directory="SimpleLarge" )
prefs.devices.cpp_standalone.openmp_threads = os.cpu_count()

startbuild=time.time()

Ne,Ni,Ns=4000,1000,500

excw,excd =  0.009, 0.8
inhw,inhd = -0.050, 2.1
stmw,stmd =  0.025, 0.5
inspk = np.genfromtxt("input.ssv")

tau = 10*ms
eqs = '''
dv/dt  = -v/tau : 1 (unless refractory)
'''

defaultclock.dt = 0.1*ms

E =  NeuronGroup(Ne, eqs, threshold='v>1.', reset='v = 0', method='linear', refractory=5.01*ms)
E.v = 0
I =  NeuronGroup(Ni, eqs, threshold='v>1.', reset='v = 0', method='linear', refractory=5.01*ms)
I.v = 0
S = SpikeGeneratorGroup(Ns, inspk[:,1].astype(int), inspk[:,0]*ms)


Cee = Synapses(E, E, on_pre='v_post += excw ')
prepost = np.genfromtxt("ee.ssv").astype(int)
Cee.connect(i=prepost[:,0], j=prepost[:,1])
Cee.delay = excd*ms

Cei = Synapses(E, I, on_pre='v_post += excw ')
prepost = np.genfromtxt("ei.ssv").astype(int)
Cei.connect(i=prepost[:,0], j=prepost[:,1])
Cei.delay = excd*ms

Cie = Synapses(I, E, on_pre='v_post += inhw ')
prepost = np.genfromtxt("ie.ssv").astype(int)
Cie.connect(i=prepost[:,0], j=prepost[:,1])
Cie.delay = inhd*ms

Cii = Synapses(I, I, on_pre='v_post += inhw ')
prepost = np.genfromtxt("ii.ssv").astype(int)
Cii.connect(i=prepost[:,0], j=prepost[:,1])
Cii.delay = inhd*ms

Cse = Synapses(S, E, on_pre='v_post += stmw ')
prepost = np.genfromtxt("se.ssv").astype(int)
Cse.connect(i=prepost[:,0], j=prepost[:,1])
Cse.delay = stmd*ms



e_mon = SpikeMonitor(E)
i_mon = SpikeMonitor(I)
s_mon = SpikeMonitor(S)

endbuild=time.time()

run(1 * second)

endsimulate= time.time()


print("Building time     : %.2f s"%(endbuild-startbuild ))
print("Simulation time   : %.2f s"%(endsimulate-endbuild))
print("Time step         : %.2f ms"%(defaultclock.dt*1000.))

e_mon = dstack( (np.array(e_mon.t/ms),np.array(e_mon.i)) )[0]
i_mon = dstack( (np.array(i_mon.t/ms),np.array(i_mon.i)) )[0]
s_mon = dstack( (np.array(s_mon.t/ms),np.array(s_mon.i)) )[0]

e_mon = e_mon[np.where(e_mon[:,0]<200)]
i_mon = i_mon[np.where(i_mon[:,0]<200)]
s_mon = s_mon[np.where(s_mon[:,0]<200)]

#plot(e_mon[:,0], e_mon[:,1]          , '.k')
#plot(i_mon[:,0], i_mon[:,1]+Ne+100   , '.r')
#plot(s_mon[:,0], s_mon[:,1]+Ne+Ni+200, '.b')

#show()
