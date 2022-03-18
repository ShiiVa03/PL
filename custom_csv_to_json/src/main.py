import re

from sys import version_info, argv
from itertools import islice
from typing import Optional, Tuple, Union, List, Callable


if 3 > version_info.major or (3 == version_info.major and 6 >= version_info.minor):
    raise Exception("Python must be >=3.6")

if (len(argv) != 2):
    raise Exception("Script requires only one aditional argument")

agg_funcs = {
    'sum': lambda x: str(sum(map(int, x))),
    'median': lambda x: str(sum(map(int, x))/len(x)),
    'count': lambda x: str(len(x)), 
}


file = open(argv[1], encoding='utf8')

header = file.readline()

agg_funcs_exp = '|'.join(agg_funcs.keys())

mode_exp = f'(?:::({agg_funcs_exp}))'
list_exp = fr'(?:{{(\d+)(?:,(\d+))?}}{mode_exp}?)'

col_exp = fr'(?:(?:(".*?"|[^,"{{}}]+){list_exp}?)?(?:,|\n))'

#header_exp_check = fr'^(({item_header_exp})?,)*({item_header_exp})?\n'
header_exp_check = fr'{col_exp}+'

if not re.fullmatch(header_exp_check, header):
    raise Exception("Header isn't valid")


'''
Check if headers aren't blank except those which reference a list slot (blank obligatory)
'''
print(col_exp)

columns = {} # Dict is ordered since Python 3.6
list_count = 0

for col, min_v, max_v, mode in re.findall(col_exp, header):
    print(col)
    if not col:
        if list_count == 0:
            raise Exception("Blank header isn't allowed")
        list_count -= 1

    else:
        col = col.strip('"')
        
        if col in columns:
            raise Exception(f"Column `{col}` is repeated")

        if list_count > 0:
            raise Exception(f"Column `{col}` is inside the previous list")

        if min_v:
            try:
                opt = (int(min_v), int(max_v or min_v), (mode, agg_funcs[mode]) if mode else None)
            except KeyError:
                raise Exception(f"Column `{col}` has invalid mode {mode}")
            
            if opt[1] == 0 or opt[0] > opt[1]:
                raise Exception(f"Column `{col}` must has list with invalid size(s)")

            list_count = opt[1]
            columns[col] = opt
        else:
            columns[col] = None
            
        
        

print(columns)

n_columns = sum(v[1] if v else 1 for v in columns.values())



json_output = []

item_row_exp = r'(".*?"|[^,]*)(?:,|$)'

row_exp_check = fr'^(?:{item_row_exp}){{{n_columns}}}'
print(row_exp_check)

item_row_re = re.compile(item_row_exp)
row_re_check = re.compile(row_exp_check)




for idx, _line in enumerate(file):
    line = _line.strip('"\n')

    if not line: # Blank line
        continue
    
    if not row_re_check.fullmatch(line):
        raise Exception(f"Line {idx + 1} doesn\'t follow the correct pattern")

    results = iter(item_row_re.findall(line))
    print(item_row_re.findall(line))
    
    def get_pair(col: str, opt: Optional[Tuple[int, int, Tuple[str, Callable[[List[str]], str]]]]) -> Union[str, List[str]]:    
        if opt:
            
            min_v, max_v, mode = opt
            
            r = [x for x in islice(results, max_v) if x]

            if len(r) < min_v:
                raise Exception(f"Line {idx + 1} contains a list without enough values")


            if mode:
                mode_name, mode_func = mode
                
                return (col + '_' + mode_name, mode_func(r))
            
            return (col, r)
        else:
            try:
                return (col, next(results))
            except StopIteration:
                raise Exception(f"Line {idx + 1} doesn't have enough values")
            
    
    values = dict(get_pair(col, opt) for col, opt in columns.items())
    json_output.append(values)

print(json_output)

