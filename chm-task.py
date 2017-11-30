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

solver = chm.ThermSolver(math.pi*2, 100, 0.5, 110, lambda x: math.sin(5*x), 0.01, lambda u,t: np.sin(0.1*u * t) ) 

solver.solve()

for r in solver.grid:
    pass
    #print(r)


root = tk.Tk()
root.wm_title("chm-task")

controls = tk.LabelFrame(root, text="parameters")
controls.pack(side=tk.LEFT)

#graphing stuff
graphframe = tk.Frame(root)
graphframe.pack(side=tk.RIGHT, expand=1)

class graphbox:
    def __init__(self, parent, fig):
        pass


def mk_animation(ax, fps=25):
    print('animation called')
    ax.clear()
    line, = ax.plot(solver.xes, solver.grid[0])

    ax.set_xlabel('x')
    ax.set_ylabel('T')
    ax.set_aspect('auto')
    ax.autoscale_view()
    ax.relim()

    def init():
        line.set_data([],[])
        return line,

    def upd(t):
        line.set_data(solver.xes, solver.grid[int(t/solver.dt)])
        ax.autoscale_view()
    
    animator = mpl_ani.FuncAnimation(ax.get_figure(), upd, init_func=init, frames=np.linspace(0, solver.maxt, solver.tsteps+1), interval=1000/fps, blit=False)

    return ax, animator


def draw_hmap(ax):
    ax.clear()
    xfmt = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*solver.dx))
    tfmt = matplotlib.ticker.FuncFormatter(lambda t, pos: '{0:g}'.format(t*solver.dt))
    print('hmap called')
    ax.imshow(np.array(solver.grid).transpose(),origin='lower')
    ax.xaxis.set_major_formatter(tfmt)
    ax.set_xlabel('t')
    ax.yaxis.set_major_formatter(xfmt)
    ax.set_ylabel('x')
    return ax


def show_graph(canvas):
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return canvas

fig = plt.Figure()
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=graphframe)
canvas = show_graph(canvas)
#draw_hmap(ax)

#def on_key_event(event):
#    print('you pressed %s' % event.key)
    #key_press_handler(event, canvas, toolbar)

#canvas.mpl_connect('key_press_event', on_key_event)

#controls

entries = {
    'xsteps':['grid steps (X)', int],
    'dt':['Δt', float],
    'tsteps':['time steps', int],
    'diff_coeff':['diffusion coeff.', float],
}

for e,ed in entries.items():
    cont = tk.Frame(controls)
    label = tk.Label(cont, text=ed[0])
    label.pack(side=tk.LEFT)
    ent = tk.Entry(cont)
    ent.pack(side=tk.RIGHT)
    ent.insert(0,getattr(solver,e))
    entries[e].append(ent)
    cont.pack(fill=tk.X, expand=1)

def recalc():
    for wn, wd in entries.items():
        print(wn, wd[1](wd[2].get()))
        setattr(solver, wn, wd[1](wd[2].get()))
    solver.solve()
    print(len(solver.grid))
    print(solver.grid[2])

def show_hmap():
    recalc()
    global ax
    ax = draw_hmap(ax)
    show_graph(canvas)

def show_animation():
    recalc()
    global ax
    ax,an = mk_animation(ax)
    show_graph(canvas)
    #an()

button = tk.Button(master=controls, text='show heatmap', command=show_hmap)
button.pack()


abtn = tk.Button(master=controls, text='animate', command=show_animation)
abtn.pack()

tk.mainloop()
