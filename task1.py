import re

def readmatr():
    mat = []
    while True:
        tokens = input().split()
        if not len(tokens):
            break
        mat.append(list(map(float,tokens)))
    minlen = min(map(len,mat))
    return [row[:minlen] for row in mat]

def trace(mat,offset):
    return 


class CmdProcessor:
    def __init__(self):
        self.commands = []

    def regcmd(self, cmd_regex):
        def _reg_cmd_decorator(fun):
            self.add_cmd(cmd_regex,fun)
        return _reg_cmd_decorator

    def add_cmd(self, cmd_regex, fun):
        cmd_pattern = re.compile(cmd_regex)
        self.commands.append((cmd_pattern,fun))

    def run_cmd(self,cmd_text):
        for patt,fun in self.commands:
            match = patt.match(cmd_text)
            if match is not None:
                return fun(match)
                        

cp = CmdProcessor()

@cp.regcmd('diagsum ([0-9]+)')
