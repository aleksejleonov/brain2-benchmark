import sys, os, re
from numpy import *
from matplotlib.pyplot import *

def getstat(f):
    NCPUS = -1
    CPUNAME = f.split('/')[1][:-4]
    BUILDTIME = {}
    RUNTIME   = {}
    TESTNMAES = ""
    with open(f) as fd:
        for l in fd.readlines():
            if 'processor' in l:
                cpu = int( l[l.index(':')+1:] )
                if cpu+1 > NCPUS : NCPUS = cpu+1
            elif 'model name' in l:
                CPUNAME = l[l.index(':')+1:-1]
            elif 'Testing 10 times with ' in l:
                TESTNMAES = l[len('Testing 10 times with '):-4]
                if not TESTNMAES in BUILDTIME: BUILDTIME[TESTNMAES] = []
                if not TESTNMAES in RUNTIME  : RUNTIME[TESTNMAES]   = []
            elif "Building time" in l :
                bt = l[l.index(':')+1:]
                bt = bt.split()
                for b in bt:
                    try:
                        BUILDTIME[TESTNMAES].append(float(b))
                        break
                    except:
                        continue
            elif "Simulation time" in l :
                st = l[l.index(':')+1:]
                st = st.split()
                for s in st:
                    try:
                        RUNTIME[TESTNMAES].append(float(s))
                        break
                    except:
                        continue
    return CPUNAME,NCPUS,BUILDTIME,RUNTIME
    
if __name__ == "__main__":
    stats = [ getstat(f) for f in sys.argv[1:] ]
    tests = []
    for _,_,b,r in stats:
        for n in b:
            if not n in tests: tests.append(n)
        for n in r:
            if not n in tests: tests.append(n)
    tests.sort(reverse=True)
    N=len(tests)
    f = figure(figsize=(12,8))
    subplot(1,2,1)
    title("Minimal Build time")
    for n,_,b,_ in stats:
        l = []
        for ti,t in enumerate(tests):
            if not t in b: continue
            l.append([ti, amin(b[t]), mean(b[t])])
        l = array(l)
        semilogy(l[:,0],l[:,1],'o-',label=n)
    legend(loc='best')
    ylabel("time (s)")
    xticks(arange(N), tests, rotation='vertical')
    subplot(1,2,2)
    title("Minimal Simulation time")
    for n,_,_,s in stats:
        l = []
        for ti,t in enumerate(tests):
            if not t in s: continue
            l.append([ti, amin(s[t]), mean(s[t])])
        l = array(l)
        semilogy(l[:,0],l[:,1],'o-',label=n)
    legend(loc='best')
    xticks(arange(N), tests, rotation='vertical')
    subplots_adjust(left=0.08, right=0.99, top=0.95, bottom=0.3)
    savefig("results.svg")
    savefig("results.jpg")
    show()
            
        
    

