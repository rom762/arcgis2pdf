import glob
import json
import os
from pathlib import Path
from pprint import pprint


def parse_coords(raw_coords: list):
    new_coords = []
    for line in raw_coords:
        if len(line) > 0:
            coords = [float(val) for val in line.split(',') if len(val) > 0]
            new_coords.append(coords)
    return new_coords


def parse_txt(*args, **kwargs) -> dict:
    filepath = kwargs.get('filepath', r'c:\Users\nickr\YandexDisk\Coding\Python\Work\Shell_Projects\arcgis2pdf\data\RES\77-01-02-000696.txt')
    filename = Path(filepath).stem
    image_path = os.path.join(os.path.dirname(filepath), f'{filename}.jpg')

    with open(filepath, 'r', encoding='utf-8') as ff:
        lines = ff.readlines()

    lines = [line.strip() for line in lines]
    active_poligon = 'poligon1'
    data = {
        'filename': filename,
        'area': 0,
        'poligon1': {
            'parts': 0,
            'rings': [],
        },
        'poligon2': {
            'parts': 0,
            'rings': [],
        },
        'image': image_path,
    }

    if not lines[0].startswith('Area:'):
        raise Exception(f"Wrong file format for {filename}")

    for line in lines:
        if line.startswith('Area:'):
            data['area'] = float(line.split(':')[1].strip())
        if line == 'ВТОРОЙ ПОЛИГОН':
            active_poligon = 'poligon2'
            print(f'{filename} имеет два полигона')
        if line.startswith('Parts:'):
            data[active_poligon]['parts'] = int(line.split(':')[1])
        if line[:3].isdigit():
            raw_coords = line.strip().split(';')
            coords = parse_coords(raw_coords)
            data[active_poligon]['rings'].append(coords)
    return data


if __name__ == "__main__":
    print('почему то срабатывает name=main')
    datadir = os.path.join(os.getcwd(), 'data', 'RES', '*.txt')
    files = glob.glob(datadir)
    aggregate = []
    for filepath in files:
        filename = Path(filepath).stem
        aggregate.append(parse_txt(filepath=filepath))

    with open('data/aggregate.json', 'w') as f:
        f.write(json.dumps(aggregate))

    # for file in aggregate[5]:
    #     for k, v in file.items():
    #         for ring in v['poligon1']['rings']:
    #             for coords in ring:
    #                 if coords[0] in coords[1:]:
    #                     print(k, ring[0], ring[-1])
