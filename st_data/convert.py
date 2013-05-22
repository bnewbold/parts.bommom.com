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
    "returns (family, subfamily, memory, package)"
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

family_key = PREFIXES[1]
family = lists[family_key]
print "PROCESSING: " + family_key

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

for subfamily in tree.values():
    subfamily_keys = part.keys() # old part from above
    subfamily_keys.remove('mpn')
    uncommon_keys = list()
    for spec in subfamily_keys:
        #subfamily_items = [p for p in [m for m in subfamily]]
        if not identical([x[spec] for x in [pkg.values() for pkg in [mem.values() for mem in subfamily.values()]]]):
            subfamily_keys.remove(spec)
            uncommon_keys.append(spec)
    print subfamily_keys
    subfamily['_common_specs'] = subfamily_keys
    subfamily['_uncommon_specs'] = uncommon_keys

pkg_keys = []
def csv_for_family():
    part_dict = dict()
    spec_list = []
    for subfamily_key in sorted(family.keys()):
        for mem_key in sorted(family[subfamily_key].keys()):
            mem = family[subfamily_key][mem_key]
            mem_part = mem.values()[0]
            mem_part['Part Number'] = family_key + subfamily_key + "x" + mem_key
            mem_part['PKG_PINS'] = dict()
            for pkg_key in mem.keys():
                if not pkg_key in pkg_keys:
                    pkg_keys.append(pkg_key)
                mem_part['PKG_PINS'][pkg_key] = mem[pkg_key]['I/O Pins']
            part_dict[mem_part['Part Number']] = mem_part

    sorted_part_names = sorted(part_dict.keys())
    spec_list.remove('Part Number')
    spec_list.insert(0,'Part Number')
    for spec in spec_list:
        # generate 'line' string of all parts for spec
        pass



print_family(family)

"""
def combine(tree, depth):
    if depth:
        combinel(
"""
