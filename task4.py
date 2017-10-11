#!/usr/bin/python3
import sys


def get_transactions(filename):
    with open(filename, 'r') as f:
        for num, line in enumerate(f):
            if not num % 50000:
                print('.', end='')
            tokens = line.strip().split()
            if len(tokens) == 7:
                ttype = tokens[1]
                try:
                    ttime = int(tokens[-1])
                except Exception as e:
                    print('OOPS', type(e), e.args)
                else:
                    yield ttype, ttime
            else:
                print('WAT', len(tokens), '|', ' '.join(tokens))
        print()


def sort_transactions(filename):
    stg = {}
    print('parsing file')
    for ttype, ttime in get_transactions(filename):
        if ttype in stg:
            stg[ttype].append(ttime)
        else:
            stg[ttype] = [ttime]
    for tt in stg:
        stg[tt].sort()
    return stg


def make_event_stats(sorted_times):
    datalen = len(sorted_times)
    quantile = lambda q: sorted_times[int((datalen - 1) * q)]
    clinfo = (
        ('min', quantile(0)),
        ('50%', quantile(0.5)),
        ('90%', quantile(0.9)),
        ('99%', quantile(0.99)),
        ('99.9%', quantile(0.999))
    )
    xtdict = {}
    for rt in map(lambda t: t // 5, sorted_times):
        if rt not in xtdict:
            xtdict[rt] = 0
        xtdict[rt] += 1

    stat_tbl = []
    ttn = 0
    for xt in sorted(xtdict):
        ttn += xtdict[xt]
        stat_tbl.append([xt, xtdict[xt], xtdict[xt] / datalen, ttn / datalen])

    return clinfo, stat_tbl


def format_table(evtname, stat_tbl):
    tbtempl = '''<h3>{evtname}</h3>
<table>
    <tr> <td>ExecTime</td> <td>TransNo</td> <td>Weight,%</td> <td>Percent</td> </tr>
{rows}
</table>
'''
    format_row = lambda row: '<tr><td>{:d}</td><td>{:d}</td><td>{:5.2f}</td><td>{:5.2f}</td></tr>'.format(
        row[0], row[1], row[2] * 100, row[3] * 100)

    return tbtempl.format(evtname, '\n'.join(map(format_row, stat_tbl)))


def print_stats(statdict):
    txt = ''
    html = ''
    for eventname, (txtinfo, htmlinfo) in statdict:
        txt += eventname + ' '.join('{n}={v}'.format(n, v) for n, v in txtinfo + '\n'
        html += format_table(eventname, htmlinfo)
