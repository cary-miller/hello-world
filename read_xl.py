'''
Read excel files.
xlrd is quite good but it is old and fails to read xlsx files.
xlsrd supposedly reads them but it is not available via pip so I'm not
taking the trouble to track it down further.
openpyxl is even better than xlrd and reads xlsx.
'''



import xlrd
#import xlsxrd  # supposedly reads xlsx but not available via pip.

try: book = xlrd.open_workbook(fname)
except: pass
# xlrd is really lagging with xlsx support.  Criminey, the format has
# been around for years and they still don't support it.  Fortunately
# openpyxl comes along to deal with it.

import openpyxl
from openpyxl.reader.excel import load_workbook



wb = load_workbook(fname)
sn = wb.get_sheet_names()

s1 = wb.worksheets[0]
data = [[cell.value for cell in row] for row in s1.rows]
head = data[0]
data = data[1:]



def stringify(thing):
    if thing is None: return '-'                     # None
    if type(thing) == str: return thing         # string
    if type(thing) == int: return str(thing) # int
    return thing



def delimited(data, 
    row_delim='\n', 
    col_delim='\t', 
    cell_func=lambda x:x, 
    row_func=lambda x:x):
    return row_delim.join([col_delim.join(row_func(
        cell_func(col) for col in row)) for row in data])


s = '\n'.join(['\t'.join([stringify(v) for v in row]) for row in data])
t = delimited(data, cell_func=stringify)
assert s==t

print s


