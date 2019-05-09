#!/usr/bin/env python
import sys
from argparse import ArgumentParser

from PIL import Image
import pytesseract

parser = ArgumentParser()
parser.add_argument('filename', help='path to the image')


def main():
    args = parser.parse_args()
    image = Image.open(args.filename)
    text = pytesseract.image_to_string(image)
    print(text)


if __name__ == "__main__":
    sys.exit(main())
