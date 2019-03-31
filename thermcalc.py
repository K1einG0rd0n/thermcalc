import numpy as np
import scipy as sp
from scipy import constants
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from scipy.integrate import simps
import SchemDraw as schem
import SchemDraw.elements as e



pi = constants.pi
h = constants.h
kb = constants.k


class Port:
    def __init__(self, part):
        self.part = part
        self.connect_to = []

    def connect(self, port):
        self.connect_to = port
        port.__connect_back(self)

    def __connect_back(self, port):
        self.connect_to = port


class Part:
    def __init__(self, num_ports):
        self.num_ports = num_ports
        self.port = []
        for i in range(0, num_ports):
            self.port.append(Port(self))


class ThermSource(Part):
    def __init__(self, temp):
        Part.__init__(self, 1)
        self.temp = temp


class Attenuator(Part):
    def __init__(self, atten, temp):
        Part.__init__(self, 2)
        self.atten = atten
        self.temp = temp

    def gain(self):
        return gain(-self.atten)

    def loss(self):
        return gain(self.atten)

    def spec_prop(self, spec_in):
        spec_out = PowerSpec()
        spec_out.freq = spec_in.freq
        spec_out.power = self.gain() * spec_in.power + (1 - self.gain()) * therm_noise(self.temp).power
        return spec_out


class SpecAnalyzer(Part):
    def __init__(self):
        Part.__init__(self, 1)


class PowerSpec:
    logf = np.arange(0, 14, 0.01)
    freq = np.power(10, logf)

    def __init__(self):
        self.power = []
        self.bandwidth = 1

    def dbm(self, bandwidth=1):
        dbm_val = 10 * (np.log10(self.power/0.001) + np.log10(bandwidth))
        return dbm_val

    def dbm_plot(self, bandwidth=1):
        fig = figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
        ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])
        plt.plot(self.freq * 1E-9, self.dbm(bandwidth))
        plt.xlim(0, 20)
        plt.xlabel('Freq (GHz)')
        plt.ylabel('Noise power (dBm)')
        plt.show()

    def total_power(self):
        return simps(self.power, self.freq)

    def total_power_dbm(self):
        return dbm(self.total_power())


def evaluate(source):
    N = therm_noise(source.temp)
    part = source.port[0].connect_to.part
    while part.num_ports != 1:
        N = part.spec_prop(N)
        part = part.port[1].connect_to.part
    return N


def draw(source):
    fig = figure(num=None, figsize=(8, 8), dpi=80, facecolor='w', edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    plt.axis('equal')
    plt.hlines(0, 0, 6, linestyles='--', colors='r')

    d = schem.Drawing()
    d.add(e.DOT_OPEN, xy=[3, 1], rgtlabel=str(source.temp)+' K')
    d.add(e.LINE, d='down', toy=0)
    d.add(e.DOT)

    part = source.port[0].connect_to.part
    while part.num_ports != 1:
        d.add(e.RBOX, d='down', botlabel=str(part.atten)+' dB\n'+str(part.temp)+' K')
        part = part.port[1].connect_to.part
    d.add(e.LINE, d='down', l=1)
    d.add(e.DOT_OPEN, botlabel='Spectrum Analyzer')
    d.draw(ax=ax)


def therm_noise(temp):
    f_temp_cutoff = 1E13
    noise = PowerSpec()
    f_temp = np.minimum(noise.freq/temp, f_temp_cutoff)
    noise.power = (h * noise.freq) / np.expm1(h * f_temp / kb)
    return noise


def dbm(power):
    dbm_val = 10 * np.log10(power/0.001)
    return dbm_val


def gain(db):
    gain_val = np.power(10, db / 10)
    return gain_val


def helloworld():
    print("Hello world!")

