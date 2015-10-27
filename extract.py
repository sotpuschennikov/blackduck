import csv
import re
import sys
import os

data = {}
data2 = {}
distr = ''
release = os.environ["RELEASE"]

def read_encryption_data(enc_input, distr):
    if distr == 'rpm':
        unversion = re.compile('-[0-9]')
    else:
        unversion = re.compile('_[0-9]')
    with open(enc_input, 'rb') as inf:
        reader_keys  = csv.reader(inf)
        titles = [_.strip() for _ in reader_keys.next()]
        for row in reader_keys:
            current = dict(zip(titles, row))
            if current['Package'] != '':
                current_package = unversion.split(current['Package'])[0]
            else:
                current['Package'] = current_package
                if len(current['Algorithm']) > 0:
                    if current['Package'] in data.keys():
                        data[current['Package']][current['Algorithm'].lstrip().\
                        rstrip()]={current['MaxKeyLength'].lstrip().rstrip() : \
                                   current['Comment'].lstrip().rstrip()}
                    else:
                        data[current['Package']]={
                            current['Algorithm'].lstrip().rstrip() : \
                            {current['MaxKeyLength'].lstrip().rstrip() : \
                             current['Comment'].lstrip().rstrip()}
                            }
    return data

def read_package_data(package_input):
    with open(package_input, 'rb') as inf:
        reader_lic = csv.reader(inf)
        titles = [_.strip() for _ in reader_lic.next()]
        for row in reader_lic:
            current2 = {k:v.strip() for k, v in zip(titles, row)
                        if k != '' and v != ''}
            if current2.get('Package name') is not None:
                current2['Encryption'] = data.get(current2['Source'])
                data2[current2['Package name'].strip()] = current2
        return data2

def merge_package_encryption_data(data, data2, output):
    fieldnames = ('Package name', "Source", "Package Description", 'Package License',\
                  'Encryption types', 'Encryption Max Key Length', "Comment")
    with open(output, 'w') as outf:
        writer=csv.DictWriter(outf, fieldnames=fieldnames)
        headers = dict( (n,n) for n in fieldnames )
        writer.writerow(headers)
        tmp_k=''
        for k,v in data2.items():
            if v['Encryption'] is not None:
                for name,fields in v['Encryption'].items():
                    for maxlen,comment in fields.items():
                        writer.writerow( { 'Package name':k,
                                           'Source':v['Source'],
                                           'Package Description':v['Package Description'],
                                           'Package License':v['Package License'],
                                           'Encryption types':name,
                                           'Encryption Max Key Length':maxlen,
                                           'Comment': comment,
                                         }
                                       )
            else:
                writer.writerow( { 'Package name':k,
                                   'Source':v['Source'],
                                   'Package Description':v['Package Description'],
                                   'Package License':v['Package License'],
                                   'Encryption types':'',
                                   'Encryption Max Key Length':'',
                                 }
                               )

def main(enc_input, package_input, output):
    if enc_input == 'ubuntu' + release + '.csv':
        distr = 'deb'
    else:
        distr = 'rpm'
    encryption_data = read_encryption_data(enc_input, distr)

    package_data = read_package_data(package_input)

    merge_package_encryption_data(encryption_data, package_data, output)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
