from asyncore import read
import os
import argparse
from pathlib import Path


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [tuple(fl.replace('\n', '').split('	')) for fl in f]
    return data


def merge(files, format):
    data, merged_data = [], []
    for file_path in files:
        data.extend(read_file(file_path))
    if format == 'transformers':
        for sample in data:
            merged_data.append({'translation': {'ru': sample[0], 'en': sample[1]}})
    else:
        raise Exception('not implemented')
    return merged_data
    

def write_output(file_path, data, format):
    with open(file_path, 'w', encoding='utf-8') as f:
        if format == 'transformers':
            import json
            for sample in data:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')
        else:
           raise Exception('not implemented') 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', type=str)
    parser.add_argument('--file_dir', type=str, default='./clean_data')
    parser.add_argument('--output_format', choices=['transformers', 'opennmt'], default='transformers')
    parser.add_argument('--output_file', type=str)

    args = parser.parse_args()

    assert args.files is not None
    assert args.output_file is not None

    files = args.files.split(',')
    
    files = [Path(args.file_dir, f) for f in files]
    output_file = Path(args.file_dir, args.output_file)

    merged_data = merge(files, args.output_format)
    write_output(output_file, merged_data, args.output_format)
