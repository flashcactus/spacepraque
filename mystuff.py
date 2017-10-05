#!/usr/bin/python3

import re

class CmdProcessor:
    def __init__(self):
        self.commands = []

    def regcmd(self, cmd_regex):
        '''decorator for commands'''
        return lambda fun: self.add_cmd(cmd_regex,fun)

    def add_cmd(self, cmd_regex, fun):
        '''add command to procesor'''
        cmd_pattern = re.compile(cmd_regex)
        self.commands.append((cmd_pattern,fun))

    def parse_cmd(self,cmd_text):
        for patt,fun in self.commands:
            match = patt.match(cmd_text)
            if match is not None:
                return fun, match
        else:
            raise KeyError('command not found')

    def run_cmd(self, cmd_text, runfun=lambda f,m: f(m)):
        fun, match = self.parse_cmd(cmd_text)

 
def readmatr():
    mat = []
    while True:
        tokens = input().split()
        if not len(tokens):
            break
        mat.append(list(map(float,tokens)))
    minlen = min(map(len,mat))
    return [row[:minlen] for row in mat]


