import numpy as np


class Species(object):
    def __init__(self, q, m, N):
        self.q = q
        self.m = m
        self.N = int(N)
        self.x = np.zeros(N, dtype=float)
        self.v = np.zeros(N, dtype=float)

    def leapfrog_init(self, electric_field_function, dt):
        """Leapfrog pusher initialization
        dt: usual timestep, minus halving is done automatically"""

        electric_force = electric_field_function(self.x) * self.q / self.m
        v_new = self.v - electric_force * 0.5 * dt
        energy = self.v * v_new / (2 * self.m)
        self.v = v_new
        return energy

    def push_particles(self, electric_field_function, dt, L):
        """Leapfrog pusher"""
        electric_force = electric_field_function(self.x) * self.q / self.m
        v_new = self.v + electric_force * dt

        self.x += v_new * dt
        self.x %= L
        energy = self.v * v_new / (2 * self.m)
        self.v = v_new
        return energy

    def distribute_uniformly(self, Lx, shift=False):
        self.x = (np.linspace(0, Lx, self.N, endpoint=False) + shift * self.N/Lx/10) % Lx

    def sinusoidal_position_perturbation(self, amplitude, mode, L):
        self.x += amplitude * np.cos(2 * mode * np.pi * self.x / L)
        self.x %= L
