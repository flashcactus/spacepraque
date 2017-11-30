#!/usr/bin/python3

import matplotlib
matplotlib.use('TkAgg')

import math
import numpy as np
from numpy import pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.animation as mpl_ani

import sys

try:
    import tkinter as tk
except:
    import Tkinter as tk

import chm


xes = np.linspace(0,1,100)
t = np.linspace(0,5,100)

z = np.zeros((100,100))
for t in range (100):
    z[t] = np.sin(0.5*xes + 0.07*t)

solver = chm.ThermSolver(math.pi*2, 100, 0.5, 110, lambda x: math.sin(5*x), 0.01, lambda u,t: np.sin(0.1*u + t) ) 

solver.solve()

for r in solver.grid:
    pass
    #print(r)


root = tk.Tk()
root.wm_title("chm-task")

controls = tk.Frame(root, background="#000")
controls.pack(side=tk.LEFT)

entries = {
    'xsteps':['grid steps (X)', int],
    'dt':['Δt', float],
    'tsteps':['time steps', int],
    'diff_coeff':['diffusion coeff.', float],
}

entry_widgets = {}

for e,ed in entries.items():
    cont = tk.Frame(controls)
    label = tk.Label(cont, text=ed[0])
    label.pack(side=tk.LEFT)
    ent = tk.Entry(cont)
    ent.pack(side=tk.RIGHT)
    ent.insert(0,getattr(solver,e))
    entries[e].append(ent)
    cont.pack(fill=tk.X, expand=1)

canv = None
def recalc():
    for wn, wd in entry_widgets.items():
        setattr(solver, wnm, wd[1](wd[2].get()))
    solver.solve()
    canv = show_graph(mk_hmap(), canv)

button = tk.Button(master=controls, text='recalculate', command=recalc)
button.pack(side=tk.BOTTOM)


#graphing stuff
graphframe = tk.Frame(root)
graphframe.pack(side=tk.RIGHT, expand=1)


def show_graph(fig, canv=None):
    canvas = FigureCanvasTkAgg(fig, master=graphframe) if canv is None else canv
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return canvas

def mk_animation(fps=25):
    print('animation called')
    anifig = plt.Figure()
    aniax = anifig.add_subplot(111)
    aniline, = aniax.plot(solver.grid[0])

    def ani_init():
        aniline.set_data([],[])
        return aniline,

    def ani_set(t):
        aniline.set_data(solver.xes, solver.grid[t/solver.dt])

    anicanv = show_graph(anifig)
    
    animator = lambda: mpl_ani.FuncAnimation(anifig, ani_set, init_func=ani_init, frames=np.linspace(0, solver.maxt, solver.tsteps+1), interval=1000/fps, blit=False)

    animator()

    return anicanv


def mk_hmap():
    xfmt = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*solver.dx))
    tfmt = matplotlib.ticker.FuncFormatter(lambda t, pos: '{0:g}'.format(t*solver.dt))
    print('hmap called')
    hmplot = plt.imshow(np.array(solver.grid).transpose(),origin='lower')
    hmfig = hmplot.figure
    hmax = hmplot.axes
    hmax.xaxis.set_major_formatter(tfmt)
    hmax.set_xlabel('t')
    hmax.yaxis.set_major_formatter(xfmt)
    hmax.set_ylabel('x')
    return hmfig


fig = mk_hmap()
canvas = show_graph(fig)
#canvas=mk_animation(20)

def on_key_event(event):
    print('you pressed %s' % event.key)
    #key_press_handler(event, canvas, toolbar)

#canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate



tk.mainloop()

# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
