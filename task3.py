#!/usr/bin/python3

import mystuff
import math

mcproc = mystuff.CmdProcessor()

fdict = {}

funs = {
    'mul': lambda a,b: a * b,
    'pow': lambda a,b: a ** b, 
    'sin': lambda a,b: math.sin(a * math.pi + b)
}

@mcproc.command("([a-zA-Z]+) *= *(mul|pow|sin) +([0-9.]+)")
def add_function(match):
    name, fname, arg = match.groups()
    fdict[name] = (funs[fname], float(arg))
    return 'OK'

@mcproc.command("([a-zA-Z]+)\(([0-9.]+)\)")
def run_function(match):
    name, arg = match.groups()
    fun, funarg = fdict[name]
    return fun(funarg, float(arg))

def read_cmd():
    cmd = input('> ')
    try:
        print(mcproc.run_cmd(cmd))
    except Exception as e:
        print(type(e),e.args)



while True: 
    read_cmd()
