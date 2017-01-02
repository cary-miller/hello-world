#!/home/cary/bar/bin/python3

import sys
import pandas as pd



def raw_data(data_file):
    try:
        skip = 0
        n = 200
        dataf = pd.read_csv(data_file, skipinitialspace=True, skiprows=skip, nrows=n)
        dataf.index = dataf['id']
        del dataf['id']
        return dataf
    except pd.io.parsers.CParserError as exc:
        print(exc)
        print('yoohoo')
        raise


def raw_lines(data_file):
    with open(data_file) as fh:
        lines = fh.readlines()
    return [line.strip() for line in lines if line.split()]


def comma_check(data_file):
    info = lambda line: (line.split(',')[0], line.count(','))
    return [info(line) for line in raw_lines(data_file)]



names = '''id length height v2 v4.1 v4.2 v3.1 v3.2 v5.1 v5.2 v5.3 v5.4 vfr.1 vfr.2       h2 h4.1 h4.2 h3.1 h3.2 h5.1 h5.2 h5.3 h5.4 hfr.1 hfr.2'''.split()

# read csv data
data_file = 'esthetic_data.csv'
dataf = raw_data(data_file)
column_names = dataf.columns.tolist()
lines = comma_check(data_file)
bad = [(name, n) for (name, n) in lines if n != 24]
from collections import namedtuple
raw = raw_lines(data_file)



if __name__ == '__main__':
    pass
 #   print('dataf')
  #  print(dataf)
   # print('ds')
#    print(ds)

