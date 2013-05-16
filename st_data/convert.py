#!/usr/bin/env python
"""
MPN structure:
    STM32F101RB 
    STM32F1 01 R B 
    {family} {subfamily} {package} {memory}
"""

import json
import csv

ALL_FILE = "stm32_all_20130509.csv"

PREFIXES = [
    'STM32F0',
    'STM32F1',
    'STM32F2',
    'STM32F3',
    'STM32L',
    'STM32W',
]

def decompose(mpn):
    "returns (family, subfamily, memory, package"
    return mpn[:7], mpn[7:9], mpn[9], mpn[10]

def ensure_recurse_dict(tree, addr):
    if not tree.has_key(addr[0]):
        tree[addr[0]] = dict()
    if len(addr) > 1:
        ensure_recurse_dict(tree[addr[0]], addr[1:])

def identical(l):
    a = l[0]
    for b in l[1:]:
        if a != b:
            return False
    return True

stm32_all_list = []
with open(ALL_FILE, 'r') as f:
    dr = csv.DictReader(f)
    stm32_all_list.extend(dr)

for item in stm32_all_list:
    item['mpn'] = item.pop("Part Number")

lists = dict()

for pref in PREFIXES:
    lists[pref] = [x for x in stm32_all_list if x['mpn'].startswith(pref)]
    print "%s:" % pref
    print '\t' + '\n\t'.join([x['mpn'] for x in lists[pref]])

family = lists[PREFIXES[1]]

# strip common specifications
family_specs = dict()
for spec in family[0].keys():
    if identical([x[spec] for x in family]):
        family_specs[spec] = family[0][spec]
        [item.pop(spec) for item in family]

print family_specs

tree = dict()
for part in family:
    addr = decompose(part['mpn'])
    #ensure_recurse_dict(tree, addr)
    #tree[addr[0]][addr[1]][addr[2]][addr[3]] = part
    ensure_recurse_dict(tree, addr[1:])
    tree[addr[1]][addr[2]][addr[3]] = part

print sorted(tree.keys())


for subfamily in tree.items():
    subfamily_keys = part.keys()
    subfamily_keys.remove('mpn')
    for spec in subfamily_keys:
        subfamily_items = 
        if not identical([x[spec] for x in [pkg.items() for pkg in [mem.items() for mem in subfamily.items()]]]):
            subfamily_keys.remove(spec)
    print subfamily_keys

def combine(tree, depth):
    if depth:
        combinel(
