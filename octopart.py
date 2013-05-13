
import json
import urllib
from decimal import Decimal

from settings import *

def fetch_bom(bom):
    # inspired by "bom_quote.py" provided at http://octopart.com/api
    reply = dict()
    queries = []
    for p in bom:
        pid = "%s|%s" % p
        queries.append({'mpn': p[1],
                        'brand': p[0],
                        'reference': pid})
        reply[pid] = None

    # do requests in batches of 20
    results = []
    for i in range(0, len(queries), OCTOPART_BATCH_SIZE):
        batched_queries = queries[i:i+OCTOPART_BATCH_SIZE]
        url = 'http://octopart.com/api/v3/parts/match?queries=%s' \
            % urllib.quote(json.dumps(batched_queries))
        url += '&apikey=%s' % OCTOPART_API_KEY
        #print url
        data = urllib.urlopen(url).read()
        response = json.loads(data)
        results.extend(response['results'])
   
    #print "len(results): %d" % len(results)

    for result in results:
        pid = result['reference']
        #print "len(items[%s]): %d" % (pid, len(result['items']))
        if len(result['items']) == 0:
            reply[pid] = None
        else:
            reply[pid] = result['items'][0]
    return reply

def price_info(item, quantity=1000):
    if not item:
        return dict(url=None, css='notfound', price='Not Found')
    info = dict(url=item['octopart_url'])
    info['css'] = 'unavailable'
    info['price'] = 'No Offers'
    for offer in item['offers']:
        if not offer['is_authorized']:
            continue
        if not offer['prices'].has_key('USD'):
            continue
        price = None
        for price_pair in offer['prices']['USD']:
            if price_pair[0] <= quantity:
                if not price or price_pair[1] < price:
                    price = price_pair[1]
        if not price:
            print "WARNING: not a price: %s" % price
            continue
        if not info['price'] or price < info['price']:
            info['price'] = Decimal(price)
            if offer['in_stock_quantity'] > 0:
                info['css'] = 'available'
            else:
                info['css'] = 'outofstock'
    return info

def url_info(item):
    if item:
        return item['octopart_url']
    else:
        return None

