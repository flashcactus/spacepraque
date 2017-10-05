import re
import mystuff

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

cp = mystuff.CmdProcessor()

@cp.regcmd('diagsum ([0-9]+)')
def diagsum(*args):
    pass
