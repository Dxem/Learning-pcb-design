import skrf as rf
from skrf.circuit import Circuit

freq = rf.Frequency(start=2.4, stop=2.4, unit='GHz', npoints=1)
tl_media = rf.media.DefinedGammaZ0(freq, z0=50, gamma=1j*freq.w/rf.constants.c)
C1 = tl_media.capacitor(3.222e-12, name='C1')
C2 = tl_media.capacitor(82.25e-15, name='C2')
C3 = tl_media.capacitor(3.222e-12, name='C3')
L2 = tl_media.inductor(8.893e-9, name='L2')
RL = tl_media.resistor(50, name='RL')
gnd = Circuit.Ground(freq, name='gnd')
port1 = Circuit.Port(freq, name='port1', z0=50)
port2 = Circuit.Port(freq, name='port2', z0=50)