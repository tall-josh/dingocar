#!/usr/bin/env python

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import sys
import textwrap

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

font = ImageFont.load_default()

disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height

if len(sys.argv) > 1:
  message = sys.argv[1]

  image = Image.new('1', (width, height))
  text = textwrap.fill(
    message, width=8, initial_indent=' ', subsequent_indent=' ',
    break_long_words=False)
  draw = ImageDraw.Draw(image)
  draw.text((0, 0), text, font=font, fill=255)
  image = image.rotate(180)
  disp.image(image)
  disp.display()
