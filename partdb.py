
import os
import json
import urllib
import datetime

import settings
import octopart

today = datetime.datetime.utcnow().strftime("%Y%m%d")
#today = "20130510"

def safe(s): #TODO: this
    return s.lower()

def ensure_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def part_path(p):
    vendor = safe(p[0])
    mpn = safe(p[1])
    return '/'.join((settings.OCTOPART_CACHE_FOLDER, today, vendor, mpn)) + '.json'

def read_part(p):
    with open(part_path(p), 'r') as f:
        part = json.loads(f.read())
    return part

def write_part(p, data):
    pp = part_path(p)
    ensure_dir(os.path.dirname(pp))
    with open(part_path(p), 'w') as f:
        f.write(json.dumps(data))

def check_part(p):
    pp = part_path(p)
    return os.path.exists(pp) and os.path.isfile(pp)

def ensure_bom(bom):
    # first things first
    ensure_dir(settings.OCTOPART_CACHE_FOLDER)
    ensure_dir('/'.join((settings.OCTOPART_CACHE_FOLDER, today)))

    fetch_list = []
    for p in bom:
        if not check_part(p):
            fetch_list.append(( safe(p[0]), safe(p[1]) ))
            print "Will fetch part: %s" % str(p)

    if len(fetch_list):
        results = octopart.fetch_bom(fetch_list)
        for p in fetch_list:
            pid = "%s|%s" % p
            if results[pid]:
                write_part(p, results[pid])
            else:
                write_part(p, dict())
                print "Part not found: %s" % str(p)

def part_url(p):
    return octopart.url_info(read_part(p))

def best_price_info(bom):
    best = None
    for p in bom:
        info = octopart.price_info(read_part(p))
        if not best:
            best = info
        elif not best['price'] and info['price']:
            best = info
        elif info['price'] and info['price'] < best['price']:
            best = info
    if type(best['price']) not in (str, unicode):
        best['price'] = "$%.2f" % best['price']
    return best

