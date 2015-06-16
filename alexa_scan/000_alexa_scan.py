import json
import subprocess
import re
import os
import thread
from time import sleep
import fnmatch
import random

subdomains = open('../subdomains.txt').read().split()
org_data = json.loads(open('../alexa.json').read())
data = []

cats_data = {}
for org_datum in org_data:
    domain = org_datum[0]
    cat = org_datum[1]
    if not cat in cats_data:
        cats_data[cat] = []
    cats_data[cat].append(org_datum)


def scan(cat_name, cat_data):
    for file in os.listdir('../'):
        if fnmatch.fnmatch(file, 'alexa_sub_'+cat_name+'.json'):
            print('cat skip: '+cat_name)
            return
    print('cat start: '+cat_name)
    counter = 0
    for cat_datum in cat_data:
        if (counter % 100) == 0:
            print('cat: '+cat_name+str(counter)+'/500')
        domain = cat_datum[0]
        domain_underscore = domain.replace('.', '_')
        cat = cat_datum[1]
        flag_has_scan_result = False
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, domain_underscore+'*'):
                flag_has_scan_result = True
                print('found result for domain: '+domain)
                output = open(file).read()
                break
        if not flag_has_scan_result:
            sleep(0.5)
            print('processing domain: '+domain)
            cmd = 'knockpy -w ../subdomains.txt ' + domain
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            output = process.communicate()[0]
            m = re.search('Output saved in CSV format: (.*\.csv)', output)
            if m:
                # output_file = m.group(1)
                # os.remove(output_file)
                pass
            else:
                open(domain_underscore, 'a').close()
        datum = {}
        datum['domain'] = domain
        datum['category'] = cat
        for subdomain in subdomains:
            datum[subdomain] = (subdomain+'.'+domain) in output
        data.append(datum)
        counter += 1
    json_str = json.dumps(data)
    f = open('../alexa_sub_'+cat_name+'.json', 'w')
    f.write(json_str)
    print('cat finish: '+cat_name)

for cat_name, cat_data in cats_data.iteritems():
    try:
        thread.start_new_thread(scan, (cat_name, cat_data, ))
    except:
        print "Error: unable to start thread"

while True:
    sleep(60)
