import numpy as np
from neuron import neuron
import matplotlib.pyplot as plt
import mel

#constant global parameters which are same for the whole network
global Pref, Pmin, Pth, D, Pspike, time, T, dt
T = 500
dt = 0.125
Pref = 0
Pmin = -1
Pth = 5
D = 1
Pspike = 4
t_ref = 5
time  = np.arange(0, T+dt, dt)

def izh_simulation(a, b, c, d, time_ita, current, v_init):
    # a,b,c,d parameters for Izhikevich model
    # time_ita time iterations for euler method
    # current list of current for each time step
    # v_init initial voltage
    v = v_init
    u = v * b
    v_plt = np.zeros(time_ita)
    u_plt = np.zeros(time_ita)
    spike = np.zeros(time_ita)
    tstep = 0.1 #ms
    ita = 0
    while ita < time_ita:
        v_plt[ita] = v
        u_plt[ita] = u
        v += tstep * (0.04 * (v**2) + 5 * v + 140 - u + current[ita])
        print(current[ita])
        u += tstep * a *(b * v - u)
        if v > 30.:
            spike[ita] = 1
            v = c
            u += d
        ita += 1
    time = np.arange(time_ita) * tstep
    return time, v_plt, spike

def synapse(tau, time, spike):
    synapse_output = np.zeros(len(time))
    for t in range(len(time)):
        tmp_time = time[t] - time[0:t]
        synapse_output[t] = np.sum(((tmp_time*spike[0:t])/tau) * np.exp(-(tmp_time*spike[0:t])/tau))
    return synapse_output

def synapse_func(tau):
    time = np.arange(10000) * 0.1
    func = time/tau * np.exp(-time/tau)
    return time, func



if __name__ == "__main__":

    a = 0.02
    b = 0.2
    c = -65.
    d = 8.
    time_ita = 5000
    tau = 20
    mfcc = mel.test("kss.wav")
    current = np.ones(time_ita) * mfcc[0,11]
    time4, v_plt4, spike4 = izh_simulation(a, b, c, d, time_ita, current, c)
    syn_output = synapse(tau, time4, spike4)
    w = 10.
    syn_current = w * syn_output
    time5, v_plt5, spike5 = izh_simulation(a, b, c, d, time_ita, syn_current, c)

    plt.plot(time4, v_plt4, 'b-')
    plt.plot(time5, v_plt5, 'g-')
    plt.plot(time4, syn_current, 'r-')
    plt.xlabel('time (ms)')
    plt.ylabel('voltage (mV)')
    plt.show()
    #Build our input layer
    # inputLayer = []
    # classifyLayer = []
    # i = 0
    # while i < 13:
    #     inputLayer.append(neuron())
    #
    # i = 0
    # while i < 2:
    #     classifyLayer.append(neuron())
    #
    # mfcc = mel.test("shh.wav")