
import partdb
import csv

def load_csv(path):
    table = []
    with open(path, 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            table.append(row)
    return table

def process_csv(data_path, shared_path, speed_grades, temp_grade):
    raw_specs = load_csv(shared_path)
    raw_data = load_csv(data_path)
    split_row = 0

    # find row split between data and pins
    for i in range(len(raw_data)):
        if raw_data[i][0] == "###":
            split_row = i
            break

    package_table = raw_data[split_row+1:]
    prefix_list = raw_data[0][1:]

    # infill sparse prefix_lists (eg, for xilinx zynq)
    last = None
    for i in range(len(prefix_list)):
        if not prefix_list[i]:
            prefix_list[i] = last
        else:
            last = prefix_list[i]

    suffix_row = [list() for i in range(len(prefix_list))]
    bom = []
    for row_num in range(len(package_table)):
        package = package_table[row_num][0]
        for cell_num in range(len(package_table[row_num][1:])):
            cell = package_table[row_num][cell_num+1].strip()
            if cell:
                for speed_grade in speed_grades:
                    suffix = speed_grade + package + temp_grade
                    mpn = prefix_list[cell_num] + suffix
                    bom.append(('Xilinx', mpn))
                    suffix_row[cell_num].append(dict(mpn=mpn, suffix=suffix))

    shared_specs = dict()
    for row in raw_specs:
        shared_specs[row[0]] = row[1]

    data_table = []
    span = 1
    for raw_row in raw_data[:split_row]:
        row = [[1, raw_row[0]], ]
        for raw_cell in raw_row[1:]:
            if raw_cell:
                row.append([1, raw_cell.replace('n/a', '-')])
            else:
                row[-1][0] += 1
        data_table.append(row)

    partdb.ensure_bom(bom)
    price_row = [None for i in range(len(prefix_list))]
    for i in range(len(prefix_list)):
        bom = [('Xilinx', suf['mpn']) for suf in suffix_row[i]]
        price_row[i] = partdb.best_price_info(bom)

    # attach URLs to suffix row entries
    for cell_num in range(len(suffix_row)):
        cell = suffix_row[cell_num]
        for part_num in range(len(cell)):
            part = cell[part_num]
            p = ('Xilinx', part['mpn'])
            part['url'] = partdb.part_url(p)
            cell[part_num] = part
        suffix_row[cell_num] = cell

    return dict(shared_specs=shared_specs,
                data_table=data_table,
                price_row=price_row,
                package_table=package_table,
                suffix_row=suffix_row)

today = partdb.today

spartan3a_grid = process_csv(
    'xilinx_data/spartan3a.csv',
    'xilinx_data/spartan3a_shared.csv',
    speed_grades=['-4',],
    temp_grade='C')
spartan3a_grid['vendor'] = "Xilinx"
spartan3a_grid['familyname'] = "Spartan3A"

virtex6_grid = process_csv(
    'xilinx_data/virtex6.csv',
    'xilinx_data/virtex6_shared.csv',
    speed_grades=['-1', '-2'],
    temp_grade='C') # E, I
virtex6_grid['vendor'] = "Xilinx"
virtex6_grid['familyname'] = "Virtex6"

virtex7_grid = process_csv(
    'xilinx_data/virtex7.csv',
    'xilinx_data/virtex7_shared.csv',
    speed_grades=['-1', '-2'],
    temp_grade='C') # E, I
virtex7_grid['vendor'] = "Xilinx"
virtex7_grid['familyname'] = "Virtex7"

kintex7_grid = process_csv(
    'xilinx_data/kintex7.csv',
    'xilinx_data/kintex7_shared.csv',
    speed_grades=['-1', '-2'],
    temp_grade='C') # E, I
kintex7_grid['vendor'] = "Xilinx"
kintex7_grid['familyname'] = "Kintex7"

artix7_grid = process_csv(
    'xilinx_data/artix7.csv',
    'xilinx_data/artix7_shared.csv',
    speed_grades=['-2', '-3'],
    temp_grade='C') # E, I
artix7_grid['vendor'] = "Xilinx"
artix7_grid['familyname'] = "Artix7"

spartan6_grid = process_csv(
    'xilinx_data/spartan6.csv',
    'xilinx_data/spartan6_shared.csv',
    speed_grades=['-2', '-3'],
    temp_grade='C')
spartan6_grid['vendor'] = "Xilinx"
spartan6_grid['familyname'] = "Spartan6"

zynq7000_grid = process_csv(
    'xilinx_data/zynq7000.csv',
    'xilinx_data/zynq7000_shared.csv',
    speed_grades=['-1'],
    temp_grade='C')
zynq7000_grid['vendor'] = "Xilinx"
zynq7000_grid['familyname'] = "Zynq7000"

