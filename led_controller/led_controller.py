#!/root/env/bin/python3
# -*- coding: utf-8 -*

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# NeoPixels on Raspberry Pi

# See https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/ 

import time
import board
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

import math
import random
import logging
from time import sleep
from datetime import date, datetime, timezone, timedelta
from suntime import Sun, SunTimeException


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 420

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
#ORDER = neopixel.RGB

# Colors
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (127, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Declare a 6-element RGB rainbow palette
palette = [ 
  fancy.CRGB(1.0, 0.0, 0.0),  # Red 
  fancy.CRGB(0.5, 0.5, 0.0),  # Yellow
  fancy.CRGB(0.0, 1.0, 0.0),  # Green
  fancy.CRGB(0.0, 0.5, 0.5),  # Cyan
  fancy.CRGB(0.0, 0.0, 1.0),  # Blue
  fancy.CRGB(0.5, 0.0, 0.5),  # Magenta
]

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
  # Input a value 0 to 255 to get a color value.
  # The colours are a transition r - g - b - back to r.
  if pos < 0 or pos > 255:
    r = g = b = 0
  elif pos < 85:
    r = int(pos * 3)
    g = int(255 - pos * 3)
    b = 0
  elif pos < 170:
    pos -= 85
    r = int(255 - pos * 3)
    g = 0
    b = int(pos * 3)
  else:
    pos -= 170
    r = 0
    g = int(pos * 3)
    b = int(255 - pos * 3)
  return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def setPixelHeatColor(Pixel, temperature):
  # Scale 'heat' down from 0-255 to 0-191
  t192 = round((temperature/255.0)*191)

  # calculate ramp up from
  heatramp = t192 & 0x3F # 0..63
  heatramp <<= 2 # scale up to 0..252
  
  # figure out which third of the spectrum we're in
  if t192 > 0x80 :
    pixels[Pixel] = (255, 255, heatramp) # hottest
  elif t192 > 0x40 :
    pixels[Pixel] = (255, heatramp, 0)   # medium
  else :
    pixels[Pixel] = (heatramp, 0, 0)     # coolest

    
def rainbow_cycle():
  for l in range(255):
    for j in range(255):
      for i in range(num_pixels):
        pixel_index = int((i * 256 // num_pixels) + j)
        pixels[i] = wheel(pixel_index & 255)
      pixels.show()
      time.sleep(0.001) # rainbow cycle with 1ms delay per step


def black_and_white():
  for i in range(0,num_pixels-29,30):
    for b in range(8):
      pixels[i+b] = BLACK
    for b in range(8,22):
      if 12 < b < 17 :
        pixels[i+b] = BLACK
      else:
        pixels[i+b] = WHITE
    for b in range(22,30):
      pixels[i+b] = BLACK


def holiday():
  for i in range(0,num_pixels-29,30):
    for b in range(0,8):
      pixels[i+b] = GREEN
    for b in range(8,22):
      if 12 < b < 17 :
        pixels[i+b] = GREEN
      else:
        pixels[i+b] = RED
    for b in range(22,30):
      pixels[i+b] = GREEN


#random.uniform(0, 1)
def halloween():
  for l in range(255):
    if bool(random.getrandbits(1)):
      for i in range(0,num_pixels-29,30):
       for b in range(8):
         pixels[i+b] = BLACK
       for b in range(8,22):
         if b > 12 and b < 17 :
           pixels[i+b] = BLACK
         else:
           pixels[i+b] = ORANGE
       for b in range(22,30):
         pixels[i+b]  = BLACK
    else:
      pixels.fill(BLACK)
    pixels.show()
    sleep(random.uniform(0.09, 0.5))


def gradient():
  offset = 0
  for l in range(255):
    for i in range(num_pixels):
      # Load each pixel's color from the palette using an offset, run it
      # through the gamma function, pack RGB value and assign to pixel.
      color = fancy.palette_lookup(palette, offset + i / num_pixels)
      color = fancy.gamma_adjust(color, brightness=0.25)
      pixels[i] = color.pack()
    pixels.show()
    offset += 0.02 # Bigger number = faster spin


def knight_rider(color, wait, barLength):
  off = BLACK
  for l in range(255):
    i = j = k = 0
    while i < num_pixels:
      for k in range(barLength):
        pixels[k] = color
        pixels.show()
        sleep(wait)
      for j in range(num_pixels-barLength):
        pixels[j] = off
        pixels[j+barLength] = color
        pixels.show()
        sleep(wait)
      for k in range(num_pixels-1,num_pixels-barLength,-1):
        pixels[k] = color
        pixels.show()
        sleep(wait)
      for j in range(num_pixels-1,0,-1):
        pixels[j] = off
        pixels[j-barLength] = color
        pixels.show()
        sleep(wait)
    pixels[0] = off
    pixels.show()
    sleep(wait)


def RGBLoop():
  for l in range(255):
    for j in range(0,3):
      for k in range(0,255): # Fade IN
        match j:
          case 0:
            pixels.fill((k, 0, 0))
          case 1:
            pixels.fill((0, k, 0))
          case 2:
            pixels.fill((0, 0, k))
        pixels.show()
        sleep(3)
      for k in range(255,0,-1): # Fade OUT
        match j:
          case 0:
            pixels.fill((k, 0, 0))
          case 1:
            pixels.fill((0, k, 0))
          case 2:
            pixels.fill((0, 0, k))
        pixels.show()
        sleep(3)


def CylonBounce(r, g, b, EyeSize, SpeedDelay, ReturnDelay):
  for l in range(255):
    for i in range(0,num_pixels-EyeSize-2):
      pixels.fill(BLACK)
      pixels[i]  = (int(r/10), int(g/10), int(b/10))
      for j in range(1,EyeSize+1):
        pixels[i+j]  = (r, g, b)
      pixels[i+EyeSize+1]  = (int(r/10), int(g/10), int(b/10))
      pixels.show()
      sleep(SpeedDelay)

    sleep(ReturnDelay)

    for i in range(num_pixels-EyeSize-2,0, -1):
      pixels.fill(BLACK)
      pixels[i]  = (int(r/10), int(g/10), int(b/10))
      for j in range(1,EyeSize+1):
        pixels[i+j]  = (r, g, b)
      pixels[i+EyeSize+1]  = (int(r/10), int(g/10), int(b/10))
      pixels.show()
      sleep(SpeedDelay)

    sleep(ReturnDelay)


def Twinkle(r, g, b, Count, SpeedDelay, OnlyOne):
  for l in range(255):
    pixels.fill(BLACK)
    for i in range(0,Count):
      pixels[random.randint(0,num_pixels-1)]  = (r, g, b)
      pixels.show()
      sleep(SpeedDelay)
      if OnlyOne:
        pixels.fill(BLACK)
    sleep(SpeedDelay)


def TwinkleRandom(Count, SpeedDelay, OnlyOne):
  for l in range(255):
    pixels.fill(BLACK)
    for i in range(0,Count):
      pixels[random.randint(0,num_pixels-1)]  = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
      pixels.show()
      sleep(SpeedDelay)
      if OnlyOne:
        pixels.fill(BLACK)
    sleep(SpeedDelay)


def Sparkle(r, g, b, SpeedDelay):
  for l in range(255):
    Pixel = random.randint(0,num_pixels-1)
    pixels[Pixel] = (r, g, b)
    pixels.show()
    sleep(SpeedDelay)
    pixels[Pixel] = (0,0,0)


def SnowSparkle(r, g, b, SparkleDelay, SpeedDelay):
  for l in range(255):
    pixels.fill((r, g, b))
    Pixel = random.randint(0,num_pixels-1)
    pixels[Pixel] = (255,255,255)
    pixels.show()
    sleep(SparkleDelay)
    pixels[Pixel] = ((r, g, b))
    pixels.show()
    sleep(SpeedDelay)


def RunningLights(r, g, b, WaveDelay):
  for l in range(128):
    Position = 0
    for j in range(num_pixels*2):
      Position += 1
      for i in range(num_pixels-1):
        # sine wave, 3 offset waves make a rainbow!
        # float level = sin(i+Position) * 127 + 128;
        # setPixel(i,level,0,0);
        # float level = sin(i+Position) * 127 + 128;
        R = int(((math.sin(i+Position) * 127 + 128)/255)*r)
        G = int(((math.sin(i+Position) * 127 + 128)/255)*g)
        B = int(((math.sin(i+Position) * 127 + 128)/255)*b)
        pixels[i] = (R, G, B)
      pixels.show()
      sleep(WaveDelay)


def colorWipe(r, g, b, SpeedDelay):
  for l in range(255):
    for i in range(num_pixels-1):
      pixels[i] = (r, g, b)
      pixels.show()
      sleep(SpeedDelay)
    for i in range(num_pixels-1):
      pixels[i] = (0, 0, 0)
      pixels.show()
      sleep(SpeedDelay)


def theaterChase(r, g, b, SpeedDelay):
  for l in range(255):
    for j in range(0,9): # do 10 cycles of chasing
      for q in range (0,2):
        for i in range(0, num_pixels-1, 3):
          pixels[i+q] = (r, g, b) # turn every third pixel on
        pixels.show()
        sleep(SpeedDelay)
        for i in range(0, num_pixels-1, 3):
          pixels[i+q] = (0, 0, 0) # turn every third pixel off


def theaterChaseRainbow(SpeedDelay):
  for l in range(255):
    for j in range(0,255): # cycle all 256 colors
      for q in range (0,2):
        for i in range(0, num_pixels-1, 3):
          pixels[i+q] = wheel( (i+j) % 255 ) # turn every third pixel on
        pixels.show()
        sleep(SpeedDelay)
        for i in range(0, num_pixels-1, 3):
          pixels[i+q] = (0, 0, 0) # turn every third pixel off


def Fire(Cooling, Sparking, SpeedDelay):
  for l in range(255):

    heat = [0] * num_pixels

    for i in range(0, num_pixels-1):
      cooldown = random.randint(0, int(((Cooling * 10) / num_pixels) + 2))
      if cooldown > heat[i]:
        heat[i] = 0
      else:
        heat[i]=heat[i]-cooldown

    for k in range(num_pixels-2, 2, -1):
      heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3

    if random.randint(1, 255) < Sparking:
      y = random.randint(1, 7)
      heat[y] = heat[y] + random.randint(160,255)

    for j in range(0, num_pixels-1):
       setPixelHeatColor(j, heat[j])

    pixels.show()
    sleep(SpeedDelay)


#####################################################################################
# Main loop

try:

  latitude = 45.26886663548439
  longitude = -75.27623677331822
  sun = Sun(latitude, longitude)
  current_month_day = datetime.now().strftime('%m-%d')

  pixels.fill((0,0,0))
  pixels.show()

  while True:
    
    today_sr = sun.get_sunrise_time().astimezone()
    today_ss = sun.get_sunset_time().astimezone()

    now = datetime.now().astimezone()

    sr_ut = time.mktime(today_sr.timetuple()) - 1800.0
    ss_ut = time.mktime(today_ss.timetuple()) + 1800.0
    now_ut = time.mktime(now.timetuple())

    if (now_ut < ss_ut and now_ut > sr_ut):
      pixels.fill((0, 0, 0)) # All black - not time to iluminate
    else:
      match current_month_day:
        case '12-15'|'12-16'|'12-17'|'12-18'|'12-19'|'12-20'|'12-21'|'12-22'|'12-23'|'12-26'|'12-27'|'12-28'|'12-29'|'12-30':
          holiday()
        case '01-02'|'01-03'|'01-04'|'01-05'|'01-06'|'01-07'|'01-08':
          holiday()
        case '12-24'|'12-25'|'12-31'|'01-01':
          rainbow_cycle()
        case '01-31'|'06-15'|'07-30'|'10-26':
          gradient()
        case '02-02':
          knight_rider(RED, 0.05, 8)
        case '10-31':
          halloween()
        case _:
          #RGBLoop()
          #CylonBounce(0xff, 0, 0, 4, 0.010, 0.050)
          #Twinkle(255, 0, 0, 3, 0.100, False) # Width = 3 pixels
          #TwinkleRandom(2, 0.100, False) # Width = 2 pixels
          #Sparkle(255,255,255,0)
          #SnowSparkle(16, 16, 16, 0.020, random.randint(100,1000))
          #RunningLights(0, 255, 0, 0.050)
          #colorWipe(0, 255, 0, 0.050)
          #theaterChase(255,0,0,0.050)
          #theaterChaseRainbow(0.050)
          #Fire(55,120,0.15)
          black_and_white()

    pixels.show()
    sleep(600)

except KeyboardInterrupt as e:
  logging.info("Stopping...")
