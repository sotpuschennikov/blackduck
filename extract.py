import csv
import re
from pprint import pprint

data = {}
data2 = {}

def read_encryption_data(inf):
    reader_keys  = csv.reader(inf)
    titles = [_.strip() for _ in reader_keys.next()]
#    unversion = re.compile('-[0-9]')
    unversion = re.compile('_[0-9]')
    for row in reader_keys:
        current = dict(zip(titles, row))
        if current['Package'] != '':
            current_package = unversion.split(current['Package'])[0]
        else:
            current['Package'] = current_package
            if len(current['Algorithm']) > 0:
                if current['Package'] in data.keys():
                    data[current['Package']][current['Algorithm'].lstrip().\
                    rstrip()]=current['MaxKeyLength'].lstrip().rstrip()
                else:
                    data[current['Package']]={current['Algorithm'].lstrip()\
                    .rstrip() : current['MaxKeyLength'].lstrip().rstrip()} 
    pprint(data)
    return data

def read_package_data(inf):
    reader_lic = csv.reader(inf)
    titles = [_.strip() for _ in reader_lic.next()]
    for row in reader_lic:
        current2 = {k:v.strip() for k, v in zip(titles, row)
                    if k != '' and v != ''}
        if current2.get('Package name') is not None:                                  
            current2['Encryption'] = data.get(current2['Package name'])
            data2[current2['Package name'].strip()] = current2
    return data2
   
def write_out_data(merged_data, outf):
    fieldnames = ('Package name', "Package Description", 'Package License',\
                  'Encryption types', 'Encryption Max Key Length')
    writer=csv.DictWriter(outf, fieldnames=fieldnames)
    headers = dict( (n,n) for n in fieldnames )
    writer.writerow(headers)
    for key,value in merged_data.items():
        if packname == key:
            key = ''
        if packdescr == value['Package Description']:
            value['Package Description'] = ''
        if packlic == value['Package License']:
            value['Package License'] = ''
        writer.writerow( { 'Package name':key,
                           'Package Description':value['Package Description'],
                           'Package License':value['Package License'],
                           'Encryption types':value['Algorithm'],
                           'Encryption Max Key Length':value['MaxKeyLength'] ,
                         }
                       )
        packname = key
        packdesc = value['Package Description']
        packlic = value['Package License']
   
def merge_package_encryption_data_2(data, data2):
    tmp_k=''
    for k,v in data2.items():
        for k2,v2 in data.items():
            data3['Package name'] = ({'Package Description':v['Package Description'],
                                      'Package License':v['Package License'],
                                      'Encryption types':v2['Algorithm'],
                                      'Encryption Max Key Length':v2['MaxKeyLength'],
                                     }
                                    )
            pprint(data3)
    return data3

def merge_package_encryption_data(data, data2, outf):
    fieldnames = ('Package name', "Package Description", 'Package License',\
                  'Encryption types', 'Encryption Max Key Length')
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
            writer.writerow( { 'Package name':k,
                               'Package Description':v['Package Description'],
                               'Package License':v['Package License'],
                               'Encryption types':'',
                               'Encryption Max Key Length':'',
                              }
                          )

def main(enc_input, package_input, output):
    with open(enc_input, 'rb') as inf:
            encryption_data = read_encryption_data(inf)
    inf.close()        
    
    with open(package_input, 'rb') as inf:
            package_data = read_package_data(inf)
    inf.close()        

    with open(output, 'w') as outf:
        merge_package_encryption_data(encryption_data, package_data, outf)
    outf.close()    

if __name__ == "__main__":
    main('ubuntu61.csv', 'license_mos_6.1_deb.csv', 'deb_output.csv')
