#!/usr/bin/env python3
from argparse import ArgumentParser
import sys

from PIL import Image

from download import get_tile

parser = ArgumentParser()
LEVEL = 0
parser.add_argument('--level', default=LEVEL, type=int,
                    help='zoom level')
START = (-2, -1)
parser.add_argument('--start', nargs=2, type=int, default=START)
SIZE = (4, 3)
parser.add_argument('--size', nargs=2, type=int, default=SIZE)


def main():
    args = parser.parse_args()

    tiles = [[None] * args.size[0] for i in range(args.size[1])]
    for x in range(args.size[0]):
        for y in range(args.size[1]):
            tile_x = args.start[0] + x
            tile_y = args.start[1] + y
            tiles[y][x] = get_tile(args.level, tile_x, tile_y)

    width = sum(tiles[0][x].size[0] for x in range(args.size[0]))
    height = sum(tiles[y][0].size[1] for y in range(args.size[1]))

    tile_map = Image.new('RGB', (width, height))
    x_offset = 0
    for x in range(args.size[0]):
        y_offset = 0
        for y in range(args.size[1]):
            t = tiles[y][x]
            tile_map.paste(t, (x_offset, y_offset))
            y_offset += t.size[1]
        x_offset += t.size[0]
    # tile_map.resize((int(width * 2), int(height * 2)), Image.BICUBIC)
    tile_map.save('map.png')


if __name__ == "__main__":
    sys.exit(main())
