#!/usr/bin/python

import math
import numpy as np


class ThermSolver():
    def __init__(self, xsize, xsteps, dt, tsteps, initial_temp, diff_coeff, ih_fun):
        self.xsize = xsize
        self.xsteps = xsteps 
        self.dt = dt 
        self.tsteps = tsteps 
        self.initial_temp = initial_temp 
        self.diff_coeff = diff_coeff 
        self.ih_fun = ih_fun
        self.mkdeps()


    def mkdeps(self):
        self.dx = self.xsize/self.xsteps
        self.maxt = self.tsteps * self.dt


    def update(self, *args, **kwargs):
        self.__init__(*args, **kwargs)


    def solve(self, tsteps = None):
        self.mkdeps()
        self.xes = np.linspace(0,self.xsize,self.xsteps)
        self.grid = [np.array([self.initial_temp(x) for x in self.xes])]

        self.lambdas = np.zeros(self.xsteps, dtype="float")

        for k in range(1,self.xsteps//2):
            self.lambdas[k] = 4 * self.diff_coeff * self.dx**-2 * np.sin(k*self.dx/4)**2
            self.lambdas[-k] = self.lambdas[k]

        for t in range(self.tsteps):
            self.mk_next()

        
    def mk_next(self, num_iterations=5):
        '''black numerical magic'''
        tstep = len(self.grid)
        dt = self.dt
        #print(tstep*self.dt)
        um = self.grid[-1]
        fum = np.fft.fft(um)
        us = um
        fus = fum
        F1 = self.ih_fun(um, tstep*dt)
        for s in range(num_iterations):
            F2 = self.ih_fun(us, tstep*dt)
            f = np.fft.fft((F1+F2)/2)
            fus = ((2 - self.lambdas * dt) * fum + f * dt) / (2 + self.lambdas * dt)
            us = np.fft.ifft(fus)
        self.grid.append(np.real(us))

    
    def get_value(self, x, t):
        return self.grid[t//self.dt, x//self.dx]

    def get_solution(self):
        return lambda x,t: self.get_value(x,t)


