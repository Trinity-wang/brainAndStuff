import numpy as np
from Izhikevic import IzhikevichModularNetwork, RewireModularNetwork, CropMatrix, ConnectIzhikevichNetworkLayers
import matplotlib.pyplot as plt

NUM_NEURONS = 1000
NUM_MODULES = 8
NUM_EXCITORY = 800
NUM_EXCITORY_PER_MODULE = 100
NUM_INHIBITORY = 200
NUM_CONNECTIONS_E_to_E = 1000
NUM_CONNECTIONS_E_to_I = 4

T  = 1000  # Simulation time
Ib = 15    # Base current
p = 0.5

CIJ = IzhikevichModularNetwork(NUM_NEURONS, NUM_MODULES, NUM_EXCITORY_PER_MODULE, NUM_CONNECTIONS_E_to_E, NUM_INHIBITORY)
CIJ = RewireModularNetwork(CIJ, NUM_EXCITORY, NUM_EXCITORY_PER_MODULE, p)
plt.matshow(CropMatrix(CIJ, 0, NUM_NEURONS, 0, NUM_NEURONS), cmap=plt.cm.gray)
plt.show()

net = ConnectIzhikevichNetworkLayers(CIJ, NUM_EXCITORY, NUM_INHIBITORY)

## Initialise layers
for lr in xrange(len(net.layer)):
    net.layer[lr].v = -65 * np.ones(net.layer[lr].N)
    net.layer[lr].u = net.layer[lr].b * net.layer[lr].v
    net.layer[lr].firings = np.array([])

v1 = np.zeros([T, NUM_EXCITORY])
v2 = np.zeros([T, NUM_INHIBITORY])
u1 = np.zeros([T, NUM_EXCITORY])
u2 = np.zeros([T, NUM_INHIBITORY])

## SIMULATE
for t in xrange(T):

    net.layer[0].I = np.zeros(NUM_EXCITORY)
    net.layer[1].I = np.zeros(NUM_INHIBITORY)
    
    # Background firing
    for i in range(NUM_EXCITORY):
        if np.random.poisson(0.1) > 0:
            net.layer[0].I[i] = Ib
        
    for i in range(NUM_INHIBITORY):
        if np.random.poisson(0.1) > 0:
            net.layer[1].I[i] = Ib
            
    net.Update(t)

    v1[t] = net.layer[0].v
    v2[t] = net.layer[1].v
    u1[t] = net.layer[0].u
    u2[t] = net.layer[1].u

## Retrieve firings and add Dirac pulses for presentation
firings1 = net.layer[0].firings
firings2 = net.layer[1].firings

if firings1.size != 0:
    v1[firings1[:, 0], firings1[:, 1]] = 30

if firings2.size != 0:
    v2[firings2[:, 0], firings2[:, 1]] = 30


## Plot membrane potentials
plt.figure(1)
plt.subplot(211)
plt.plot(range(T), v1)
plt.title('Population 1 membrane potentials')
plt.ylabel('Voltage (mV)')
plt.ylim([-90, 40])

plt.subplot(212)
plt.plot(range(T), v2)
plt.title('Population 2 membrane potentials')
plt.ylabel('Voltage (mV)')
plt.ylim([-90, 40])
plt.xlabel('Time (ms)')

## Plot recovery variable
plt.figure(2)
plt.subplot(211)
plt.plot(range(T), u1)
plt.title('Population 1 recovery variables')
plt.ylabel('Voltage (mV)')

plt.subplot(212)
plt.plot(range(T), u2)
plt.title('Population 2 recovery variables')
plt.ylabel('Voltage (mV)')
plt.xlabel('Time (ms)')

## Raster plots of firings
if firings1.size != 0:
    plt.figure(3)
    plt.subplot(211)
    plt.scatter(firings1[:, 0], firings1[:, 1] + 1, marker='.')
    plt.xlim(0, T)
    plt.ylabel('Neuron number')
    plt.ylim(0, NUM_EXCITORY+1)
    plt.title('Population 1 firings')

if firings2.size != 0:
    plt.subplot(212)
    plt.scatter(firings2[:, 0], firings2[:, 1] + 1, marker='.')
    plt.xlim(0, T)
    plt.ylabel('Neuron number')
    plt.ylim(0, NUM_INHIBITORY+1)
    plt.xlabel('Time (ms)')
    plt.title('Population 2 firings')

plt.show()
