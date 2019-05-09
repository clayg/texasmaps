#!/usr/bin/env python
from PIL import Image

from argparse import ArgumentParser
import sys

parser = ArgumentParser()
parser.add_argument('filename', help='path to the image')
parser.add_argument('output', help='path to save image')


def main():
    args = parser.parse_args()
    image = Image.open(args.filename)
    data = []
    for pixel in image.getdata():
        if sum(pixel) < 350 and max(pixel) - min(pixel) < 70:
            data.append(pixel)
        else:
            data.append((255, 255, 255))
    new = Image.new(image.mode, image.size)
    new.putdata(data)
    with open(args.output, 'wb') as f:
        new.save(f)


if __name__ == "__main__":
    sys.exit(main())
