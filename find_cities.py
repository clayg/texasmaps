#!/usr/bin/env python
from PIL import Image
import pytesseract
import cv2

from argparse import ArgumentParser
import sys

parser = ArgumentParser()
parser.add_argument('filename', help='path to the image')
parser.add_argument('output', help='path to save image')


def main():
    args = parser.parse_args()

    # white wash the map to draw out text
    image = Image.open(args.filename)
    data = []
    for pixel in image.getdata():
        if sum(pixel) < 350 and max(pixel) - min(pixel) < 70:
            data.append(pixel)
        else:
            data.append((255, 255, 255))

    # drop white washed image to disk
    new = Image.new(image.mode, image.size)
    new.putdata(data)
    tmp_filename = '.tmp.' + args.output
    with open(tmp_filename, 'wb') as f:
        new.save(f)

    # extract text from the image
    img = cv2.imread(tmp_filename)
    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    # add boxes to map
    img = cv2.imread(args.filename)
    for text, conf, x, y, w, h in zip(d['text'], d['conf'], d['left'],
                                      d['top'], d['width'], d['height']):
        if not text:
            continue
        print('found: {0}'.format(text))
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # write out annotated map
    cv2.imwrite(args.output, img)


if __name__ == "__main__":
    sys.exit(main())
