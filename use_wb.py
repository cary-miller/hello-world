from worldbank import WorldBank

import functools
import json
import csv
from cStringIO import StringIO

wb = WorldBank(per_page=10000)  # connect to World Bank


def table(res, transform=lambda x:x, filter=lambda x:True):
    return [transform(ob) for ob in res if filter(ob)]


def none2(thing, to=0):
    '''alt name:  convert_none
    '''
    if thing is None: return to
    return thing


def xform(ob):
    '''Transform a dict into a table row / list.
    '''
    return [int(ob['date']), 
        ob['country']['id'], 
        ob['indicator']['id'], 
        ob['indicator']['value'], 
        float(none2(ob['value']))
        ]

def xform2(ob):
    '''Transform a dict into a table row / list.
    '''
    return [int(ob['date']), 
        ob['country']['id'], 
        float(none2(ob['value']))
        ]



def fetch(indicator=None, date=None, country=None, transform=xform2):
    (junk, js) = wb.get_country(code=country, date=date, indicator=indicator)
    return table(js, transform=transform)


def to_json(data):
    return json.dumps(data)+'\n'


def to_csv(data):
    ofile = StringIO()
    out = csv.writer(ofile, delimiter='\t')
    for row in data: out.writerow(row[:2]+[row[-1]])
    ofile.seek(0)
    return ofile.read()



def save_data(fmat='json'):
    # Current latest year available == 2009
    # One indicator for multiple countries over multiple years.

    country_list='br;ca;cn;de;fr;in;jp;mx;ru;us'
    date_range='1980:2009'
    indicator_id='EG.IMP.TOTL.KT.OE'   # imports (KT)  EMPTY

    format_d = dict(json=to_json, csv=to_csv)

    def to_file(indicator_id):
        fname = indicator_id +'.'+ fmat
        to_format = format_d[fmat]
        data = fetch(indicator=indicator_id, date=date_range, country=country_list)
        with open(fname, 'w') as out:
            out.write(to_format(data))

#    to_file('EG.IMP.CONS.ZS')   # imports (% of total) (use?).
#    to_file('EG.USE.COMM.KT.OE')   # use (KT)
#    to_file('EG.EGY.PROD.KT.OE')   # production (KT)

    to_file('NY.GDP.MKTP.KD')   # 'GDP (constant 2000 US$)'


demo=True
demo=False
if demo:
    from pprint import pprint

    def wb_info(global_ob):
        t = lambda x: (x['name'], x['id'])
        return functools.partial(table, global_ob[1], transform=t)
     
    # Get general info re countries and indicators
    cnt = wb.get_country()	# general data on all countries
    indicators = wb.get_indicators()	# all 6000+ indicators

    # Country info
    country_info = wb_info(cnt) # function to display country info
    pprint(sorted(country_info()))
    filt=lambda c:c['name'].startswith('Bra')
    pprint(sorted(country_info(transform=lambda c:c['name'], filter=filt)))


    # Indicator info
    indicator_info = wb_info(indicators) # display function
    _filter = lambda ob: 'Energy imports' in ob['name']
    _filter = lambda ob: 'nergy' in ob['name']
    _filter = lambda ob: 'Energy use' in ob['name']
    _filter = lambda ob: 'Energy production' in ob['name']
    pprint(sorted(indicator_info(filter=_filter)))

    '''
    These are the energy indicators I discovered.
    [(u'Energy imports (kt of oil equivalent)', u'EG.IMP.TOTL.KT.OE'), # blank
     (u'Energy imports, net (% of energy use)', u'EG.IMP.CONS.ZS')]  OK

     (u'Energy production (kt of oil equivalent)', u'EG.EGY.PROD.KT.OE')  OK

    [(u'Energy use (kg of oil equivalent per capita)', u'EG.USE.PCAP.KG.OE' X
    'Energy use (kg of oil equivalent) per $1,000 GDP (constant 2005 PPP)' X
      u'EG.USE.COMM.GD.PP.KD'),
     (u'Energy use (kt of oil equivalent)', u'EG.USE.COMM.KT.OE')]  OK
    '''

    br_iz = wb.get_country(code='bra', indicator='EG.IMP.CONS.ZS')
    x_iz = wb.get_country(indicator='EG.IMP.CONS.ZS') # one indicator, all countries

    _filter = lambda ob: 'lectricity prod' in ob['name']
    pprint(sorted(indicator_info(filter=_filter)))


    _filter = lambda ob: ob['name'].startswith('GDP (')
    pprint(sorted(indicator_info(filter=_filter)))

    '''
 (u'GDP (constant 2000 US$)', u'NY.GDP.MKTP.KD')
 (u'GDP (constant LCU)', u'NY.GDP.MKTP.KN')
 (u'GDP (current LCU)', u'NY.GDP.MKTP.CN')
 (u'GDP (current US$)', u'NY.GDP.MKTP.CD')
 (u'GDP (implicit price deflator contant 2005 USD)', u'NYGDPMKTPXD') 
    '''

