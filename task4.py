#!/usr/bin/python3
import sys


def get_transactions(fileobj):
    for num, line in enumerate(fileobj):
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


def sort_transactions(fileobj):
    stg = {}
    print('parsing file')
    for ttype, ttime in get_transactions(fileobj):
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
    for rt in map(lambda t: t - t % 5, sorted_times):
        if rt not in xtdict:
            xtdict[rt] = 0
        xtdict[rt] += 1

    stat_tbl = []
    ttn = 0
    for xt in sorted(xtdict):
        ttn += xtdict[xt]
        stat_tbl.append([xt, xtdict[xt], xtdict[xt] / datalen, ttn / datalen])

    return clinfo, stat_tbl


make_stats = lambda stimes_dict: {k:make_event_stats(l) for k,l in stimes_dict.items()}


def format_table(evtname, stat_tbl):
    tbtempl = '''<h3>{evtname}</h3>
<table>
    <tr> <td>ExecTime</td> <td>TransNo</td> <td>Weight,%</td> <td>Percent</td> </tr>
{rows}
</table>
'''
    rowtempl = '<tr><td>{:d}</td><td>{:d}</td><td>{:5.2f}</td><td>{:5.2f}</td></tr>'

    format_row = lambda row: rowtempl.format(
        row[0], row[1], row[2] * 100, row[3] * 100)

    return tbtempl.format(evtname=evtname, rows='\n'.join(map(format_row, stat_tbl)))


def format_stats(statdict):
    txt = ''
    html = ''
    html_templ = '<html>\n<head></head>\n<body>\n{}\n</body>\n</html>'
    for eventname,(txtinfo, htmlinfo) in statdict.items():
        txt += eventname + ' '.join('{}={}'.format(n, v) for n, v in txtinfo) + '\n'
        html += format_table(eventname, htmlinfo)
    return txt,html_templ.format(html)


def write_reports(inputfile, outfile_txt, outfile_html):
    txt, html = format_stats(make_stats(sort_transactions(inputfile)))
    outfile_txt.write(txt)
    outfile_html.write(html)



#process args
import optparse
import sys 

from optparse import OptionParser
    
parser = OptionParser()
parser.add_option("-i", "--input", dest="ifname", metavar="FILE", help="read data from FILE")
parser.add_option("-o", "--output_prefix", dest="ofprefix",
                 help="write reports to \"PREFIX.txt\" and \"PREFIX.html\"", metavar="PREFIX")
parser.add_option("--output_txt", dest="ofname_t", metavar="FILE", help="write text report to FILE")
parser.add_option("--output_html", dest="ofname_h", metavar="FILE", help="write HTML report to FILE")
parser.add_option("-c", "--config", dest="config_fname", metavar="FILE", help="read configuration from FILE")
parser.add_option("-q", "--quiet",
                 action="store_false", dest="verbose", default=True,
                 help="don't print status messages to stdout")

(options, args) = parser.parse_args()

#parse config or use cmdline names or load defaults
#do the actual thing
with open(options.ifname,'r') as inputfile, open(options.ofname_t,'w') as ofile_txt, open(options.ofname_h, 'w') as ofile_html:
    write_reports(inputfile, ofile_txt, ofile_html)
