import csv
import re
packages = list()
#for infile in ('centos61.csv', 'feick.csv'):
data = dict()
data2 = dict()
with open('centos61.csv', 'rb') as inf:
    reader_keys  = csv.reader(inf)
    titles = [_.strip() for _ in reader_keys.next()]
    unversion = re.compile('-[0-9]')                
    for row in reader_keys:
        current = dict(zip(titles, row))
        if current['Package'] != '':
            current_package = unversion.split(current['Package'])[0]
        else:
            current['Package'] = current_package
            if len(current['Algorithm']) > 0:
                if current['Package'] in data.keys():
                    data[current['Package']][current['Algorithm'].lstrip().rstrip()]=current['MaxKeyLength'].lstrip().rstrip()
                else:
                    data[current['Package']]={current['Algorithm'].lstrip().rstrip() : current['MaxKeyLength'].lstrip().rstrip()} 
inf.close()
with open('license_mos_6.1_rpm.csv', 'rb') as inf:
     reader_lic = csv.reader(inf)
     titles = [_.strip() for _ in reader_lic.next()]
     print titles
     for row in reader_lic:
         current2 = {k:v.strip() for k, v in zip(titles, row) 
                     if k != '' and v != ''}
         if current2.get('Package name') is not None:                                  
             current2['Encryption'] = data.get(current2['Package name'])
             data2[current2['Package name'].strip()] = current2
inf.close()
from pprint import pprint
#pprint(data)
#for k, v in data2.items():
#    if v['Encryption'] is not None:
#        print k,
#        pprint(v)
#exit()
with open('output.csv', 'w') as outf:
#        writer=csv.writer(outf, dialect='excel', lineterminator='\n')
    fieldnames = ('Package name', "Package Description", 'Package License', 'Encryption types', 'Encryption Max Key Length')
    writer=csv.DictWriter(outf, fieldnames=fieldnames)
    headers = dict( (n,n) for n in fieldnames )
    writer.writerow(headers)
    tmp_k=''
    for k,v in data2.items():
        if v['Encryption'] is not None:
            tmp_k=k
            packdesc=''
            packlic=''
            for name,fields in v['Encryption'].items():
                if packdesc == v['Package Description']:
                    v['Package Description']=''
                if packlic == v['Package License']:
                    v['Package License']=''
                writer.writerow( { 'Package name':tmp_k,
                                   'Package Description':v['Package Description'],
                                   'Package License':v['Package License'],
                                   'Encryption types':name,
                                   'Encryption Max Key Length':fields,
                                 }
                )
                tmp_k=''
                packdesc=v['Package Description']
                packlic=v['Package License']
        else:
            pprint(v)
            writer.writerow( { 'Package name':k,
                               'Package Description':v['Package Description'],
                               'Package License':v['Package License'],
                               'Encryption types':'',
                               'Encryption Max Key Length':'',
                              }
                           )
inf.close()
outf.close()
