import re

from sys import version_info
from itertools import islice


if 3 > version_info.major or (3 == version_info.major and 6 >= version_info.minor):
    raise Exception("Python must be >=3.6")


file = open("file2.csv", encoding='utf8')

header = file.readline().rstrip()
item_header_exp = r'([^,{}]+)(?:{(\d+)})?'

col_exp = fr'(?:^|,)(?:{item_header_exp})?'

header_exp_check = fr'^(({item_header_exp})?,)*$'

if not re.match(header_exp_check, header):
    raise Exception("Header isn't valid")


'''
Check if headers aren't blank except those which reference a list slot (blank obligatory)
'''


columns = {} # Dict is ordered since Python 3.6
list_count = 0

for col, count in re.findall(col_exp, header):
    print(col)
    if not col:
        if list_count == 0:
            raise Exception("Blank header isn't allowed")
        list_count -= 1

    else:
        if col in columns:
            raise Exception(f"Column `{col}` is repeated")

        if list_count > 0:
            raise Exception(f"Column `col` is inside the previous list")
        
        count = int(count or 0)
        columns[col] = count
        list_count = count

print(columns)

n_columns = sum(max(v, 1) for v in columns.values())



json_output = []

row_exp_check = fr'^([^,]+,){{{n_columns - 1}}}([^,]+)$'
print(row_exp_check)
row_re_check = re.compile(row_exp_check)

item_row_exp = r'([^,]+)'
item_row_re = re.compile(item_row_exp)

for idx, _line in enumerate(file):
    line = _line.rstrip()
    
    if not row_re_check.match(line):
        raise Exception(f'Line {idx + 1} doesn\'t follow the correct pattern')

    results = iter(item_row_re.findall(line))
    get_value = lambda count: list(islice(results, count)) if count > 0 else next(results) 
    values = {col:get_value(count) for col, count in columns.items()}
    json_output.append(values)

print(json_output)

