import os
import argparse
from pathlib import Path
from typing import List, Tuple


def read_file(file_path: Path, sep: str, lower_case: bool):
    data = []
    unused_data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if lower_case:
                line = line.lower()
            if line != '' and line  != '	':
                line = line.split(sep)
                if len(line) == 2:
                    if ',' in line[-1]:
                        tmp = line[-1].split(',')
                        tmp = [t for t in tmp if t != '']

                        data.extend(list(zip([line[0],]*len(tmp), tmp)))
                    else:
                        data.append(tuple(line))
                else:
                    unused_data.append(tuple(line))
    print(f'Data len: {len(data)}, unused data len: {len(unused_data)}')
    return data, unused_data


def del_unions(new_data: List[Tuple[str]], old_data: List[Tuple[str]]):
    return list(set(new_data) - set(old_data))


def file_lines(filename):
    f = open(filename, 'rb')
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)
    f.close()
    return lines


def write_output(data: List[Tuple[str]], type: str, output_file: Path, rewrite_output: bool):
    if rewrite_output:
        flag = 'w'
    else:
        flag = 'a'
        old_data, _ = [], []
        if os.path.exists(output_file):
            old_data, _ = read_file(output_file, '	', True)
        old_len = len(data)
        data = del_unions(data, old_data)
        print(f'Delete {old_len - len(data)} repeatings')
    with open(output_file, flag, encoding='utf-8') as f:
        for sample in data:
            if type == 'en-ru':
                sample = (sample[1], sample[0])
            f.write(f'{sample[0]}	{sample[1]}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_file')
    parser.add_argument('--sep', default='	')
    parser.add_argument('--output_dir', default='./clean_data')
    parser.add_argument('--output_file')
    parser.add_argument('--lower_case', action='store_true')
    parser.add_argument('--rewrite_output', action='store_true')
    parser.add_argument('--type', choices=['ru-en', 'en-ru'])
    parser.set_defaults(lower_case=False, rewrite_output=False)

    args = parser.parse_args()
    assert args.raw_file is not None, 'You should define --raw_file'
    assert args.output_file is not None, 'You should defile --output_file'
    assert args.type in ['ru-en', 'en-ru'], 'You should defile --type as ru-en or en-ru'
    print('-------------------------------------------------')
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    raw_file = Path(args.raw_file)
    data, _ = read_file(raw_file, args.sep, args.lower_case)
    
    output_file = Path(args.output_dir, args.output_file)

    write_output(data, args.type, output_file, args.rewrite_output)
    print(f'Write data to {output_file}')
    print(f'Total samples: {file_lines(output_file)}')
    print('-------------------------------------------------')
