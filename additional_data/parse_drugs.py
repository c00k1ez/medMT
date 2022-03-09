import os
import argparse
from pathlib import Path

from bs4 import BeautifulSoup
import requests
import re


_BASE_LINK = 'https://www.vidal.ru'


def get_links():
    r = requests.get(f'{_BASE_LINK}/drugs/products/p/rus-a')
    soup = BeautifulSoup(r.text, features='html.parser')
    letters = [a for a in soup.find('div', {'class', 'letters-russian'}).contents if a != '\n']
    links = [f'{_BASE_LINK}{l["href"]}' for l in letters]
    return links


def _postprocess_ru_name(name):
    name = name.lower()
    name = name.replace('\n', '')
    name = name.replace('®', '')
    name = name.replace('+', ' ')
    name = re.sub(r'[0-9]+', '', name)
    return name.strip()


def _postprocess_en_name(name):
    name = name.replace('-', ' ')
    name = name.replace('_', ' ')
    name = re.sub(r'[0-9]+', '', name)
    return name.strip()


def parse_drugs(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features='html.parser')
    contents = soup.find_all('td', {'class': 'products-table-name'})
    data = []
    for content in contents:
        ru_name = _postprocess_ru_name(content.contents[1].text)
        en_name = _postprocess_en_name(content.contents[1]['href'].split('/drugs/')[-1])
        data.append((ru_name, en_name))
    data = list(dict.fromkeys(data))
    return data


def write_output(data, output_file: Path, rewrite_output: bool):
    if rewrite_output:
        flag = 'w'
    else:
        flag = 'a'
    with open(output_file, flag, encoding='utf-8') as f:
        for sample in data:
            f.write(f'{sample[0]}	{sample[1]}\n')


def parse_letter_link(link):
    print('-------------------------------------------------')
    print(f'Parse {link}')
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features='html.parser')
    spans = soup.find('span', {'class': 'last'})
    if spans is not None:
        last_page = int(spans.contents[1]['href'].split('?p=')[-1])
    else:
        last_page = 1
    pages = list(range(1, last_page + 1))
    print(f'Pages: {last_page}')
    data = []
    for page in pages:
        total_link = f'{link}?p={page}'
        parsed_data = parse_drugs(total_link)
        print(f'Page:\t{page}\t{len(parsed_data)} samples')
        data.extend(parsed_data)
    return data


def write_metadata(metadata_file, link):
    with open(metadata_file, 'w', encoding='utf-8') as f:
        f.write(link)


def read_metadata(metadata_file):
    with open(metadata_file, 'r', encoding='utf-8') as f:
        old_link = f.read()
    return old_link.replace('\n', '').strip()


def restore_parse(metadata_file, links):
    old_link = read_metadata(metadata_file)
    print(f'Last parsed link: {old_link}')
    link_id = links.index(old_link)
    return links[link_id + 1:]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', default='./clean_data')
    parser.add_argument('--rewrite_output', action='store_true')
    parser.add_argument('--output_file')
    parser.set_defaults(rewrite_output=False)

    args = parser.parse_args()
    assert args.output_file is not None, 'You should define --output_file'

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    output_file = Path(args.output_dir, args.output_file)
    metadata_output_file = Path(args.output_dir, args.output_file + '.metadata')

    links = get_links()
    if os.path.exists(metadata_output_file):
        links = restore_parse(metadata_output_file, links)
        print(f'Start from {links[0]}')
    data = []
    print(f'Number of links: {len(links)}')
    first_link = True
    for link in links:
        parsed_data = parse_letter_link(link)
        data.extend(parsed_data)
        print(f'Total samples: {len(data)}')
        write_metadata(metadata_output_file, link)
        if first_link:
            write_output(data, output_file, args.rewrite_output)
            first_link = False
        else:
            write_output(parsed_data, output_file, False)
    
    print(f'Write data to {output_file}')
