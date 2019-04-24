#!/usr/bin/env python3
from argparse import ArgumentParser
import os
import sys
from io import BytesIO

from PIL import Image
import requests

HOSTNAME = 'server.arcgisonline.com'
PATH = '/ArcGIS/rest/services/World_Street_Map/MapServer/tile'
CACHE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.cache'))

LEVEL_MAP = {
    0: 10,
    1: 11,
    2: 12,
    3: 13,
    4: 14,
}

parser = ArgumentParser()
parser.add_argument('--level', type=int, default=0, choices=LEVEL_MAP.keys(),
                    help='zoom level')
parser.add_argument('x', nargs='?', default=0, type=int,
                    help='horizontal position relative to Plano')
parser.add_argument('y', nargs='?', default=0, type=int,
                    help='vertical position relative to Plano')

COORDINATE_MAP = {
    14: (
        lambda y: 6598 + y,
        lambda x: 3791 + x,
    ),
    13: (
        lambda y: 3299 + y,
        lambda x: 1895 + x,
    ),
    12: (
        lambda y: 1649 + y,
        lambda x: 947 + x,
    ),
    11: (
        lambda y: 824 + y,
        lambda x: 473 + x,
    ),
    10: (
        lambda y: 412 + y,
        lambda x: 236 + x,
    ),
}


def get_image(group, subdir, image):
    image_path = os.path.join(CACHE_ROOT, f'{group}_{subdir}_{image}')
    try:
        with open(image_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        try:
            with open(image_path, 'wb') as f:
                path = f'https://{HOSTNAME}{PATH}/{group}/{subdir}/{image}'
                print(f'downloading {path}')
                resp = requests.get(path, stream=True)
                if resp.status_code != 200:
                    raise Exception(f'Unexpected response {resp.status}')
                data = resp.raw.read()
                f.write(data)
        except FileNotFoundError:
            os.mkdir(CACHE_ROOT)
            data = get_image(group, subdir, image)
    return data


def get_tile(level, x, y):
    group = LEVEL_MAP[level]
    subdir = COORDINATE_MAP[group][0](y)
    image = COORDINATE_MAP[group][1](x)
    data = get_image(group, subdir, image)
    img = Image.open(BytesIO(data))
    return img


def main():
    args = parser.parse_args()
    img = get_tile(args.level, args.x, args.y)
    img.show()


if __name__ == "__main__":
    sys.exit(main())
