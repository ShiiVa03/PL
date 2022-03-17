import re

from sys import version_info
from itertools import islice
from typing import Optional, Tuple, Union, List


if 3 > version_info.major or (3 == version_info.major and 6 >= version_info.minor):
    raise Exception("Python must be >=3.6")


file = open("file.csv", encoding='utf8')

header = file.readline()
item_header_exp = r'([^,{}]+)(?:{(\d+)(?:,(\d+))?})?'

col_exp = fr'(?:{item_header_exp})?(?:,|\n)'

header_exp_check = fr'^(({item_header_exp})?,)*({item_header_exp})?\n'

if not re.fullmatch(header_exp_check, header):
    raise Exception("Header isn't valid")


'''
Check if headers aren't blank except those which reference a list slot (blank obligatory)
'''
print(col_exp)

columns = {} # Dict is ordered since Python 3.6
list_count = 0

for col, min_v, max_v in re.findall(col_exp, header):
    print(col)
    if not col:
        if list_count == 0:
            raise Exception("Blank header isn't allowed")
        list_count -= 1

    else:
        if col in columns:
            raise Exception(f"Column `{col}` is repeated")

        if list_count > 0:
            raise Exception(f"Column `{col}` is inside the previous list")

        if min_v:
            counts = (int(min_v), int(max_v or min_v))
            if counts[1] == 0 or counts[0] > counts[1]:
                raise Exception(f"Column `{col}` must has list with invalid size(s)")

            list_count = counts[1]
            columns[col] = counts
        else:
            columns[col] = None
            
        
        

print(columns)

n_columns = sum(v[1] if v else 1 for v in columns.values())



json_output = []

row_exp_check = fr'^([^,]*,){{{n_columns - 1}}}([^,]*)$'
print(row_exp_check)
row_re_check = re.compile(row_exp_check)

item_row_exp = r'([^,]*)(?:,|$)'
item_row_re = re.compile(item_row_exp)

for idx, _line in enumerate(file):
    line = _line.rstrip()

    if not line: # Blank line
        continue
    
    if not row_re_check.fullmatch(line):
        raise Exception(f"Line {idx + 1} doesn\'t follow the correct pattern")

    results = iter(item_row_re.findall(line))
    print(item_row_re.findall(line))
    
    def get_value(count: Optional[Tuple[int, int]]) -> Union[str, List[str]]:
        print(count)
        if count:
            r = [x for x in islice(results, counts[1]) if x]

            if len(r) < counts[0]:
                raise Exception(f"Line {idx + 1} contains a list without enough values")

            return r
        else:
            return next(results)
        
    values = {col:get_value(count) for col, count in columns.items()}
    json_output.append(values)

print(json_output)

